int plant0 = 8;
int plant0Humidity = 0;

void setup() {
  pinMode(8, INPUT);
  Serial.begin(9600);
  while (!Serial) {
  }
  establishContact();
}

void loop() {
  while (Serial.available() > 0) {
    plant0Humidity = analogRead(plant0);
    Serial.println(plant0Humidity);
    delay(1000);
  }
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');
    delay(300);
  }
}
