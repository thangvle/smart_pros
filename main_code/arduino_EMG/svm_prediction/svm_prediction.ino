const int analogInPin0 = A0;  // Analog input pin that the potentiometer is attached to
const int analogInPin1 = A1;  // Analog input pin that the potentiometer is attached to
const int analogInPin2 = A2;  // Analog input pin that the potentiometer is attached to
const int analogInPin3 = A3;  // Analog input pin that the for EMG1 
const int analogInPin4 = A4;  // Analog input pin that the for EMG2
const int analogInPin5 = A5;  // Analog input for EMG3 (FIFTH position from left, await real time confirmation)
unsigned long currenttime;

double Ac1 = 0;      // value read from the pot
double Ac2 = 0;      // value read from the pot
double Ac3 = 0;      // value read from the pot
double EMG1 = 0;      // value read from the pot
double EMG2 = 0;      // value read from the pot
double EMG3 = 0;      // value read from the pot


void setup() {
  // put your setup code here, to run once:

Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  Ac1 = 2  + analogRead(analogInPin0); // accelerometer channel 1
  Ac2 = 2  + analogRead(analogInPin1); // accelerometer channel 2
  Ac3 = 2  + analogRead(analogInPin2); // accelerometer channel 3
  EMG1 = 2  + analogRead(analogInPin3); // EMG channel 1
  EMG2 = 2  + analogRead(analogInPin4); // EMG channel 2
  EMG3 = 2  + analogRead(analogInPin5); // EMG channel 3

  Serial.print(Ac1);
  Serial.print("\t");
  Serial.print(Ac2);
  Serial.print("\t");
  Serial.print(Ac3);
  Serial.print("\t");
  Serial.print(EMG1);
  Serial.print("\t");
  Serial.print(EMG2);
  Serial.print("\t");
  Serial.println(EMG3);

  
}
