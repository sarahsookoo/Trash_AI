//Utilizing an A4988 motor driver and a NEMA17 motor

//Setting up what is equivalent to a variable, but for arduino

#define stepPinn 3 //Pin 3 will be used for rotation speed of the motor (steps)
#define directionPinn 4 //Pin 4 will be used for the direction of the motor (this involves polarity)

// Motor Connections (Both must use PWM pins)
#define RPWM 5
#define LPWM 6

// defines pins numbers
const int stepPin = 3; 
const int dirPin = 4; 

void setup(){ //one time execution
  pinMode(stepPinn, OUTPUT); //step pin will only be sending signals OUT, not receiving any 
  pinMode(directionPinn, OUTPUT); //direction pin will only be sending signals OUT, not receiving any 

  // Set motor connections as outputs
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);

  // Stop motors
  analogWrite(RPWM, 0);
  analogWrite(LPWM, 0);
  //Receive signal from rasperry pi to change one of the integers to a 1

  //Bin Selection
  int binOne = 0;
  int binTwo = 0;
  int binThree = 0;
}

void loop(){ //instantly repeated execution after setup
  digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for(int x = 0; x < 200; x++) {
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
}



 

  /*
  TO BE DONE:
  - Move the motor back to its original position after initial rotation
      + Reverse direction (polarity) and move the same amount 

  - Implement serial communication between rasperry pi and arduino 
    for material type communication

  - Push actuator forward and then pull back

  - Apparnetly there's a library for stepper motors, can I use it 

  - Wire and power all of this
  */

