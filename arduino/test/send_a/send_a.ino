
// the setup function runs once when you press reset or power the board
void setup() {


  pinMode(LED_BUILTIN, OUTPUT);
  
  for(byte i = 0; i<3 ;i ++){
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);                       // wait for a second
  }    
  
  // initialize digital pin LED_BUILTIN as an output.
  Serial.begin(9600);  


}

// the loop function runs over and over again forever
void loop() {
      Serial.println("hola");
      
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(1000);                       // wait for a second
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      delay(1000);                       // wait for a second
  
}
