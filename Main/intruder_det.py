# To run this script, run the following commands in the terminal:
# cd Main/
# python intruder_det.py

import cv2
import numpy as np
import time
from datetime import datetime
import os
import threading
import matplotlib.pyplot as plt

# Custom modules
import whatsapp_message

"""
    ? Extra Features:
    * Added cropping of the face from the frame and saving it with a timestamp in a new folder.
    * Added additional checks to ensure that the face is big enough before saving it.
    * Dynamically update the faces list with the faces which are big enough.
    * Added the popup window to display the saved face images from the saved folder.
    * WhatsApp integration to send the saved face images to a WhatsApp number.

"""

# --------------- GLOBAL VARIABLES  ------------------ #

# Intruder detection line
LINE_Y = 200  # in pixels from the top

# True/False: Send/Don't send the saved face images to WhatsApp
WHATSAPP = False


# True/False: Delete/Don't delete the saved face images in the saved folder
DELETE_SAVED_IMAGES = True
if DELETE_SAVED_IMAGES:
    for file in os.listdir("./saved/original"):
        os.remove(f"./saved/original/{file}")
    for file in os.listdir("./saved/canny"):
        os.remove(f"./saved/canny/{file}")


# Set the time interval between each face detection
TIME_INTERVAL = 2  # in seconds
LAST_SAVE_TIME = time.time()  # To store the last time at which the face was saved


def cannyEdgeDetection(image_path):
    """Perform canny edge detection and save the image under 'saved/canny' folder.

    Args:
        image_path (str): The path of the image to perform canny edge detection.

    Returns:
        None
    """

    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Perform canny edge detection
    edges = cv2.Canny(image, 50, 150)

    # Extract the file name and extension
    file_name, file_extension = os.path.splitext(os.path.basename(image_path))

    # Save the canny edge detection result under 'saved/canny' folder
    cv2.imwrite(f"./saved/canny/{file_name}_canny{file_extension}", edges)


def saveImage(frame, x, y, w, h, time):
    """1. Save the face image with the timestamp on the bottom of the image
    2. Display it in a new window
    3. Send it to WhatsApp.

    Args:
        frame: The original frame from which the face is cropped.
        x, y, w, h: The coordinates of the face rectangle in the frame.
        time: The time at which the face was detected.

    Returns:
        None
    """

    # Check if detected face is big enough
    if w < 50 or h < 50:
        return

    # Crop the face from the frame
    face = frame[y-100:y+h+100, x-100:x+w+100]  # 100 pixels extra on each side

    # If image becomes empty, return
    if face.size == 0:
        return

    # Write the timestamp on the bottom of face image and save it
    face = cv2.putText(face, time, (10, y+h), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 255, 255), 2, cv2.LINE_AA)

    # Convert the current time to a string
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current_time_formatted = datetime.now().strftime("on %B %d %Y, at %I:%M:%S %p")

    # Save the face image under "saved/original" folder
    cv2.imwrite(f"./saved/original/face_{current_time}.jpg", face)
    # Perform canny edge detection on the saved face image
    cannyEdgeDetection(f"./saved/original/face_{current_time}.jpg")

    print(f"✅ Face saved at {current_time}")

    # Pop up a window to display the saved face image
    cv2.imshow(f"Face {current_time}", face)
    # Pop up a window to display the canny edge detection result
    canny_edge_detection_result = cv2.imread(
        f"./saved/canny/face_{current_time}_canny.jpg")
    cv2.imshow(
        f"Canny Edge Detection Result {current_time}", canny_edge_detection_result)

    if WHATSAPP:
        # Send the image to whatsapp using a thread
        t = threading.Thread(target=ThreadSendImage, args=(
            f"./saved/original/face_{current_time}.jpg", current_time_formatted))
        t.start()


def ThreadSendImage(path, timestamp):
    """Send the image to WhatsApp using a thread to prevent the program from freezing.

    Args:
        path (str): The path of the image to be sent.
        timestamp (str): The timestamp to be sent with the image.

    Returns:
        None
    """

    whatsapp_message.UploadImage(path, timestamp)


