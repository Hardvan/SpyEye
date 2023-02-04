import cv2
import numpy as np

# Load the cascade classifier
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Create a face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()


# Load the face samples
faces, labels = [], []

# Map the labels to the names of the people
names = {1: "Hardik", 2: "Karan", 3: "Abhishek",
         4: "Akshaja", 5: "Harsha", 6: "Aditya",
         7: "Gokul", 8: "Rohith", 9: "Jayanth"}

for i in range(1, 1+1):  # ? Change the range to the number of people you want to recognize
    face = cv2.imread(f'./images/face{i}.jpeg', 0)

    faces.append(face)
    labels.append(i)

face_recognizer.train(faces, np.array(labels))

# Open the webcam
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5)

    # Predict the label of each face
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(face)

        # Display the name of the person on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        name = names[label]
        cv2.putText(frame, f'Person {name} ({confidence:.2f}%)', (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the number of faces detected on the frame
    count = len(faces)
    cv2.putText(frame, f'Number of faces: {count}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
