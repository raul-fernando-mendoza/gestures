#include "TinyWireM.h"
// to be able to send data at 115200 to BLT-05 you need to AT+BAUD8 to the BLT-05 using the 3 volts in the usb to serial
// +BAUD=115200
 
#define TX_PIN PB4
#include "ATtinySerialOut.hpp"

#define PIN_OUT 3
#define PIN_INPUT 1


#define RX    -1   // *** D3, Pin 2 rmh remove 3 as RX 
#define TX    4   // *** D4, Pin 3


// #define DEBUG 1  // - uncomment this line to display accel/gyro values
#ifdef DEBUG
#endif

int accelX, accelY, accelZ;
int gyroX, gyroY, gyroZ;
int gyroXold, gyroYold, gyroZold;
char mpu = 0x68;  // I2C address of MPU.  Connect 5V to pin ADO to use 0x69 address instead

int led = 1;
unsigned long ledLastChangedTime = 0L;

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
/* set clock to max speed
  cli(); // Disable interrupts
  CLKPR = (1<<CLKPCE); // Prescaler enable
  CLKPR = 0; // Clock division factor 1 (0000)
  sei(); // Enable interrupts
*/  
  initTXPin();
 // swsri.print("Setup speed to:115200");
   
  TinyWireM.begin();

  Serial.println("Setup");
  // We need to do three things.  1. Disable sleep mode on the MPU (it activates on powerup).  2. Set the scale of the Gyro.  3. Set the scale of the accelerometer
  // We do this by sending 2 bytes for each:  Register Address & Value
  TinyWireM.beginTransmission(mpu); 
  TinyWireM.write(0x6B); //  Power setting address
  TinyWireM.write(0b00000000); // Disable sleep mode (just in case)
  TinyWireM.endTransmission();
  TinyWireM.beginTransmission(mpu); 
  TinyWireM.write(0x1B); // Config register for Gyro
  TinyWireM.write(0x00000000); // 250° per second range (default)
  TinyWireM.endTransmission();
  TinyWireM.beginTransmission(mpu); //I2C address of the MPU
  TinyWireM.write(0x1C); // Accelerometer config register
  TinyWireM.write(0b00000000); // 2g range +/- (default)
  TinyWireM.endTransmission();
  //swsri.println("Starting v1");
}

void loop() {
  getAccel();
  getGyro();
  
    
  Serial.print(millis());
  Serial.print("\t");
  Serial.print(gyroX);
  Serial.print("\t");
  Serial.print(gyroY);
  Serial.print("\t");
  Serial.print(gyroZ);
  Serial.print("\t");
  Serial.print(accelX);
  Serial.print("\t");
  Serial.print(accelY);
  Serial.print("\t");
  Serial.print(accelZ);
  Serial.print("\t");

  int buttonStatus = digitalRead(PIN_INPUT);
  Serial.print(buttonStatus);  
  Serial.println();

  if(  millis() - 1000 > ledLastChangedTime){
    led = !led;
    digitalWrite(PIN_OUT, led );
    ledLastChangedTime = millis();
  }  
}

void getAccel() {
  TinyWireM.beginTransmission(mpu); //I2C address of the MPU
  TinyWireM.write(0x3B); //  Acceleration data register
  TinyWireM.endTransmission();
  TinyWireM.requestFrom(mpu, 6); // Get 6 bytes, 2 for each DoF
  accelX = TinyWireM.read() << 8; // Get X upper byte first
  accelX |= TinyWireM.read();     // lower
  accelY = TinyWireM.read() << 8; // Get Y upper byte first
  accelY |= TinyWireM.read();     // lower
  accelZ = TinyWireM.read() << 8; // Get Z upper byte first
  accelZ |= TinyWireM.read();     // lower
}

void getGyro() {
  TinyWireM.beginTransmission(mpu); //I2C address of the MPU
  TinyWireM.write(0x43); // Gyro data register
  TinyWireM.endTransmission();
  TinyWireM.requestFrom(mpu, 6); // Get 6 bytes, 2 for each DoF
  while (TinyWireM.available() < 6);
  gyroX = TinyWireM.read() << 8; // Get X upper byte first
  gyroX |= TinyWireM.read();     // lower
  gyroY = TinyWireM.read() << 8; // Get Y upper byte first
  gyroY |= TinyWireM.read();     // lower
  gyroZ = TinyWireM.read() << 8; // Get Z upper byte first
  gyroZ |= TinyWireM.read();     // lower
}
