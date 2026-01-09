# Gesture Controlled 3D Cube

A 3D interactive application where you control a floating cube using hand gestures! Built with Python, Ursina Engine, MediaPipe, and OpenCV.

![Demo](https://github.com/Khorrrr/gesture-controlled-3d-ar/releases/download/v1.0.0/demo.gif)

## 🎮 Features

-   **Real-time Hand Tracking**: Uses MediaPipe to track your hand landmarks with high precision.
-   **Interactive 3D Graphics**: smooth 3D rendering powered by the Ursina Engine.
-   **Gesture Controls**:
    -   **🖐 Open Hand**: Rotate the cube. Move your hand to spin it, or "flick" to give it momentum with physics-based inertia.
    -   **✊ Fist**: Enter "Color Cycle" mode. The cube spins and cycles through vibrant colors.
-   **Physics & Feedback**: Includes friction, velocity, and snapping to nearest angles for a polished feel.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/gesture-controlled-cube.git
    cd gesture-controlled-cube
    ```

2.  **Create a virtual environment (Optional but Recommended)**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

1.  Run the application:
    ```bash
    python gesture_controlled_Ar_d.py
    ```

2.  **Controls**:
    -   Show your hand to the camera.
    -   **Move Open Hand**: Rotates the cube.
    -   **Make a Fist**: Changes cube color and spins it.
    -   **ESC**: Quit the application.

## 🔧 Technologies Used

-   [Ursina Engine](https://www.ursinaengine.org/) - For 3D rendering.
-   [MediaPipe](https://developers.google.com/mediapipe) - For hand tracking.
-   [OpenCV](https://opencv.org/) - For camera input processing.

## 📝 Requirements

-   Python 3.x
-   Webcam
