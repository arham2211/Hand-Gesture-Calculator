# Hand Gesture Calculator

## Overview

The **Hand Gesture Calculator** is an interactive application that uses hand gestures to operate a virtual calculator. The application leverages the MediaPipe library to detect hand landmarks and OpenCV for real-time video processing, allowing users to perform basic arithmetic operations through hand gestures.

## Features

- **Hand Gesture Recognition**: Uses MediaPipe to track hand landmarks and detect gestures.
- **Virtual Calculator**: Displays a calculator interface on the screen with buttons for numbers and arithmetic operations.
- **Gesture-Based Input**: Allows users to interact with the calculator using thumb and index finger gestures.

## How It Works

1. **Hand Detection**: The application captures video from the webcam and detects hand landmarks using MediaPipe.
2. **Gesture Detection**: When the thumb and index finger are close together, the application checks if they are over any calculator buttons.
3. **Button Interaction**: If the gesture corresponds to a button on the calculator, it performs the associated action (e.g., number entry, arithmetic operations, or clearing the input).
4. **Display Results**: The calculator updates and displays the result of arithmetic operations in real-time.

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- `math` library (standard Python library)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/hand-gesture-calculator.git
   cd hand-gesture-calculator
   ```

2. Install the required Python packages:

   ```bash
   pip install opencv-python mediapipe
   ```

## Usage

1. Run the main script:

   ```bash
   python calculator.py
   ```

2. The application will open a window showing the live video feed from your webcam.
3. Interact with the virtual calculator by moving your right hand and using thumb and index finger gestures to press the calculator buttons.
