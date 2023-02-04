import cv2
import numpy as np


def getCameraChoice():
    """Get camera choice from user and return VideoCapture object

    Returns:
        cap: VideoCapture object
    """

    print("Which is your camera source?")
    print("1. Laptop Webcam")
    print("2. IP Camera")
    choice = int(input("Enter your choice: "))

    cap = None
    if choice == 1:
        # For Laptop Webcam
        cap = cv2.VideoCapture(0)

    elif choice == 2:
        # For IP Camera
        cap = cv2.VideoCapture(
            'rtsp://username:password@192.168.1.64/1')

    else:
        print("Invalid choice. Try again.")
        return getCameraChoice()

    return cap


# Get camera choice
cap = getCameraChoice()

# Infinite loop to continuously display frames
while (True):

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display frame in a window called "frame"
    cv2.imshow('frame', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
