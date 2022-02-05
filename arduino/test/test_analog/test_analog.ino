//My test arduion only works with A4 and A5

int a = 0;
double v = 0;
int pin = 0;
int analogPins[] = {A0,A1,A2,A3,A4,A5}; 

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
  for( int i=0; i<6;i++ ){
    pin = analogPins[i];
    a = analogRead(pin);  // read the input pin
    v = ((double)a * 5)/1024;
    Serial.print(pin, HEX);
    Serial.print(" ");
    Serial.print(a);
    Serial.print(" ");
    Serial.println(v);
    
  } 
  Serial.println("");
  delay(1000);
}
