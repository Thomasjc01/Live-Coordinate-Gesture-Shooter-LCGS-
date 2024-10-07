import cv2
import mediapipe as mp

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize hand detection model
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

# Initialize camera
cap = cv2.VideoCapture(1)

# Load the target image
while True:
    ret,original_target=cap.read()
    break

cap=cv2.VideoCapture(0)
def are_all_fingers_open(hand_landmarks, frame_shape):
    # Get landmarks
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    # Convert to pixel coordinates
    thumb_tip_y = int(thumb_tip.y * frame_shape[0])
    thumb_ip_y = int(thumb_ip.y * frame_shape[0])
    index_tip_y = int(index_tip.y * frame_shape[0])
    index_pip_y = int(index_pip.y * frame_shape[0])
    middle_tip_y = int(middle_tip.y * frame_shape[0])
    middle_pip_y = int(middle_pip.y * frame_shape[0])
    ring_tip_y = int(ring_tip.y * frame_shape[0])
    ring_pip_y = int(ring_pip.y * frame_shape[0])
    pinky_tip_y = int(pinky_tip.y * frame_shape[0])
    pinky_pip_y = int(pinky_pip.y * frame_shape[0])

    # Check if all fingertips are above the PIP joints
    all_fingers_open = all([
        thumb_tip_y < thumb_ip_y,
        index_tip_y < index_pip_y,
        middle_tip_y < middle_pip_y,
        ring_tip_y < ring_pip_y,
        pinky_tip_y < pinky_pip_y
    ])

    return all_fingers_open

def is_index_finger_raised(hand_landmarks, frame_shape):
    # Get fingertip landmarks
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # Convert to pixel coordinates
    thumb_tip_y = int(thumb_tip.y * frame_shape[0])
    index_tip_y = int(index_tip.y * frame_shape[0])
    middle_tip_y = int(middle_tip.y * frame_shape[0])
    ring_tip_y = int(ring_tip.y * frame_shape[0])
    pinky_tip_y = int(pinky_tip.y * frame_shape[0])

    # Check if index finger is raised
    index_raised = index_tip_y < min(thumb_tip_y, middle_tip_y, ring_tip_y, pinky_tip_y)
    
    # Check if other fingers are in a closed position
    fingers_closed = all([
        (index_tip_y < thumb_tip_y) and (thumb_tip_y - index_tip_y > 50),  # Index above thumb
        index_tip_y < middle_tip_y,  # Index above middle
        index_tip_y < ring_tip_y,    # Index above ring
        index_tip_y < pinky_tip_y    # Index above pinky
    ])
    
    return index_raised and fingers_closed

# Get the dimensions of the target image
ret, frame = cap.read()

if not ret:
    print("Failed to read from the camera")
    cap.release()
    exit()

h, w = frame.shape[:2]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Copy the original target image
    target = cv2.resize(original_target, (w, h))

    # Draw hand landmarks and connections
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_tip_x = int(thumb_tip.x * frame.shape[1])
            thumb_tip_y = int(thumb_tip.y * frame.shape[0])

            if are_all_fingers_open(hand_landmarks, frame.shape):
                # Draw a circle on the thumb tip
                circle_radius = 20
                cv2.circle(frame, (thumb_tip_x, thumb_tip_y), circle_radius, (0, 255, 0), 2)
                cv2.circle(target, (thumb_tip_x, thumb_tip_y), circle_radius, (0, 255, 0), 2)
                break
            elif is_index_finger_raised(hand_landmarks, frame.shape):
                # Draw a cross on the thumb tip
                cross_size = 20
                cv2.line(frame, (thumb_tip_x - cross_size, thumb_tip_y), (thumb_tip_x + cross_size, thumb_tip_y), (0, 255, 0), 2)
                cv2.line(frame, (thumb_tip_x, thumb_tip_y - cross_size), (thumb_tip_x, thumb_tip_y + cross_size), (0, 255, 0), 2)
                cv2.line(target, (thumb_tip_x - cross_size, thumb_tip_y), (thumb_tip_x + cross_size, thumb_tip_y), (0, 255, 0), 2)
                cv2.line(target, (thumb_tip_x, thumb_tip_y - cross_size), (thumb_tip_x, thumb_tip_y + cross_size), (0, 255, 0), 2)

            # Draw hand landmarks and connections
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the resulting frame
    cv2.imshow('Hand Detection', frame)
    cv2.imshow("TARGET", target)
    
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