def drawRectangles(frame, faces):
    """Display rectangles around the faces and the number of faces detected on the frame.

    Args:
        frame: The frame on which the rectangles are to be drawn.
        faces: The list of faces detected in the frame.

    Returns:
        None
    """

    new_faces = []  # To store the faces which are big enough

    # Display rectangles around the faces
    for i, (x, y, w, h) in enumerate(faces):
        if w > 50 and h > 50:  # Check if the face is big enough
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f"Face {i+1}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            new_faces.append((x, y, w, h))

    # Update the faces list with the faces which are big enough
    faces = np.array(new_faces)

    # Display the no. of faces detected on the frame
    cv2.putText(frame, f"No. of faces: {len(faces)}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)


def checkLineCrossing(faces, frame, frame_copy):
    """Check if any face crosses the line and display a warning.

    Args:
        faces: The list of faces detected in the frame.
        frame: The frame on which the warning is to be displayed.
        frame_copy: The copy of the frame from which the face is cropped.

    Returns:
        None
    """

    for (x, y, w, h) in faces:
        # Check if the face crossed the line
        if y < LINE_Y:
            cv2.putText(frame, "WARNING: Face crossed line!", (10, 720 - 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # ? Save the face image only if the time interval has passed
            global LAST_SAVE_TIME
            if time.time() - LAST_SAVE_TIME >= TIME_INTERVAL:
                saveImage(frame_copy, x, y, w, h, time.ctime())
                LAST_SAVE_TIME = time.time()


def displayImagesSideBySide(original_folder, canny_folder):
    """Display images side by side from the 'original' and 'canny' subfolders.

    Args:
        original_folder (str): Path to the 'original' subfolder.
        canny_folder (str): Path to the 'canny' subfolder.

    Returns:
        None
    """

    # Get the list of files in the 'original' folder
    original_files = os.listdir(original_folder)

    # Iterate through the files in the 'original' folder
    for original_file in original_files:

        # Construct the paths for the original and canny images
        original_path = os.path.join(original_folder, original_file)
        canny_file = original_file.replace('.jpg', '_canny.jpg')
        canny_path = os.path.join(canny_folder, canny_file)

        # Read the original and canny images
        original_image = cv2.imread(original_path)
        canny_image = cv2.imread(canny_path, cv2.IMREAD_GRAYSCALE)

        # Resize the canny image to match the original image dimensions
        canny_image = cv2.resize(
            canny_image, (original_image.shape[1], original_image.shape[0]))

        # Display the images side by side using matplotlib
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        plt.title('Original Image')

        plt.subplot(1, 2, 2)
        plt.imshow(canny_image, cmap='gray')
        plt.title('Canny Edge Detection')

        plt.show()


def main():

    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Set the resolution of the webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:

        ret, frame = cap.read()

        frame_copy = frame.copy()  # To save cropped face image without white line and rectangle

        # Draw a straight line at the top of the frame
        cv2.line(frame, pt1=(0, LINE_Y), pt2=(1280, LINE_Y),
                 color=(255, 255, 255), thickness=2)

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Load the cascade classifier
        face_cascade = cv2.CascadeClassifier(
            "../XML_Files/haarcascade_frontalface_default.xml")

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5)

        # Draw rectangles around the faces and display the no. of faces detected
        drawRectangles(frame, faces)

        # If any face crosses the line, display a warning
        checkLineCrossing(faces, frame, frame_copy)

        # Display the frame
        cv2.imshow("Face Recognition", frame)

        # Exit if "q" is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()  # Release the webcam
    cv2.destroyWindow("Face Recognition")  # Close the window
    cv2.waitKey(0)  # Wait for a key event to exit
    cv2.destroyAllWindows()  # Close all other windows

    print("Do you want to see the saved images (original) and (canny) side by side (y/n)?: ")
    choice = input()
    if choice in ["y", "Y"]:
        displayImagesSideBySide("./saved/original", "./saved/canny")
    else:
        print("Exiting...")


if __name__ == "__main__":
    main()
