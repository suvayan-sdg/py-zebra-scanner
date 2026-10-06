import cv2
import time
from pyzbar.pyzbar import decode, ZBarSymbol
from pynput.keyboard import Controller, Key

keyboard = Controller()
TYPING_DELAY = 0.01

last_value = None
qr_visible_last_frame = False
frame_count = 0

def send_as_keyboard(value):
    print("\n" + "=" * 60)
    print("⌨️ TYPING INITIATED...")

    try:
        for char in value:
            keyboard.type(char)
            time.sleep(TYPING_DELAY)

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        print("✅ ENTER sent.")
        print("=" * 60)

    except Exception as error:
        print(f"❌ Keyboard input error: {error}")

# macOS camera
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    raise SystemExit

print("=" * 60)
print("ZEBRA SCANNER EMULATOR STARTED")
print("=" * 60)

while True:
    ret, frame = cap.read()

    if not ret:
        print("WARNING: Camera frame could not be read.")
        time.sleep(0.1)
        continue

    frame_count += 1
    if frame_count % 60 == 0:
        h, w = frame.shape[:2]
        print(f"... scanning (frame {frame_count}, {w}x{h}, mean brightness {frame.mean():.0f})")

    # zbar wants grayscale; decoding the raw BGR frame only reads the blue
    # channel, which hurts contrast and makes some QR codes undetectable.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode only QR codes
    decoded_objects = decode(gray, symbols=[ZBarSymbol.QRCODE])
    qr_visible_now = len(decoded_objects) > 0

    for obj in decoded_objects:
        try:
            value = obj.data.decode("utf-8")
        except UnicodeDecodeError:
            continue

        should_scan = (value != last_value or not qr_visible_last_frame)

        if should_scan:
            # --- STEP 1: VERIFY DETECTION ---
            print(f"\n🎯 QR CAPTURED: {value}")
            last_value = value

            # --- STEP 2: PAUSE FOR WINDOW FOCUS ---
            print("⏳ You have 3 seconds to click into your target text field...")
            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)

            # --- STEP 3: TYPE ---
            send_as_keyboard(value)

        # Draw QR rectangle
        x, y, w, h = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    qr_visible_last_frame = qr_visible_now

    cv2.imshow("Zebra Scanner Emulator - Press Q to Quit", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Scanner stopped.")
