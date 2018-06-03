int plant0 = 8;

void setup() {
    Serial.begin(9600);
}

void loop() {
}

void serialEvent() {
    plant0 = Serial.parseInt();
    pinMode(plant0, INPUT);
    Serial.println((int) analogRead(plant0));
}
