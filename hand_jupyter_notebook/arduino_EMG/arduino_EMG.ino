// These constants won't change. They're used to give names to the pins used:
const int analogInPin1 = A1;  // Analog input pin that the potentiometer is attached to
const int analogInPin2 = A2;  // Analog input pin that the potentiometer is attached to
const int analogInPin3 = A3;  // Analog input pin that the potentiometer is attached to
const int analogInPin4 = A4;  // Analog input pin that the potentiometer is attached to
const int analogInPin5 = A5;  // Analog input pin that the potentiometer is attached to
unsigned long currenttime;
double sensorValue1 = 0;        // value read from the pot
double sensorValue2 = 0;        // value read from the pot
double sensorValue3 = 0;        // value read from the pot
double sensorValue4 = 0;        // value read from the pot
double sensorValue5 = 0;        // value read from the pot

const int led2 = 2;
const int led3 = 3;
const int led4 = 4;
int incomingByte;

void setup() {
  Serial.begin(115200);
 
//   Serial.print("Rest for 3 seconds...");
//  delay(1000);
//  Serial.print("Rest for 2 seconds...");
//  delay(1000);
//   Serial.println("Rest for 1 seconds...");
//   delay(1000);
//   Serial.print("Start recording for holding movement of holding a cup posture for 7 seconds...");
//   Serial.print("\n");
   currenttime=millis();
   
   pinMode(led2, OUTPUT);
   pinMode(led3, OUTPUT);
   pinMode(led4, OUTPUT);
   
}
void loop() {

  while(currenttime<100){
  // read the analog in value:
    sensorValue1 = analogRead(analogInPin1);
    sensorValue2 = analogRead(analogInPin2);
    sensorValue3 = analogRead(analogInPin3);
    sensorValue4 = analogRead(analogInPin4);
    sensorValue5 = analogRead(analogInPin5);
    currenttime=millis();
    //Serial.println(currenttime);
    //Serial.print(" miliseconds");
    //Serial.print("\t");
    Serial.print(sensorValue1*5/1023);
    Serial.print("\t");
    Serial.print(sensorValue2*5/1023);
    Serial.print("\t");
    Serial.print(sensorValue3*5/1023);
    Serial.print("\t");
    Serial.print(sensorValue4*5/1023);
    Serial.print("\t");
    Serial.print(sensorValue5*5/1023);
    Serial.println();
    delay(10);
    
    if (Serial.available() > 0) {
      incomingByte = Serial.read();
      if (incomingByte == 'A') {
        digitalWrite(led2, HIGH);
        digitalWrite(led3, LOW);
      }
      if (incomingByte == 'R'){
        digitalWrite(led2, LOW);
        digitalWrite(led3, HIGH); 
      }
    }  
  }
}


