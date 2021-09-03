char incoming_value = 0;
int val = 0;
int analogPin = A5;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  

  for(byte i = 0; i<2 ;i ++){
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);                       // wait for a second
  }  
}

// the loop function runs over and over again forever
void loop() {
  if(Serial.available() > 0){
    incoming_value = Serial.read();
    Serial.println(incoming_value);
    if( incoming_value == '1' ){
      digitalWrite(13, HIGH );
      val = analogRead(analogPin);  // read the input pin
      Serial.println(val);
    }
    else if (incoming_value == '0' )
      digitalWrite(13, LOW );
  }
  
}
