import cv2                # OpenCV för bildbehandling
import serial             # För seriell kommunikation med Arduino
import time               # För att kunna lägga till pauser

# Välj rätt COM-port för Arduino och starta seriell kommunikation
arduino = serial.Serial('COM12', 115200, timeout=0.1)
time.sleep(2)  # Vänta 2 sekunder så att anslutningen stabiliseras

# Sätt storleken på kamerabilden (måste matcha Arduino-koden)
frame_width = 640
frame_height = 480

# Starta webbkameran (0 = första tillgängliga kameran)
cap = cv2.VideoCapture(0)
cap.set(3, frame_width)   # Bredd på videobilden
cap.set(4, frame_height)  # Höjd på videobilden

# Ladda in Haar Cascade-modellen för ansiktsdetektering
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Variabler för att spara tidigare skickade positioner
last_x = None
last_y = None
threshold = 10  # Endast skicka ny data om förändringen är större än detta

# Funktion som skickar X och Y till Arduino via serieport
def send_position(x_center, y_center):
    global last_x, last_y
    # Kontrollera om positionen har förändrats tillräckligt mycket
    if last_x is None or abs(x_center - last_x) > threshold or abs(y_center - last_y) > threshold:
        data = f"{x_center},{y_center}\n"       # Skapa sträng i formatet "x,y\n"
        arduino.write(data.encode('utf-8'))     # Skicka till Arduino som byte-sträng
        print(f"[Python] Skickar: {data.strip()}")  # Skriv ut vad som skickas
        last_x = x_center
        last_y = y_center

# Huvudloopen som körs så länge kameran är igång
while True:
    ret, frame = cap.read()  # Läs en bildruta från kameran
    if not ret:
        print("Kunde inte läsa från kameran")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Konvertera bilden till gråskala
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)  # Detektera ansikten

    for (x, y, w, h) in faces:
        cx = x + w // 2  # Beräkna mittpunkten (X) av ansiktet
        cy = y + h // 2  # Beräkna mittpunkten (Y) av ansiktet

        # Rita rektangel och mittpunkt på ansiktet i videon
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

        send_position(cx, cy)  # Skicka koordinaterna till Arduino
        break  # Skicka bara första ansiktet

    # Visa videon med markerat ansikte
    cv2.imshow("Face Tracking", frame)

    # Avsluta programmet om användaren trycker på "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stäng allt när loopen avslutas
cap.release()             # Släpp kameran
cv2.destroyAllWindows()   # Stäng fönstret
arduino.close()           # Stäng seriell anslutning
