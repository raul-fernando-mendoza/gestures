#include <SoftwareSerial.h>  // libreria que permite establecer pines digitales
        // para comunicacion serie

SoftwareSerial miBT(10, 11);  // pin 10 como RX, pin 11 como TX

void setup(){
  //pinMode(10, OUTPUT);
  //digitalWrite(10, LOW);
  //pinMode(11, OUTPUT);
  //digitalWrite(11, LOW);
  Serial.begin(9600);   // comunicacion de monitor serial a 9600 bps
  Serial.println("Listo");  // escribe Listo en el monitor
  miBT.begin(9600);    // comunicacion serie entre Arduino y el modulo a 38400 bps
}

void loop(){
  if (miBT.available())       // si hay informacion disponible desde modulo
     Serial.write(miBT.read());   // lee Bluetooth y envia a monitor serial de Arduino
  
  if (Serial.available())     // si hay informacion disponible desde el monitor serial
     miBT.write(Serial.read());   // lee monitor serial y envia a Bluetooth
  
}
