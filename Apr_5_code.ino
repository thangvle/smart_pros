/*
This is a setup sketch for only one MX-28 connected and it is used to set ID and Baudrate of the Dynamixal

Connection of Dynamixel to Arduino 
==================================
You do not need a half to full duplex circuit if you do not wish to receive ANY data FROM the Dynamixal servo, as we are only setting up the Dynamixal servo we will leave this circuit out and connect directly to Arduino to make things simple.

MX-28 (Pin)            Arduino (Pin)
====================================
GND (1) -------------- GND (Power GND)
VDD (2) -------------- VIN (Power VIN)
DATA(3) -------------- TX (Pin 1) 

With the 3 wires connected as above and the Arduino programmed with this sketch connect a 12Vdc to the DC in of the Arduino. 
(CAUTION! This power supply must not be greater then +14.8Vdc as this is the supply that powers the Dynamixal). 
Wait about a ONE minute and if successfully the Dynamixal should start to move with its LED turning ON and OFF.

Robotis e-Manual ( http://support.robotis.com )

*/

#include <SoftwareSerial.h>
#include <Dynamixel_Serial.h>       // Library needed to control Dynamixal servo

SoftwareSerial mySerial(11, 10); // RX, TX

#define SERVO_ID 0x01               // ID of which we will set Dynamixel too 
#define SERVO_ControlPin 0x02       // Control pin of buffer chip, NOTE: this does not matter becasue we are not using a half to full contorl buffer.
#define SERVO_SET_Baudrate 1000000  // Baud rate speed which the Dynamixel will be set too (1Mbps)
#define LED13 0x0D                  // Pin of Visual indication for runing "heart beat" using onboard LED

#define CW_LIMIT_ANGLE -0x6000        // lowest clockwise angle is 1, as when set to 0 it set servo to wheel mode
#define CCW_LIMIT_ANGLE 0x6000       // Highest anit-clockwise angle is 0XFFF, as when set to 0 it set servo to wheel mode

void setup(){
 pinMode(LED13, OUTPUT);            // Pin setup for Visual indication of runing (heart beat) program using onboard LED
 digitalWrite(LED13, HIGH);

 delay(1000);                                                 // Give time for Dynamixel to start on power-up

 for (int b=1; b<0xFF; b++){                                  // This "for" loop will take about 20 Sec to compelet and is used to loop though all speeds that Dynamixel can be and send reset instuction 
    long Baudrate_BPS = 0;
    Baudrate_BPS  = 2000000 / (b + 1);                        // Calculate Baudrate as ber "Robotis e-manual"
      Dynamixel.begin(Baudrate_BPS);   // Set Ardiuno Serial speed and control pin      
    Dynamixel.setDirectionPin(SERVO_ControlPin);                            // Optional. Set direction control pin

        Dynamixel.reset(0xFE);                                // Broadcast to all Dynamixel IDs(0xFE is the ID for all Dynamixel to responed) and Reset Dynamixel to factory default
        delay(5);
        Dynamixel.end();
        delay(5);
         
 } 
 digitalWrite(LED13, LOW);
 
 delay(3000);                                                 // Give time for Dynamixel to reset
  
 // Now that the Dynamixel is reset to factory setting we will program its Baudrate and ID
 Dynamixel.begin(1000000);                 // Set Ardiuno Serial speed to factory default speed of 1000000
     Dynamixel.setDirectionPin(SERVO_ControlPin);                            // Optional. Set direction control pin

 Dynamixel.setID(0xFE,SERVO_ID);                               // Broadcast to all Dynamixel IDs(0xFE) and set with new ID
 delay(10);                                                     // Time needed for Dynamixel to set it's new ID before next instruction can be sent
 Dynamixel.setStatusPaket(SERVO_ID,READ);                      // Tell Dynamixel to only return status packets when a "read" instruction is sent e.g. Dynamixel.readVoltage();
 Dynamixel.setBaudRate(SERVO_ID,SERVO_SET_Baudrate);           // Set Dynamixel to new serial speed 
 delay(30);                                                    // Time needed for Dynamixel to set it's new Baudrate


  Dynamixel.begin(SERVO_SET_Baudrate);    // We now need to set Ardiuno to the new Baudrate speed 
      Dynamixel.setDirectionPin(SERVO_ControlPin);                            // Optional. Set direction control pin

  Dynamixel.ledState(SERVO_ID, ON);                            // Turn Dynamixel LED on
  delay(5);
  Dynamixel.setMode(SERVO_ID, SERVO,-0x6000,0x6000);              // Turn mode to SERVO, must be WHEEL if using wheel mode
  delay(5);
  Dynamixel.setMaxTorque(SERVO_ID, 0x2FF);                     // Set Dynamixel to max torque limit

// put your setup code here, to run once:
Serial.begin(57600);
mySerial.begin(1000000);
delay(1000);
Dynamixel.begin(mySerial);                                    // We now need to set Ardiuno to the new Baudrate speed
Serial.println("begun");
Dynamixel.setMode(SERVO_ID, SERVO, CW_LIMIT_ANGLE, CCW_LIMIT_ANGLE);    // set mode to SERVO and set angle limits
Dynamixel.servo(SERVO_ID,-0x1000,0x100);   // Comman for servo mode, Move servo to angle 1(0.088 degree) at speed 100
}



// Flash Dynamixel LED and move Dynamixel to check that all setting have been writen
void loop(){
  // put your main code here, to run repeatedly:
//  digitalWrite(LED13, HIGH);                  // Turn Arduino onboard LED on
//  Dynamixel.ledState(SERVO_ID, ON);           // Turn Dynamixel LED on
//  delayMicroseconds(1);
//  Dynamixel.wheel(SERVO_ID,LEFT,0x3FF);              // Comman for Wheel mode, Move left at max speed  
//    digitalWrite(LED13, LOW);  
//  Dynamixel.servo(SERVO_ID,0x002,0x100);   // Comman for servo mode, Move servo to angle 1(0.088 degree) at speed 100
// delay(4000);
  
//  digitalWrite(LED13, LOW);                  // Turn Arduino onboard LED off
//  Dynamixel.ledState(SERVO_ID, OFF);         //Turn Dynamixel LED off
//  delayMicroseconds(1);
//  Dynamixel.wheel(SERVO_ID,RIGHT,0x3FF);          // Comman for Wheel mode, Move right at max speed 
//  Dynamixel.servo(SERVO_ID,0x7000,0x3FF);  // Comman for servo mode, Move servo to max angle at max speed (angle
//  delay(4000);

//  Dynamixel.servo(SERVO_ID,0x001,0x100);   // Move servo to angle 1(0.088 degree) at speed 100
//  Dynamixel.ledState(SERVO_ID, ON);           // Turn Dynamixel LED on

//  delay(4000);
// Serial.println("switch");

//  Dynamixel.ledState(SERVO_ID, OFF);         //Turn Dynamixel LED off

//  Dynamixel.wheel(SERVO_ID,LEFT,0x3FF);  //  Move servo to max angle at max speed (1023)
//  Dynamixel.servo(SERVO_ID,0x001,0x3FF);  //  Move servo to max angle at max speed (1023)
//  delay(4000);
//  Serial.println("switch");  
}
