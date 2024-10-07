#include <Servo.h>

Servo myservo;
Servo myservo2;
Servo myservo3;
Servo myservo4;

void setup() {
  Serial.begin(9600);
  myservo.attach(3);   // attaches the servo on pin 3 to the servo object
  myservo2.attach(5);  // attaches the servo on pin 5 to the servo object
  myservo3.attach(6);  // attaches the servo on pin 6 to the servo object
  myservo4.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop() {
  if (Serial.available() > 0) {
    String angleData = Serial.readStringUntil('\n');  // Read the incoming serial data
    int commaIndex = angleData.indexOf(','); // Find the comma separator
    if (commaIndex > 0) {
      String horAngleStr = angleData.substring(0, commaIndex);
      String vertAngleStr = angleData.substring(commaIndex + 1);
      float hor_angle = horAngleStr.toFloat(); // Convert to float
      float vert_angle = vertAngleStr.toFloat(); // Convert to float

      myservo2.write(0); /// to move upwards... increase servo2 and decrease servo1   
      myservo.write(180); ///all in parallel   
      myservo3.write(90);     
      myservo4.write(85);     
      delay(2000);   
      
      if(hor_angle > 85) {
        for(int i = 85; i < hor_angle; i += 2) {
          myservo4.write(i);
          delay(50);
        }
      } else if (hor_angle <= 85) {
        for(int i = 85; i > hor_angle; i -= 2) {
          myservo4.write(i);
          delay(50);
        }    
      }
      delay(2000);
      
      for(int i = 0; i <= vert_angle; i += 5) {
        myservo2.write(i);
        myservo.write(180 - i);
        delay(50);
      }

      delay(2000);
      myservo3.write(0);
      delay(1000);
      myservo3.write(90);
      delay(1000);
      
      for(int i = (vert_angle / 5) * 5; i >= 0; i -= 5) {
        myservo2.write(i);
        myservo.write(180 - i);
        delay(50);
      }
      delay(1000);

      if(hor_angle > 85) {
        for(int i = (hor_angle / 2) * 2; i >= 85; i -= 2) {
          myservo4.write(i);
          delay(50);
        }
      } else if (hor_angle <= 85) {
        for(int i = (hor_angle / 2) * 2; i <= 85; i += 2) {
          myservo4.write(i);
          delay(50);
        }    
      }
    }  
  }
}
