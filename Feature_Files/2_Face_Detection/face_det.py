# Run this code by cd-ing to Face_Detection and running the following command:
# py face_det.py

import cv2


def detectFaces(image):
    """Detects faces in an image.

    Returns:
        A list of tuples containing the coordinates of the faces.
    """

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5)

    return faces


# Load the cascade classifier
face_cascade = cv2.CascadeClassifier(
    '../XML_Files/haarcascade_frontalface_default.xml')


# Initialize the camera
cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()

    faces = detectFaces(frame)

    # Draw a rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h),
                      color=(255, 0, 0), thickness=2)

    # Display the number of faces detected on the frame
    count = len(faces)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f'Number of faces: {count}',
                (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
