//Utilizing an A4988 motor driver and a NEMA17 motor

//Setting up what is equivalent to a variable, but for arduino

#define stepPinn 3 //Pin 3 will be used for rotation speed of the motor (steps)
#define directionPinn 4 //Pin 4 will be used for the direction of the motor (this involves polarity)

// Motor Connections (Both must use PWM pins)
#define RPWM 5
#define LPWM 6

#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

// defines stepper pin numbers
const int stepPin = 3;
const int dirPin = 4;

//pins for weight sensor module:
const int HX711_dout = 8; //mcu > HX711 dout pin
const int HX711_sck = 9; //mcu > HX711 sck pin

//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
unsigned long t = 0;

bool checkForNewWeight = true;
float weight = 0;

void setup() {
  Serial.begin(9600);
  delay(10);
  pinMode(stepPinn, OUTPUT); //step pin will only be sending signals OUT, not receiving any
  pinMode(directionPinn, OUTPUT); //direction pin will only be sending signals OUT, not receiving any

  // Set motor connections as outputs
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);

  // Stop motors
  analogWrite(RPWM, 0);
  analogWrite(LPWM, 0);

  //Serial.println();
  //Serial.println("Starting...");

  //Loadcell code vv

  LoadCell.begin();
  //LoadCell.setReverseOutput(); //uncomment to turn a negative output value to positive
  float calibrationValue; // calibration value (see example file "Calibration.ino")
  calibrationValue = 696.0; // uncomment this if you want to set the calibration value in the sketch
#if defined(ESP8266)|| defined(ESP32)
  //EEPROM.begin(512); // uncomment this if you use ESP8266/ESP32 and want to fetch the calibration value from eeprom
#endif
  //EEPROM.get(calVal_eepromAdress, calibrationValue); // uncomment this if you want to fetch the calibration value from eeprom

  unsigned long stabilizingtime = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true; //set this to false if you don't want tare to be performed in the next step
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag()) {
    //Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell.setCalFactor(calibrationValue); // set calibration value (float)
    //Serial.println("Startup is complete");
  }
}

void loop() {
  if (checkForNewWeight == true){
    //Loadcell code
    static boolean newDataReady = 0;
    const int serialPrintInterval = 100; //increase value to slow down serial print activity

    // check for new data/start next conversion:
    if (LoadCell.update()) newDataReady = true;

    // get smoothed value from the dataset:
    if (newDataReady) {
      if (millis() > t + serialPrintInterval) {
        weight = LoadCell.getData();
        if (weight > 5){ //Minimum weight requirement
          //Serial.print("Load_cell output val: ");
          Serial.println(weight);
          checkForNewWeight = false;
        }
        newDataReady = 0;
        t = millis();
      }
    }
  }
  //IF WEIGHT IS > CERTAIN AMOUNT -> NEW OBJECT -> SET CHECKFORNEW TO FALSE

  //Pi to arduino communication -> movement of motors
   // Check for data on serial port (material type result from AI)
   if (Serial.available() > 0){ 
    int data = Serial.parseInt();
    
    
    // Based on material type, operate
    if(data == 0) {
       // Move to trash

        /*
        int value1 = 123; // Some integer value to send back to pi
        Serial.println(value1); // Send the value back to the computer as serial data
        */
        

        digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction

        // Makes 200 pulses for making one full cycle rotation (66 is 1/3 of full)

        for(int x = 0; x < 33; x++) { // Move stepper 1/3rd of the way counter-clockwise
          digitalWrite(stepPin,HIGH);
          delayMicroseconds(5000);
          digitalWrite(stepPin,LOW);
          delayMicroseconds(5000);
        }
        delay(3000);
        // Accelerate forward
        digitalWrite(LPWM, LOW);
        analogWrite(RPWM, 255);
       
        delay(4000);

        // Accelerate reverse
        digitalWrite(RPWM, LOW);
        analogWrite(LPWM, 255);

        delay(5000);
        delay(3000);

        digitalWrite(dirPin,LOW);
        for(int x = 0; x < 33; x++) { // Move stepper 1/3rd of the way clockwise
          digitalWrite(stepPin,HIGH);
          delayMicroseconds(5000);
          digitalWrite(stepPin,LOW);
          delayMicroseconds(5000);
        }
        delay(3000);
    }
    else if(data == 1){
        // Do something when '1' is received
        

        /*
        int value2 = 456; // Some integer value to send back
        Serial.println(value2); // Send the value back to the computer as serial data
        */


        digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction

        // Makes 200 pulses for making one full cycle rotation (66 is 1/3 of full)

        for(int x = 0; x < 99; x++) { // Move stepper 2/3rd of the way counter-clockwise
          digitalWrite(stepPin,HIGH);
          delayMicroseconds(5000);
          digitalWrite(stepPin,LOW);
          delayMicroseconds(5000);
        }
        delay(3000);
        // Accelerate forward
        digitalWrite(LPWM, LOW);
        analogWrite(RPWM, 255);
       
        delay(4000);

        // Accelerate reverse
        digitalWrite(RPWM, LOW);
        analogWrite(LPWM, 255);

        delay(5000);
        delay(3000);

        digitalWrite(dirPin,LOW);
        for(int x = 0; x < 99; x++) { // Move stepper 2/3rd of the way clockwise
          digitalWrite(stepPin,HIGH);
          delayMicroseconds(5000);
          digitalWrite(stepPin,LOW);
          delayMicroseconds(5000);
        }
        delay(3000);        
    }


    else if(data == 2){
        // Do something when '2' is received


        /*
        int value3 = 789; // Some integer value to send back
        Serial.println(value3); // Send the value back to the computer as serial data
        */


        digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction

        // Makes 200 pulses for making one full cycle rotation (66 is 1/3 of full)

        for(int x = 0; x < 165; x++) { // Move stepper 1/3rd of the way counter-clockwise
          digitalWrite(stepPin,HIGH);
          delayMicroseconds(5000);
          digitalWrite(stepPin,LOW);
          delayMicroseconds(5000);
        }
        delay(3000);
        // Accelerate forward
        digitalWrite(LPWM, LOW);
        analogWrite(RPWM, 255);
       
        delay(4000);

        // Accelerate reverse
        digitalWrite(RPWM, LOW);
        analogWrite(LPWM, 255);

        delay(5000);
        delay(3000);

        digitalWrite(dirPin,LOW);
        for(int x = 0; x < 165; x++) { // Move stepper 1/3rd of the way counter-clockwise
          digitalWrite(stepPin,HIGH);
          delayMicroseconds(5000);
          digitalWrite(stepPin,LOW);
          delayMicroseconds(5000);
        }
        delay(3000);        
       
      }
    
    checkForNewWeight = true; // Enable checking for new weight
    delay(10000);
   }
}
