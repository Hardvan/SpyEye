import cv2
import numpy as np
import time
from datetime import datetime
import os

# Load the cascade classifier
face_cascade = cv2.CascadeClassifier(
    "../XML_Files/haarcascade_frontalface_default.xml")

# Iterate through the images in saved folder and delete them
# Set to False if you don't want to delete the images in saved folder
delete_saved_images = True

if delete_saved_images:
    for file in os.listdir("./saved"):
        os.remove(f"./saved/{file}")


def saveImage(frame, x, y, w, h, time):
    """Save the face image with the time on the bottom of the image.
    """

    # Crop the face from the frame
    face = frame[y-100:y+h+100, x-100:x+w+100]  # 100 pixels extra on each side

    # Write the time on the bottom of face image and save it
    face = cv2.putText(face, time, (10, y+h-60), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 255, 255), 2, cv2.LINE_AA)

    # Convert the current time to a string
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Save the face image
    try:
        cv2.imwrite(f"./saved/face_{current_time}.jpg", face)
    except:
        pass


def drawRectangles(frame, faces):
    """Display rectangles around the faces and the number of faces detected on the frame.

    Args:
        frame: The frame on which the rectangles are to be drawn.
        faces: The list of faces detected in the frame.
    """

    # Display rectangles around the faces
    for i, (x, y, w, h) in enumerate(faces):

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, f"Face {i+1}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the number of faces detected on the frame
    cv2.putText(frame, f"Number of faces: {len(faces)}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)


def checkLineCrossing(faces, frame, line_y):
    """Check if any face crosses the line and display a warning.
    """

    for (x, y, w, h) in faces:

        # Check if the face crossed the line
        if y < line_y:
            cv2.putText(frame, "WARNING: Face crossed line!", (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            saveImage(frame, x, y, w, h, time.ctime())


# Open the webcam
cap = cv2.VideoCapture(0)

# Set the resolution of the webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Intruder detection line (200 pixels from the top)
line_y = 200

while True:

    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Draw a straight line at the top of the frame
    cv2.line(frame, pt1=(0, line_y), pt2=(1280, line_y),
             color=(255, 255, 255), thickness=2)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5)

    drawRectangles(frame, faces)

    # If any face crosses the line, display a warning
    checkLineCrossing(faces, frame, line_y)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
