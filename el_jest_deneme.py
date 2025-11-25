import cv2
import mediapipe as mp

# MediaPipe modülleri
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Kamerayı aç
cap = cv2.VideoCapture(0)  # Eğer çalışmazsa 0 yerine 1 deneyebilirsin

if not cap.isOpened():
    print("Kamera açılamadı! Başka bir program kamerayı kullanıyor olabilir.")
    exit()

# MediaPipe Hands modelini başlat
with mp_hands.Hands(
        max_num_hands=2,             # En fazla 2 el
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Frame alınamadı, kamera bağlantısı koptu.")
            break

        # --- AYNA (MIRROR) MODU ---
        # 1: Yatay eksende çevir (ayna efekti)
        frame = cv2.flip(frame, 1)

        # BGR -> RGB (MediaPipe RGB bekliyor)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # El tespiti
        results = hands.process(image)

        # Tekrar RGB -> BGR (OpenCV için)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Eğer el bulunduysa landmarkları çiz
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("El Tespiti (Ayna Modu)", image)

        # q'ya basınca çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
