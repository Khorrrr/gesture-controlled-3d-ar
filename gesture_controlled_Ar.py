import cv2
import mediapipe as mp
import threading
import time
import math
from ursina import *


def detect_gesture(hand_landmarks):
    """
    Analyzes landmarks to return: 'FIST', 'OPEN', or 'OTHER'
    """
 
    tips = [8, 12, 16, 20]      
    pips = [6, 10, 14, 18]      

    fingers_up = 0


    for i in range(4):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[pips[i]].y:
            fingers_up += 1

    
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers_up += 1

    # Determine Gesture
    if fingers_up == 0:
        return "FIST"
    elif fingers_up >= 4:
        return "OPEN"
    else:
        return "OTHER"



class CameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        
        # Shared Variables
        self.hand_x = 0.5
        self.hand_y = 0.5
        self.current_gesture = "OPEN" 
        
        # OpenCV Setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

    def run(self):
        print("[Camera Thread] Started...")
        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue

            # Mirror and Process
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            # Default skeleton color 
            skeleton_color = (0, 255, 0)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # 1. Update Position
                index_tip = hand_landmarks.landmark[8]
                self.hand_x = index_tip.x
                self.hand_y = index_tip.y

                # 2. Detect Gesture
                self.current_gesture = detect_gesture(hand_landmarks)

                # 3. Visual Feedback on Skeleton Color
                if self.current_gesture == "FIST":
                    skeleton_color = (0, 0, 255)
                elif self.current_gesture == "OPEN":
                    skeleton_color = (0, 255, 0) 
                else:
                    skeleton_color = (255, 0, 255)

                # Draw Skeleton with specific color
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=skeleton_color, thickness=2, circle_radius=2),
                    connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=skeleton_color, thickness=2)
                )

            # Add text to Camera Window
            cv2.putText(frame, f"Mode: {self.current_gesture}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow("Camera Input", frame)
            
            if cv2.waitKey(1) & 0xFF == 27:
                self.running = False
        
        self.cap.release()
        cv2.destroyAllWindows()



# Start the camera thread
camera_thread = CameraThread()
camera_thread.start()

app = Ursina()
window.title = "Gesture Controlled 3D Cube"
window.color = color.black
window.position = (600, 100) 


cube = Entity(
    model='cube',
    color=color.azure,
    texture='white_cube',
    scale=2,
    position=(0, 0, 0),
    rotation=(0,0,0)
)

mode_text = Text(
    text="Mode: ROTATE (Open Hand)",
    position=(0, 0.45),
    origin=(0,0),
    scale=2,
    color=color.white
)

instruction_text = Text(
    text="[Open Hand] to Rotate | [Fist] to Change Color",
    position=(0, -0.45),
    origin=(0,0),
    scale=1,
    color=color.light_gray
)


prev_hand_x = 0.5
prev_hand_y = 0.5

rot_vel_y = 0
rot_vel_x = 0

FRICTION = 0.96
SNAP_THRESHOLD = 3.0

def update():
    global prev_hand_x, prev_hand_y, rot_vel_y, rot_vel_x
    
    # 1. Read Shared Data
    hx = camera_thread.hand_x
    hy = camera_thread.hand_y
    gesture = camera_thread.current_gesture

    # 2. Hand Velocity (Flick detection)
    hand_vel_x = (hx - prev_hand_x) * 2000
    hand_vel_y = (hy - prev_hand_y) * 2000
    
    prev_hand_x = hx
    prev_hand_y = hy

    if gesture == "FIST":
        mode_text.text = "MODE: COLOR CYCLE (Fist)"
        mode_text.color = color.red
        
        rot_vel_y = 0
        rot_vel_x = 0
        
        hue = (time.time() * 50) % 360
        cube.color = color.hsv(hue, 0.8, 0.8)
        
        cube.rotation_y += 1
        
    else:
        mode_text.text = "MODE: PHYSICS ROTATE (Open Hand)"
        mode_text.color = color.green
        
        cube.color = color.azure

        target_y = (hx - 0.5) * 360
        target_x = (hy - 0.5) * 360 * -1

        if abs(hand_vel_x) > 10 or abs(hand_vel_y) > 10:
            rot_vel_y += hand_vel_x * time.dt
            rot_vel_x += hand_vel_y * time.dt
        else:
            cube.rotation_y = lerp(cube.rotation_y, target_y, 0.1)
            cube.rotation_x = lerp(cube.rotation_x, target_x, 0.1)
            rot_vel_y = 0
            rot_vel_x = 0

        if abs(rot_vel_y) > 0.1 or abs(rot_vel_x) > 0.1:
            cube.rotation_y += rot_vel_y * time.dt
            cube.rotation_x += rot_vel_x * time.dt
            rot_vel_y *= FRICTION
            rot_vel_x *= FRICTION
            
            # Snap Logic
            if abs(rot_vel_y) < SNAP_THRESHOLD:
                snapped_y = round(cube.rotation_y / 90) * 90
                cube.rotation_y = lerp(cube.rotation_y, snapped_y, 0.1)

    if held_keys['escape']:
        camera_thread.running = False
        application.quit()

app.run()