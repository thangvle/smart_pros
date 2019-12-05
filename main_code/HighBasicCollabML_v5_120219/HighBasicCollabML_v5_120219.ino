/* THIS CODE should codify the analog signals to tell Python when training mode 1 starts and stops, similarly to mode 2, and then activation  mode */
/* For Python to communicate with this code, please read:
      0 0 0 0 0 0 as Iddle mode
      1 0 0 0 0 0 as label mode for grasp 1 training
      0 1 0 0 0 0 as label mode for grasp 2 training
      0 0 1 0 0 0 as ML prediction model
      Any other combinations as ML prediction mode
      
as of right now, the silence needs to be filled with 0 0 0 0 0 0 => to be fixed next time*/

// to declare for Blue LED or train/activation mode
  int Act_Train_inPin = 3;         // the number of the input pin
  int Act_Train_outPin = 11;       // the number of the output pin
  
  int Act_train_state = LOW;      // the current Act_train_state of the output pin
  int Act_train_reading;           // the current Act_train_reading from the input pin
  int ActTrain_prev = LOW;    // the ActTrain_prev Act_train_reading from the input pin
  
  // the follow variables are long's because the Act_Train_time, measured in miliseconds,
  // will quickly become a bigger number than can be stored in an int.
  long Act_Train_time = 0;         // the last Act_Train_time the output pin was toggled
  long Act_Train_debounce = 200;   // the Act_Train_debounce Act_Train_time, increase if the output flickers

// to declare for Yellow LED or grasping modes
  // constants won't change. Used here to set a pin number:
  const int YellowLEDPin =  LED_BUILTIN;// the number of the LED pin
  
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
  const int graspPin1 =  9;      // the number of the grasping mode 1 activation
  const int graspPin2 =  10;      // the number of the grasping mode 2 activation
  
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

  double Ac1M1 = 0;      // value read from the pot
  double Ac2M1 = 0;      // value read from the pot
  double Ac3M1 = 0;      // value read from the pot
  double EMG1M1 = 0;      // value read from the pot
  double EMG2M1 = 0;      // value read from the pot
  double EMG3M1 = 0;      // value read from the pot
  
  double Ac1M2 = 0;      // value read from the pot
  double Ac2M2 = 0;      // value read from the pot
  double Ac3M2 = 0;      // value read from the pot
  double EMG1M2 = 0;      // value read from the pot
  double EMG2M2 = 0;      // value read from the pot
  double EMG3M2 = 0;      // value read from the pot
  
  double M1ax_Ac1 = 0;
  double M1ax_Ac2 = 0;
  double M1ax_Ac3 = 0;
  double M2ax_Ac1 = 0;
  double M2ax_Ac2 = 0;
  double M2ax_Ac3 = 0;
  double M1in_Ac1 = 0;
  double M1in_Ac2 = 0;
  double M1in_Ac3 = 0;
  double M2in_Ac1 = 0;
  double M2in_Ac2 = 0;
  double M2in_Ac3 = 0;
  
  double M1ax_EMG1 = 0;
  double M1ax_EMG2 = 0;
  double M1ax_EMG3 = 0;
  double M2ax_EMG1 = 0;
  double M2ax_EMG2 = 0;
  double M2ax_EMG3 = 0;
  double M1in_EMG1 = 0;
  double M1in_EMG2 = 0;
  double M1in_EMG3 = 0;
  double M2in_EMG1 = 0;
  double M2in_EMG2 = 0;
  double M2in_EMG3 = 0;

