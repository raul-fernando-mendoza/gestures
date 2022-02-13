/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink
*/
#include <SoftwareSerial.h>

#define RX    -1   // *** D3, Pin 2
#define TX    4   // *** D4, Pin 3

#define PIN_OUT 1
#define PIN_INPUT 3
  
SoftwareSerial swsri(RX,TX);

// the setup function runs once when you press reset or power the board
void setup() {
  
  pinMode(PIN_OUT, OUTPUT);
  pinMode(PIN_INPUT, INPUT);
  
/*
  //clock speed to 1 MZ
  cli(); // Disable interrupts
  CLKPR = (1<<CLKPCE); // Prescaler enable
  CLKPR = ((1<<CLKPS1) | (1<<CLKPS0)); // Clock division factor 8 (0011)
  sei(); // Enable interrupts
*/
  for(int i=0;i<3;i++){
    digitalWrite(PIN_OUT, HIGH); // sets the digital pin 13 on
    delay(500);            // waits for a second
    digitalWrite(PIN_OUT, LOW);  // sets the digital pin 13 off
    delay(500);            // waits for a second
  }    
  swsri.begin(9600);
  swsri.print("AT+BAUD8\r\n");

  digitalWrite(PIN_OUT, HIGH); // sets the digital pin 13 on
  delay(3000);            // waits for a second  


 
}

// the loop function runs over and over again forever
void loop() {
  swsri.begin(115200);

  for(int i=0;i<3;i++){
    digitalWrite(PIN_OUT, HIGH); // sets the digital pin 13 on
    delay(1000);            // waits for a second
    digitalWrite(PIN_OUT, LOW);  // sets the digital pin 13 off
    delay(500);            // waits for a second
  }    
  swsri.println("connected at 115200");
}
