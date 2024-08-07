# SpyEye: Real-time Face Detection & Intrusion Alert System using Meta API & SMTP

This program leverages OpenCV to perform real-time face detection via the webcam. Upon detecting a face, it outlines the face with a rectangle and counts the number of faces within the frame. Additionally, it draws a line at the top of the frame and issues a warning message when a face crosses this line. The system saves a cropped image of the detected face, timestamped, in a designated "saved" folder. Furthermore, it provides the capability to display these saved images in a separate window.

## Demonstration Video

[![SpyEye Demo Video](./demo/thumbnail.png)](https://youtu.be/vapcstpVHJY)

## Requirements

- OpenCV
- NumPy
- datetime
- os
- threading

## Files

- **intruder_det.py**: The main Python script that runs the face recognition with intruder detection.
- **whatsapp_message.py**: A Python script that sends a WhatsApp message to a specified number.
- **haarcascade_frontalface_default.xml**: A pre-trained Haar Cascade classifier for face detection.

## Notes

- The program uses the Haar Cascade Classifier to detect faces. The classifier XML file is stored in the "XML_Files" folder.
- The program displays a warning message when a face crosses the line. The line is drawn at 200 pixels from the top of the frame and can be changed by modifying the `line_y` variable.
- The program saves the detected faces to a folder named "saved". The folder can be changed by modifying the `saveImage()` function.
- The problem of the video feed lagging behind the face detection is solved by using a separate thread to send the WhatsApp message. The thread is created in the `ThreadSendMessage()` function.

## How to Contribute

1. Fork the repository
2. Clone the repository to your local machine

   ```bash
   git clone <url>
   ```

3. Create a python virtual environment

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment

   ```bash
    .venv\Scripts\activate
   ```

5. Install the requirements

   ```bash
   pip install -r requirements.txt
   ```

   To see the program execution:

   ```bash
   cd Main
   python intruder_det.py
   ```

6. Create a new branch

   ```bash
    git checkout -b <branch-name>
   ```

7. Make your changes

8. Commit and push your changes

   ```bash
   git add .
   git commit -m "<message>"
   git push origin <branch-name>
   ```

9. Create a pull request
