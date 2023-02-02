import cv2

# Load the cascade classifier
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5)

    # Draw a rectangle around each face and count the number of faces detected
    count = 0
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

    # Display the number of faces detected on the frame
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
