/*
 *  Mandatory includes
 */
#include <Arduino.h>
#include <TinyMPU6050.h>

/*
 *  Constructing MPU-6050
 */
MPU6050 mpu (Wire);
int x=0;
int prev_x=0;
int y=0;
int prev_y;
int z=0;
int prev_z;
String  str;
/*
 *  Setup
 */
void setup() {

  // Initialization
  mpu.Initialize();

  // Calibration
  Serial.begin(9600);
  Serial.println("=====================================");
  Serial.println("Starting calibration...");
  mpu.Calibrate();
  Serial.println("Calibration complete!");
  Serial.println("Offsets:");
  Serial.print("GyroX Offset = ");
  Serial.println(mpu.GetGyroXOffset());
  Serial.print("GyroY Offset = ");
  Serial.println(mpu.GetGyroYOffset());
  Serial.print("GyroZ Offset = ");
  Serial.println(mpu.GetGyroZOffset());
}

/*
 *  Loop
 */
void loop() {

  mpu.Execute();

    x = mpu.GetAngX();
    y = mpu.GetAngY();
    z = mpu.GetAngZ();
    if( x != prev_x || y!=prev_y || z != prev_z){
      str = "" + String(x) + "," + String(y) + "," + String(z);
      Serial.println(str);
      prev_x = x;
      prev_y = y;
      prev_z = z;
    }  
}
