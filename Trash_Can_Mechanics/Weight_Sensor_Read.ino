//Utilizing an A4988 motor driver and a NEMA17 motor

//Setting up what is equivalent to a variable, but for arduino

#define stepPin 3 //Pin 3 will be used for rotation speed of the motor (steps)
#define directionPin 4 //Pin 4 will be used for the direction of the motor (this involves polarity)

void setup(){ //one time execution
  pinMode(stepPin, OUTPUT); //step pin will only be sending signals OUT, not receiving any 
  pinMode(directionPin, OUTPUT); //direction pin will only be sending signals OUT, not receiving any 
  
  //Bin Selection
  int binOne = 0;
  int binTwo = 0;
  int binThree = 0;

  //Receive signal from rasperry pi to change one of the integers to a 1
}

void loop(){ //instantly repeated execution after setup
  digitalWrite(directionPin, HIGH); //clockwise rotation

  int i = 0;
  if(binOne = 1){
    i = 533 + 133; //Middle of bin 1
  }
  else if(binTwo = 1){
    i = 400; //Middle of bin 2
  }
  else{
    i = 133; //Middle of bin 3
  }
  for(i = i; i < 800; i++){ //one full rotation 
    digitalWrite(stepPin, HIGH); //Begin rotation
    delay(100); //wait 100 miliseconds before next step
    digitalWrite(stepPin, LOW); //Stop rotation
    delay(100); //wait 100 miliseconds before next step
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
}

