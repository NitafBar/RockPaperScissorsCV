# Rock Paper Scissors - Hand Gesture Recognition (Computer Vision)

A webcam based rock paper scissors game featuring hand gesture recognition (computer vision) using OpenCV and Google's MediaPipe.

## Features
- Hand tracking and gesture detection
- Play against the computer with random selection
- Live score tracking
- Visual countdown before each round

## Requirements
- Python
- A Webcam

## How to Install
```bash
pip install opencv-python mediapipe
```

## How to Play
Run the game:
```bash
python RockPaperScissorssCV.py
```

Make hand gestures in front of your webcam:
- **Rock**: Closed fist
- **Paper**: Open hand
- **Scissors**: Index and middle fingers extended

## How to Exit
Press 'q' to quit.

## How It Works
The game uses OpenCV to access the webcam and handles image processing and display. Then, MediaPipe's hand tracking model is used to detect hand landmarks and classify gestures based on finger positions. When a valid gesture is detected, a 3 second countdown begins before the computer makes its move.
