import cv2
import mediapipe as mp
import pyautogui
import time

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)  # Kurangi beban komputasi

# Ambil ukuran layar
screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Balik horizontal agar seperti cermin
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Hitung jumlah jari yang diangkat
            finger_tips = [8, 12, 16, 20]  # Indeks titik ujung jari
            count = sum(1 for tip in finger_tips if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y)

            # Tentukan aksi berdasarkan jumlah jari yang diangkat
            if count == 1:
                pyautogui.press('up')
                print("Menekan tombol: UP")
            elif count == 2:
                pyautogui.press('down')
                print("Menekan tombol: DOWN")
            elif count == 3:
                pyautogui.press('right')
                print("Menekan tombol: RIGHT")
            elif count == 4:
                pyautogui.press('left')
                print("Menekan tombol: LEFT")
            elif count == 5:
                print("Tidak ada input")

            # Gambar landmark tangan
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Tracking", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
