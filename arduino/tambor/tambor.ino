int incomingByte = 0; // for incoming serial data

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  pinMode(13, OUTPUT );
}

void loop() {
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    if( incomingByte == 97 ){
      digitalWrite(13, HIGH); // sets the digital pin 13 on
      delay(100);            // waits for a second
      digitalWrite(13, LOW);  // sets the digital pin 13 off
    }
    // say what you got:
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);
  }
}