void setup()
{
  // for train/act
  pinMode(Act_Train_inPin, INPUT);
  pinMode(Act_Train_outPin, OUTPUT);

  // for grasping
  pinMode(YellowLEDPin, OUTPUT);

  // for threshold
  Serial.begin(2000000);  //probably boadrate here
  // initialize the Grasping pins as outputs:
  pinMode(graspPin1, OUTPUT);
  pinMode(graspPin2, OUTPUT);

      Serial.begin(115200); 
      Serial.print(0); // this will tell Python to not to label anything, stop activation mode
      Serial.print("\t");
      Serial.print(0);
      Serial.print("\t");
      Serial.print(1);
      Serial.print("\t");
      Serial.print(0);
      Serial.print("\t");
      Serial.print(0);
      Serial.print("\t");
      Serial.println(0);

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

  digitalWrite(Act_Train_outPin, Act_train_state); //or the blue LED
  ActTrain_prev = Act_train_reading;

      
  // start training
  if (Act_train_state == HIGH) 
    {
      // start rest calibration
      Serial.print(0); // this will tell Python to not to label anything, stop activation mode
      Serial.print("\t");
      Serial.print(0);
      Serial.print("\t");
      Serial.print(0);
      Serial.print("\t");
      Serial.print(0);
      Serial.print("\t");
      Serial.print(0);
      Serial.print("\t");
      Serial.println(0);
          
          nextstop = millis() + 5000; //pause 5 seconds to prepare user in training mode 1
          while (millis() < nextstop)     
       {
        digitalWrite(YellowLEDPin, LOW); // this is when we will calibrate rest mode for 10s if necessary
       }
        digitalWrite(YellowLEDPin, HIGH); // this signals the end of rest train mode and start grasp mode 1
                  Serial.print(1);  // this tells pyhton to start labeling mode 1
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.println(0);

           
    // train grasp mode 1 for 5s, turn on yellow LED for 5s
          nextstop = millis() + 5000;
          while (millis() < nextstop) 
           {
            digitalWrite(YellowLEDPin, HIGH); // this is when we will calibrate grasp mode 1 for 5s
            
              Ac1M1 = 2  + analogRead(analogInPin0); // accelerometer channel 1
              Ac2M1 = 2  + analogRead(analogInPin1); // accelerometer channel 2
              Ac3M1 = 2  + analogRead(analogInPin2); // accelerometer channel 3
              EMG1M1 = 2  + analogRead(analogInPin3); // EMG channel 1
              EMG2M1 = 2  + analogRead(analogInPin4); // EMG channel 2
              EMG3M1 = 2  + analogRead(analogInPin5); // EMG channel 3

              Serial.print(Ac1M1);
              Serial.print("\t");
              Serial.print(Ac2M1);
              Serial.print("\t");
              Serial.print(Ac3M1);
              Serial.print("\t");
              Serial.print(EMG1M1);
              Serial.print("\t");
              Serial.print(EMG2M1);
              Serial.print("\t");
              Serial.println(EMG3M1);    
                  
              // define standard thresholds for Grasping mode 1
                // let's define max
                if (Ac1M1 > M1ax_Ac1) { M1ax_Ac1 = Ac1M1;}
                if (Ac2M1 > M1ax_Ac2) { M1ax_Ac2 = Ac2M1;}
                if (Ac3M1 > M1ax_Ac3) { M1ax_Ac3 = Ac3M1;}
                if (EMG1M1 > M1ax_EMG1) { M1ax_EMG1 = EMG1M1;}
                if (EMG2M1 > M1ax_EMG2) { M1ax_EMG2 = EMG2M1;}
                if (EMG3M1 > M1ax_EMG3) { M1ax_EMG3 = EMG3M1;}
            
                // let's define min
                if (Ac1M1 < M1in_Ac1) { M1in_Ac1 = Ac1M1;}
                if (Ac2M1 < M1in_Ac2) { M1in_Ac2 = Ac2M1;}
                if (Ac3M1 < M1in_Ac3) { M1in_Ac3 = Ac3M1;}
                if (EMG1M1 < M1in_EMG1) { M1in_EMG1 = EMG1M1;}
                if (EMG2M1 < M1in_EMG2) { M1in_EMG2 = EMG2M1;}
                if (EMG3M1 < M1in_EMG3) { M1in_EMG3 = EMG3M1;}
           }
            digitalWrite(YellowLEDPin, LOW); // this signals the end of grasp mode 1
                  Serial.print(0); //  this will  tell  python to stop all labeling until other values are seen
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.println(0);
                  
    // start break between modes for 5s
      nextstop = millis() + 5000;
      while (millis() < nextstop) 
       {
        digitalWrite(YellowLEDPin, LOW); // this is when we will stop grasping mode 1 for 10s if necessary
                
       }
        digitalWrite(YellowLEDPin, HIGH); // this signals the end of grasping mode 1 and start grasp mode 2
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(1); // this tells python to start labeling input for train mode 2
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.println(0);
           
    // train grasp mode 2 for 5s, turn on yellow LED for 5s
          nextstop = millis() + 5000;
          while (millis() < nextstop) 
           {
            digitalWrite(YellowLEDPin, HIGH); // this is when we will calibrate grasp mode 2 for 5s
     
                Ac1M2 = 2  + analogRead(analogInPin0);
                Ac2M2 = 2  + analogRead(analogInPin1);
                Ac3M2 = 2  + analogRead(analogInPin2);
                EMG1M2 = 2  + analogRead(analogInPin3);
                EMG2M2 = 2  + analogRead(analogInPin4);
                EMG3M2 = 2  + analogRead(analogInPin5);

                Serial.print(Ac1M2);
                Serial.print('\t');
                Serial.print(Ac2M2);
                Serial.print('\t');
                Serial.print(Ac3M2);
                Serial.print('\t');
                Serial.print(EMG1M2);
                Serial.print('\t');
                Serial.print(EMG2M2);
                Serial.print('\t');
                Serial.println(EMG3M2);

              // define standard thresholds for Grasping mode 2
                // let's define max
                if (Ac1M2 > M2ax_Ac1) { M2ax_Ac1 = Ac1M2;}
                if (Ac2M2 > M2ax_Ac2) { M2ax_Ac2 = Ac2M2;}
                if (Ac3M2 > M2ax_Ac3) { M2ax_Ac3 = Ac3M2;}
                if (EMG1M2 > M2ax_EMG1) { M2ax_EMG1 = EMG1M2;}
                if (EMG2M2 > M2ax_EMG2) { M2ax_EMG2 = EMG2M2;}
                if (EMG3M2 > M2ax_EMG3) { M2ax_EMG3 = EMG3M2;}
            
                // let's define min
                if (Ac1M2 < M2in_Ac1) { M2in_Ac1 = Ac1M2;}
                if (Ac2M2 < M2in_Ac2) { M2in_Ac2 = Ac2M2;}
                if (Ac3M2 < M2in_Ac3) { M2in_Ac3 = Ac3M2;}
                if (EMG1M2 < M2in_EMG1) { M2in_EMG1 = EMG1M2;}
                if (EMG2M2 < M2in_EMG2) { M2in_EMG2 = EMG2M2;}
                if (EMG3M2 < M2in_EMG3) { M2in_EMG3 = EMG3M2;}
           }
            digitalWrite(YellowLEDPin, LOW); // this signals the end of grasp mode 2
        
                   
        Act_train_state = LOW; // this signals the end of all train mode
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(1); // this  tells pynthon to switch from labeling mode 2 into prediction mode
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.print(0);
                  Serial.print("\t");
                  Serial.println(0);
                                 
    }
 // start controlling
     // read the analog in value:
    Ac1 = 2  + analogRead(analogInPin0); 
    Ac2 = 2  + analogRead(analogInPin1);
    Ac3 = 2  + analogRead(analogInPin2);
    EMG1 = 2  + analogRead(analogInPin3);
    EMG2 = 2  + analogRead(analogInPin4);
    EMG3 = 2  + analogRead(analogInPin5);

    // let's print out Serial here to double check proper analog signals
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
//
//  // check for mode 1
//      if (Ac1 > M2in_Ac1 && Ac1 < M2ax_Ac1 && Ac2 > M2in_Ac2 && Ac2 < M2ax_Ac2 && Ac3 > M2in_Ac3 && Ac3 < M2ax_Ac3 &&
//        EMG1 > M2in_EMG1 && EMG1 < M2ax_EMG1 && EMG2 > M2in_EMG2 && EMG2 < M2ax_EMG2 && EMG3 > M2in_EMG3 && EMG3 < M2ax_EMG3)
//       {
//        // Act mode 1 (pin out 10,  red)
//        digitalWrite(graspPin1, HIGH);
//        digitalWrite(graspPin2, LOW);
//        delay(2000);
//       }
//       else
//       {
//       
//    // check for mode 2
//    if (Ac1 > M1in_Ac1 && Ac1 < M1ax_Ac1 && Ac2 > M1in_Ac2 && Ac2 < M1ax_Ac2 && Ac3 > M1in_Ac3 && Ac3 < M1ax_Ac3 &&
//        EMG1 > M1in_EMG1 && EMG1 < M1ax_EMG1 && EMG2 > M1in_EMG2 && EMG2 < M1ax_EMG2 && EMG3 > M1in_EMG3 && EMG3 < M1ax_EMG3)
//       {
//        // Act mode 2 (pin out 9, green) 
//        digitalWrite(graspPin2, HIGH);
//        digitalWrite(graspPin1, LOW);
//        delay(2000);
//        }
//        else
//       {
//        // Rest mode
//        digitalWrite(graspPin2, LOW);
//        digitalWrite(graspPin1, LOW);
//       }
//       }
}
