import cv2
import mediapipe as mp
import random
import time

# Initialise Mediapipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Possible gesture choices for the computer
possible_gestures = ["Rock", "Paper", "Scissors"]

# Store gestures outside the main while loop
gesture_computer = ""
previous_gesture = ""
countdown_active = False
countdown_start_time = None
elapsed_time = 0
your_score = 0
computer_score = 0
start_scoring = True
score_result = ""

# Start webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    gesture = ""
    cv2.putText(frame, "You: " + str(your_score), (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(frame, "Computer: " + str(computer_score), (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    # Clear the score result text when no hand is detected
    if not results.multi_hand_landmarks:
        score_result = ""
        previous_gesture = ""

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmarks of fingers
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            pinky_tip = hand_landmarks.landmark[20]

            index_centre = hand_landmarks.landmark[5]
            middle_centre = hand_landmarks.landmark[9]
            ring_centre = hand_landmarks.landmark[13]
            pinky_centre = hand_landmarks.landmark[17]

            # Compute gestureqwqqq
            if index_tip.y > index_centre.y and middle_tip.y > middle_centre.y and ring_tip.y > ring_centre.y and pinky_tip.y > pinky_centre.y:
                gesture = "Rock"
            elif index_tip.y < index_centre.y and middle_tip.y < middle_centre.y and ring_tip.y < ring_centre.y and pinky_tip.y < pinky_centre.y:
                gesture = "Paper"
            elif index_tip.y < index_centre.y and middle_tip.y < middle_centre.y:
                gesture = "Scissors"
            else:
                gesture = ""

    # Display the detected gesture on screen
    if gesture != "":
        cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Computer plays
    if (gesture == "Rock" or gesture == "Paper" or gesture == "Scissors") and gesture != previous_gesture and not countdown_active:
        countdown_active = True
        countdown_start_time = time.time()
        previous_gesture = gesture
        gesture_computer = ""

    # Countdown for 3,2,1 text. This works since it's in the while loop and the elapsed time gets checked every frame
    if countdown_active:
        elapsed_time = time.time() - countdown_start_time

        if elapsed_time < 1 and gesture != "":
            cv2.putText(frame, "3", (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif elapsed_time < 2 and gesture != "":
            cv2.putText(frame, "2", (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif elapsed_time < 3 and gesture != "":
            cv2.putText(frame, "1", (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            if gesture_computer == "":
                gesture_computer = random.choice(possible_gestures)
            if gesture != "":
                cv2.putText(frame, gesture_computer, (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Scoring
        # Ties
        if (gesture == gesture_computer) and (gesture != "" and gesture_computer != "") and start_scoring:
            score_result = "Tie!"
            start_scoring = False
        # Winning
        elif gesture == "Rock" and gesture_computer == "Scissors" and start_scoring:
            score_result = "Win!"
            your_score += 1
            start_scoring = False
        elif gesture == "Paper" and gesture_computer == "Rock" and start_scoring:
            score_result = "Win!"
            your_score += 1
            start_scoring = False
        elif gesture == "Scissors" and gesture_computer == "Paper" and start_scoring:
            score_result = "Win!"
            your_score += 1
            start_scoring = False
        # Losing
        elif gesture == "Rock" and gesture_computer == "Paper" and start_scoring:
            score_result = "Lose!"
            computer_score += 1
            start_scoring = False
        elif gesture == "Paper" and gesture_computer == "Scissors" and start_scoring:
            score_result = "Lose!"
            computer_score += 1
            start_scoring = False
        elif gesture == "Scissors" and gesture_computer == "Rock" and start_scoring:
            score_result = "Lose!"
            computer_score += 1
            start_scoring = False

        cv2.putText(frame, score_result, (500, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Restart the countdown and therefore the computer's turn when you change gestures
    if gesture != previous_gesture and gesture != "":
        countdown_active = False
        start_scoring = True


    cv2.imshow("Rock Paper Scissors", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
