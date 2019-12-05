/* THIS CODE is aimed to guide arbortix to switch between train and control modes through black training button and arduino communication*/
  // as of right now, this code is waiting for interface testing. To do this, interface needs to put back where they are with arduino channel 1  and 2
 
int Act_Train_inPin = 0; // this is for the black training button 

  int Act_train_state = LOW;      // the current Act_train_state of the output pin
  int Act_train_reading;           // the current Act_train_reading from the input pin
  int ActTrain_prev = LOW;    // the ActTrain_prev Act_train_reading from the input pin

  // the follow variables are long's because the Act_Train_time, measured in miliseconds,
  // will quickly become a bigger number than can be stored in an int.
  long Act_Train_time = 0;         // the last Act_Train_time the output pin was toggled
  long Act_Train_debounce = 200;   // the Act_Train_debounce Act_Train_time, increase if the output flickers

// to declare for Yellow LED or grasping modes
  // constants won't change. Used here to set a pin number:
  const int YellowLEDPin = 0;// the number of the LED pin - using user one for now

  // Variables will change:
  int YellowState = LOW;             // YellowState used to set the LED

  // Generally, you should use "unsigned long" for variables that hold time
  // The value will quickly become too large for an int to store
  unsigned long prevYellowMillis = 0;        // will store last time LED was updated

  // constants will change depends on grasping state
  long Yellowinterval = 0;           // Yellowinterval at which to blink (milliseconds)
  unsigned long nextstop = 0;

// to declare thresholds
  // These constants won't change. They're used to give names to the pins used:

  const int analogInPin0 = A0;  // Analog input pin for pinky finger
  const int analogInPin1 = A1;  // Analog input pin for ring finger
  const int analogInPin2 = A2;  // Analog input pin for middle finger
  const int analogInPin3 = A3;  // Analog input pin for index finger
  const int analogInPin4 = A4;  // Analog input pin for longtitudinal thumb 
  const int analogInPin5 = A5;  // Analog input pin for axial thumb 
  
  unsigned long currenttime;

// to set it up for servos
  #include <ax12.h>
  int a = 300; // delay between servo commands
  int b = a; // delay between loops

void setup()
{
  // for train/act
  pinMode(Act_Train_inPin, INPUT);

  // for grasping
  pinMode(YellowLEDPin, OUTPUT);

  // for threshold
  Serial.begin(115200);  //probably boadrate here
  
  //  for arduino communication
  Serial.begin(115200);
  pinMode(2, INPUT);
  pinMode(0, OUTPUT); 
  pinMode(1, INPUT);
}

