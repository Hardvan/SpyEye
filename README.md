# Face Recognition

This program uses OpenCV to detect faces in real-time using the webcam. When a face is detected, the program displays a rectangle around the face and counts the number of faces in the frame. The program also draws a line at the top of the frame and displays a warning message when a face crosses the line. The program saves a cropped image of the detected face with a timestamp on it to a folder named "saved". The program can also display the saved images in a new window.

## Requirements

- OpenCV
- NumPy
- datetime
- os

## Files

- **main.py**: The main Python script that runs the face recognition with intruder detection.
- **haarcascade_frontalface_default.xml**: A pre-trained Haar Cascade classifier for face detection.
- **saved/**: A directory where the detected faces will be saved with a timestamp on them.

## Notes

- The program uses the Haar Cascade Classifier to detect faces. The classifier XML file is stored in the "XML_Files" folder.
- The program displays a warning message when a face crosses the line. The line is drawn at 200 pixels from the top of the frame and can be changed by modifying the `line_y` variable.
- The program saves the detected faces to a folder named "saved". The folder can be changed by modifying the `saveImage()` function.
