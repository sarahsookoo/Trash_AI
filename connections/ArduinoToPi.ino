#include "HX711.h"

const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;

/*
Steps for weight Sensor setup & data to Pi.
    Connect HX711 to Arduino
    Install HX711 library
    Calibrate the scale (calibration factor)
    Get weight with get_units
    Send data with println
    Source - https://randomnerdtutorials.com/arduino-load-cell-hx711/
*/
HX711 scale(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN); // Creates a HX711 scale
// or HX711 scale;
// scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

void setup() {
  Serial.begin(9600);
  scale.set_scale(-459.542); // Set the calibration factor (this value is an example, you should calibrate your scale)
  scale.tare(); // Reset the scale to 0
}

void loop() {
  float weight = scale.get_units(5); // Read the weight value and average over 5 readings
  Serial.println(weight, 2); // send weight to Pi
  delay(1000); // Safety delay of 1sec

    while (Serial.available() > 0) {
        String classification = Serial.readString();

        // Print the message to the serial monitor
        Serial.println(classification);

        // RUN Actuator code here
  }
}

/*
CODE TO CALIBRATE THE SCALE


void setup() {
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
}

void loop() {

  if (scale.is_ready()) {
    scale.set_scale();    
    Serial.println("Tare... remove any weights from the scale.");
    delay(5000);
    scale.tare();
    Serial.println("Tare done...");
    Serial.print("Place a known weight on the scale...");
    delay(5000);
    long reading = scale.get_units(10);
    Serial.print("Result: ");
    Serial.println(reading);
  } 
  else {
    Serial.println("HX711 not found.");
  }
  delay(1000);
}
*/
