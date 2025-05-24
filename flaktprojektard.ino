#include <Servo.h>  // Inkluderar biblioteket för att kunna styra servomotorer

Servo servoX;       // Skapar ett Servo-objekt för rörelse i X-led (vänster-höger)
Servo servoY;       // Skapar ett Servo-objekt för rörelse i Y-led (upp-ner)
String inputString = "";  // En sträng som lagrar inkommande data från datorn (ex. "320,240")

void setup() {
  Serial.begin(115200);          // Startar seriell kommunikation med 115200 baud
  Serial.setTimeout(10);         // Väntar max 10 ms på att läsa färdigt en sträng
  servoX.attach(9);              // Kopplar servoX till pinne 9 på Arduino
  servoY.attach(10);             // Kopplar servoY till pinne 10 på Arduino
}

void loop() {
  if (Serial.available()) {                             // Om det finns data tillgänglig att läsa från datorn
    inputString = Serial.readStringUntil('\n');         // Läs hela strängen tills ett radslut (newline '\n') kommer

    int commaIndex = inputString.indexOf(',');          // Hitta index för kommatecknet i strängen
    if (commaIndex > 0) {                               // Om ett kommatecken hittas (giltig sträng)

      int x = inputString.substring(0, commaIndex).toInt();         // Plocka ut X-värdet (innan kommatecknet)
      int y = inputString.substring(commaIndex + 1).toInt();        // Plocka ut Y-värdet (efter kommatecknet)

      x = map(x, 0, 640, 0, 180);    // Konvertera X från kamerans bredd (0–640) till servons vinkel (0–180)
      y = map(y, 0, 480, 0, 180);    // Konvertera Y från kamerans höjd (0–480) till servons vinkel (0–180)

      x = constrain(x, 0, 180);      // Se till att X håller sig inom gränsen 0–180
      y = constrain(y, 0, 180);      // Se till att Y håller sig inom gränsen 0–180

      servoX.write(x);              // Skriv vinkeln till servoX (rotera servon till den vinkeln)
      servoY.write(y);              // Skriv vinkeln till servoY
    }

    inputString = "";               // Töm strängen så att nästa värde kan tas emot korrekt
  }
}
