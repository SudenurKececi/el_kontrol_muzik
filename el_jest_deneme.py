import cv2
import mediapipe as mp
import time

try:
    import pyautogui  # klavye/medya tuşları için
    HAVE_PYAUTOGUI = True
except ImportError:
    print("Uyarı: pyautogui bulunamadı, sadece terminale yazı yazılacak.")
    HAVE_PYAUTOGUI = False

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# ---------------------- Parmak durumu fonksiyonu ---------------------- #
def finger_states(hand_landmarks, hand_label, img_w, img_h):
    """
    True = parmak havada, False = aşağıda
    Sadece işaret ve baş parmak kontrol ediyoruz.
    """
    landmarks = hand_landmarks.landmark

    def px(i):
        return landmarks[i].x * img_w, landmarks[i].y * img_h

    # İşaret parmağı: 8 (uç), 6 (alt boğum)
    ix_tip_x, ix_tip_y = px(8)
    ix_pip_x, ix_pip_y = px(6)
    is_index_up = ix_tip_y < ix_pip_y  # uç daha yukarıdaysa havada

    # Baş parmak: 4 (uç), 2 (alt boğum)
    th_tip_x, th_tip_y = px(4)
    th_mcp_x, th_mcp_y = px(2)

    # Sağ elde başparmak sağa doğru açılıyor, solda sola doğru
    if hand_label == "Right":
        is_thumb_up = th_tip_x > th_mcp_x + 10  # +10 küçük tolerans
    else:  # "Left"
        is_thumb_up = th_tip_x < th_mcp_x - 10

    return is_index_up, is_thumb_up


# ---------------------- Aksiyon fonksiyonu ---------------------- #
last_action_time = 0
last_action_label = ""
cooldown = 1.0  # aynı komutu 1 saniyeden sık göndermesin


def trigger_action(label):
    global last_action_time, last_action_label

    now = time.time()
    if now - last_action_time < cooldown:
        return  # çok sık tetiklenmesin

    last_action_time = now
    last_action_label = label
    print(f">>> {label}")

    if not HAVE_PYAUTOGUI:
        return

    try:
        if label == "SES ARTTIR":
            pyautogui.press("volumeup")
        elif label == "SES AZALT":
            pyautogui.press("volumedown")
        elif label == "SONRAKI ŞARKI":
            pyautogui.press("nexttrack")
        elif label == "ÖNCEKI ŞARKI":
            pyautogui.press("prevtrack")
    except Exception as e:
        # Her ihtimale karşı hata programı bozmasın
        print("pyautogui hatası:", e)


# ---------------------- Kamera ---------------------- #
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame alınamadı.")
            break

        h, w, _ = frame.shape

        # Mediapipe RGB ister
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        # Çizimleri yapmak için kopya
        image = frame.copy()

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):
                hand_label = handedness.classification[0].label  # "Right" / "Left"

                # Noktaları çiz
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                # Parmakların durumu
                index_up, thumb_up = finger_states(
                    hand_landmarks, hand_label, w, h
                )

                # Debug için ekrana yaz
                y_text = 30 if hand_label == "Right" else 60
                text = f"{hand_label} I:{index_up} T:{thumb_up}"
                cv2.putText(
                    image, text, (10, y_text),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
                )

                # --------- Jest -> Komut eşleştirme --------- #
                if hand_label == "Right":
                    # Sağ el işaret parmağı havada → SES ARTTIR
                    if index_up and not thumb_up:
                        trigger_action("SES ARTTIR")

                    # Sağ el baş parmak havada → SES AZALT
                    elif thumb_up and not index_up:
                        trigger_action("SES AZALT")

                elif hand_label == "Left":
                    # Sol el işaret parmağı havada → SONRAKİ ŞARKI
                    if index_up and not thumb_up:
                        trigger_action("SONRAKI ŞARKI")

                    # Sol el baş parmak havada → ÖNCEKİ ŞARKI
                    elif thumb_up and not index_up:
                        trigger_action("ÖNCEKI ŞARKI")

        # Son yapılan aksiyonu ekranda kısa süre göster
        if last_action_label and time.time() - last_action_time < 1.2:
            cv2.putText(
                image,
                last_action_label,
                (50, h - 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 0, 255),
                3
            )

        # --------- AYNA MODU: görüntüyü yatay çevir --------- #
        display = cv2.flip(image, 1)

        cv2.imshow("Jest Kontrol (Ayna)", display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
