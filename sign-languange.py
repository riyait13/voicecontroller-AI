import cv2
import pytesseract
import time

#  Set path to tesseract executable (change this to match your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def singh_translator(text):
    words = text.split()
    translated_words = [word + " Singh" for word in words]
    return ' '.join(translated_words)

# for  Opening webcamq
cap = cv2.VideoCapture(0)

# Set the resolution of the webcam feed
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Press 'q' to quit.")

ret, prev_frame = cap.read()
if not ret:
    print("Failed to grab initial frame from webcam.")
    cap.release()
    exit()

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
singh1_text = ""
last_movement_time = 0
display_duration = 2  # seconds to display translation

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame from webcam.")
        break

    #  Convert frame to gray for better OCR
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(prev_gray, gray)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    movement = cv2.countNonZero(thresh)

    current_time = time.time()
    if movement > 1000:  # Movement detected
        #  OCR it!
        text = pytesseract.image_to_string(gray, lang='eng')
        print(f"OCR Text: {text}")  # Debug print

        #  Translate to Singn Language
        singh1_text = singh_translator(text)
        prev_gray = gray.copy()
        last_movement_time = current_time

    # Only display translation for a set duration after movement
    if current_time - last_movement_time > display_duration:
        singh1_text = ""

    #  Show on screen
    cv2.putText(frame, singh1_text[:100], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Singh Translator AI", frame)

    # Slow down the loop (adjust as needed)
    time.sleep(0.5)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