void loop()
{
  Act_train_reading = digitalRead(Act_Train_inPin);

  // if the input just went from LOW and HIGH and we've waited long enough
  // to ignore any noise on the circuit, toggle the output pin and remember
  // the Act_Train_time
  if (Act_train_reading == HIGH && ActTrain_prev == LOW && millis() - Act_Train_time > Act_Train_debounce) {
    if (Act_train_state == HIGH) {
      Act_train_state = LOW; }
    else {
      Act_train_state = HIGH;}

    Act_Train_time = millis();   
  }
  ActTrain_prev = Act_train_reading;

  // start training
  if (Act_train_state == HIGH)
    {
      // start rest training 
      Serial.println("start training");
      nextstop = millis() + 10000;
      while (millis() < nextstop)
       {
        digitalWrite(YellowLEDPin, LOW); // this is when we will calibrate rest mode for 10s if necessary
       }
        digitalWrite(YellowLEDPin, HIGH); // this signals the end of rest train mode and start grasp mode 1

    // train grasp mode 1 for 5s, turn on yellow LED for 5s
          nextstop = millis() + 5000;
          Serial.println("start mode 1");
          while (millis() < nextstop)
           {
            digitalWrite(YellowLEDPin, HIGH); // this is when we will calibrate grasp mode 1 for 5s
              
           }
            digitalWrite(YellowLEDPin, LOW); // this signals the end of grasp mode 1

    // start break between modes for 10s
      nextstop = millis() + 10000;
      while (millis() < nextstop)
       {
        digitalWrite(YellowLEDPin, LOW); // this is when we will stop grasping mode 1 for 10s if necessary
       }
        digitalWrite(YellowLEDPin, HIGH); // this signals the end of grasping mode 1 and start grasp mode 2

    // train grasp mode 2 for 5s, turn on yellow LED for 5s
          nextstop = millis() + 5000;
          Serial.println("Train mode 2 starts");
          while (millis() < nextstop)
           {
            digitalWrite(YellowLEDPin, HIGH); // this is when we will calibrate grasp mode 2 for 5s               
           }
            digitalWrite(YellowLEDPin, LOW); // this signals the end of grasp mode 2

        Act_train_state = LOW; // this signals the end of all train mode
        Serial.println("Realtime Control");
    }
 // start controlling
       //  make it rest and then change this when new command comes.
          SetPosition(3,2800); //set the position of servo # 1 to '0', 
          delay(a);//wait for servo to move
          SetPosition(2,2300); //set the position of servo # 2 to '0', PINKY FINGER calibrated rest
          delay(a);//wait for servo to move
          SetPosition(5,820); //set the position of servo # 2 to '0', long thumb calibrated rest
          delay(a);//wait for servo to move
          SetPosition(4,600); //set the position of servo # 4 to '0' pointer finger calibrated rest
          delay(a);//wait for servo to move 
          SetPosition(1,700); //set the position of servo # 4 to '0' ax THUMB calibrated rest
          delay(a);//wait for servo to move 
           SetPosition(6,720); //set the position of servo # 4 to '0' only  run from 0 to 1023 middle fingeer
          delay(1000);//wait for servo to move 
          
      //read servos moving command from Arduino
      int sensorVal1 = digitalRead(1); 
      int sensorVal2 = digitalRead(2);
  
    // servos activation mode
     if (sensorVal1 == HIGH) {
        digitalWrite(7, HIGH); // this  is when servos need to activate mode 1 - tranverse  volar  grasping v4
            SetPosition(1,1020); //set the position of servo # 4 to '0' ax THUMB calibrated rest
            delay(a);//wait for servo to move 
            SetPosition(5,0); //set the position of servo # 2 to '0', long thumb calibrated rest
            delay(a);//wait for servo to move
            SetPosition(4,3000); //set the position of servo # 4 to '0' pointer finger calibrated rest
            delay(a);//wait for servo to move 
            SetPosition(6,0); //set the position of servo # 4 to '0' only  run from 0 to 1023 middle fingeer   
            delay(a);//wait for servo to move 
            SetPosition(3,0); //set the position of servo # 1 to '0', ring finger calibrated rest
            delay(a);//wait for servo to move
            SetPosition(2,2300); //set the position of servo # 2 to '0', PINKY FINGER calibrated rest
            delay(b);//wait for servo to move
      } 
      else {
            if (sensorVal2 == HIGH) {
          digitalWrite(6, HIGH); // this  is when servos need to activate mode 2 - pinch v1
          
          SetPosition(1,700); //set the position of servo # 4 to '0' ax THUMB calibrated rest
          delay(a);//wait for servo to move 
          SetPosition(4,3000); //set the position of servo # 4 to '0' pointer finger calibrated rest
          delay(a);//wait for servo to move 
          SetPosition(5,0); //set the position of servo # 2 to '0', long thumb calibrated rest
          delay(a);//wait for servo to move
          SetPosition(6,0); //set the position of servo # 4 to '0'  middle fingeer   
          delay(a);//wait for servo to move 
          SetPosition(3,0); //set the position of servo # 1 to '0', ring finger calibrated rest
          delay(a);//wait for servo to move
          SetPosition(2,2300); //set the position of servo # 2 to '0', PINKY FINGER calibrated rest
          delay(a);//wait for servo to move
        } 
        else {
          digitalWrite(5, HIGH); // this is when all servos need to rest
        }
      }
}
