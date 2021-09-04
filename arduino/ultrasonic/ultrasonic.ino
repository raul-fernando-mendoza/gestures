
#include <NewPing.h>

NewPing sonar( 10, 11, 100);

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
int previous_read = 0;
int new_read = 0;
void loop() {

      new_read = sonar.ping_cm();
      if( new_read != 0 && previous_read != new_read ){
        Serial.println(new_read);
        previous_read = new_read;
      }  
      
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(10);                       // wait for a second
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      delay(10);                       // wait for a second
  
}
