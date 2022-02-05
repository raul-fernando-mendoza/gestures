/*
 *  Mandatory includes
 */
#include <SoftwareSerial.h>
#define PIN_OUT 1
#define RX    3   // *** D3, Pin 2
#define TX    4   // *** D4, Pin 3
SoftwareSerial swsri(RX,TX);

#include <Arduino.h>
#include <TinyMPU6050.h>

/*
 *  Constructing MPU-6050
 */
MPU6050 mpu (Wire);

/*
 *  Method that prints everything
 */
void PrintGets () {
  // Shows offsets
  swsri.println("--- Offsets:");
  swsri.print("GyroX Offset = ");
  swsri.println(mpu.GetGyroXOffset());
  swsri.print("GyroY Offset = ");
  swsri.println(mpu.GetGyroYOffset());
  swsri.print("GyroZ Offset = ");
  swsri.println(mpu.GetGyroZOffset());
  // Shows raw data
  swsri.println("--- Raw data:");
  swsri.print("Raw AccX = ");
  swsri.println(mpu.GetRawAccX());
  swsri.print("Raw AccY = ");
  swsri.println(mpu.GetRawAccY());
  swsri.print("Raw AccZ = ");
  swsri.println(mpu.GetRawAccZ());
  swsri.print("Raw GyroX = ");
  swsri.println(mpu.GetRawGyroX());
  swsri.print("Raw GyroY = ");
  swsri.println(mpu.GetRawGyroY());
  swsri.print("Raw GyroZ = ");
  swsri.println(mpu.GetRawGyroZ());
  // Show readable data
  swsri.println("--- Readable data:");
  swsri.print("AccX = ");
  swsri.print(mpu.GetAccX());
  swsri.println(" m/s²");
  swsri.print("AccY = ");
  swsri.print(mpu.GetAccY());
  swsri.println(" m/s²");
  swsri.print("AccZ = ");
  swsri.print(mpu.GetAccZ());
  swsri.println(" m/s²");
  swsri.print("GyroX = ");
  swsri.print(mpu.GetGyroX());
  swsri.println(" degrees/second");
  swsri.print("GyroY = ");
  swsri.print(mpu.GetGyroY());
  swsri.println(" degrees/second");
  swsri.print("GyroZ = ");
  swsri.print(mpu.GetGyroZ());
  swsri.println(" degrees/second");
  // Show angles based on accelerometer only
  swsri.println("--- Accel angles:");
  swsri.print("AccelAngX = ");
  swsri.println(mpu.GetAngAccX());
  swsri.print("AccelAngY = ");
  swsri.println(mpu.GetAngAccY());
  // Show angles based on gyroscope only
  swsri.println("--- Gyro angles:");
  swsri.print("GyroAngX = ");
  swsri.println(mpu.GetAngGyroX());
  swsri.print("GyroAngY = ");
  swsri.println(mpu.GetAngGyroY());
  swsri.print("GyroAngZ = ");
  swsri.println(mpu.GetAngGyroZ());
  // Show angles based on both gyroscope and accelerometer
  swsri.println("--- Filtered angles:");
  swsri.print("FilteredAngX = ");
  swsri.println(mpu.GetAngX());
  swsri.print("FilteredAngY = ");
  swsri.println(mpu.GetAngY());
  swsri.print("FilteredAngZ = ");
  swsri.println(mpu.GetAngZ());
  // Show filter coefficients
  swsri.println("--- Angle filter coefficients:");
  swsri.print("Accelerometer percentage = ");
  swsri.print(mpu.GetFilterAccCoeff());
  swsri.println('%');
  swsri.print("Gyroscope percentage = ");
  swsri.print(mpu.GetFilterGyroCoeff());
  swsri.println('%');
}

/*
 *  Setup
 */
void setup() {

  // Initialization
  mpu.Initialize();

  // Calibration
  swsri.begin(9600);
  swsri.println("=====================================");
  swsri.println("Starting calibration...");
  mpu.Calibrate();
  swsri.println("Calibration complete!");
}

/*
 *  Loop
 */
void loop() {
  
  mpu.Execute();
  PrintGets();
  delay(30000); // 30 sec delay

}
