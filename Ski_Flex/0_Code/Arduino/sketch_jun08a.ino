#include <AccelStepper.h>
#include <ezButton.h>
#include <SoftwareSerial.h>
#include <TMCStepper.h>
//#include <Streaming.h>
​
​
#define EN_PIN           4      // Enable - RED
#define DIR_PIN          5      // Direction - GREEN
#define STEP_PIN         6      // Step - BLUE
#define SW_SCK           7      // Software Slave Clock (SCK) - YELLOW
#define SW_TX            8      // SoftwareSerial receive pin - GREY
#define SW_RX            9      // SoftwareSerial transmit pin - ORANGE
#define DRIVER_ADDRESS   0b00   // TMC2209 Driver address according to MS1 and MS2
#define R_SENSE          0.11f  // SilentStepStick series use 0.11 ...and so does my fysetc TMC2209 (?)
#define LIMIT_SWITCH_PIN 2
​
SoftwareSerial SoftSerial(SW_RX, SW_TX);
TMC2209Stepper TMCdriver(&SoftSerial, R_SENSE, DRIVER_ADDRESS);
​
AccelStepper stepper1 (1, STEP_PIN, DIR_PIN);
ezButton limitSwitchObj(LIMIT_SWITCH_PIN);
​
const float stepsPerRevolution = 200*8;   // change this to fit the number of steps per revolution
const float lead_distance = 5;//distance in mm that one full turn of lead screw
​
volatile boolean testing_state = true;
​
int number_steps_for_test;
​
void setup() {
  Serial.begin(9600);               // initialize hardware serial for debugging
  SoftSerial.begin(9600);           // initialize software serial for UART motor control
  TMCdriver.beginSerial(9600);      // Initialize UART
​
  stepper1.setMaxSpeed(1000); //pulse/steps per second
  stepper1.setAcceleration(500.0); //steps per second per second to accelerate
  //stepper1.setSpeed(1000); //pulse/steps per second
  stepper1.setCurrentPosition(0);
  //stepper1._direction = 1;
​
  // pinMode(EN_PIN, OUTPUT);           // Set pinmodes
  // pinMode(STEP_PIN, OUTPUT);
  // pinMode(DIR_PIN, OUTPUT);
  // digitalWrite(EN_PIN, LOW);         // Enable TMC2209 board 
​
  TMCdriver.begin();                                                                                                                                                                                                                                                                                                                            // UART: Init SW UART (if selected) with default 115200 baudrate
  TMCdriver.toff(5);                 // Enables driver in software
  //TMCdriver.rms_current(500);        // Set motor RMS current
  TMCdriver.microsteps(0);         // Set microsteps
  TMCdriver.intpol(true);
  TMCdriver.en_spreadCycle(false);
  TMCdriver.pwm_autoscale(true);     // Needed for stealthChop
​
  //define pins as outputs/inputs
    pinMode(EN_PIN, OUTPUT);
    pinMode(STEP_PIN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);

  
  attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN), stop_testing, CHANGE); //digitalPinToInterrupt(LIMIT_SWITCH_PIN)
​
  number_steps_for_test = 0;
}
​
void loop() {
  // int count = 0;
  // while(count!=200*8*2){
  //   digitalWrite(STEP_PIN, !digitalRead(STEP_PIN)); 
  //   delay(1);
  //   count+=1;
  // }
  // exit(1);
​
  //limitSwitchObj.loop(); // MUST call the loop() function first
  if (testing_state && Serial.available() > 0){
    String hexString = Serial.readStringUntil('\n');
    Serial.flush();
    // Convert the hex string to decimal
    long decimalValue = strtol(hexString.c_str(), NULL, 16);
    
​
    if(decimalValue == 1280){
      float length_between_data_points = 5;//desired distance in mm between each datapoint 
      int steps2 = length_between_data_points_to_SP_steps(stepsPerRevolution, length_between_data_points, lead_distance);
      number_steps_for_test += steps2;
      move_x_steps(-steps2);
      stepper1.stop();
      byte signal = 0;
      Serial.flush();
      Serial.println(signal,HEX);
    }
  }else if(!testing_state){
      // Serial.print('move back');
      byte signal = 42;
      Serial.flush();
      Serial.println(signal,HEX); //print data
      stepper1.stop();
      move_x_steps(number_steps_for_test);
      stepper1.stop();
      exit(1);
      
  }
}
​
void stop_testing(){
    testing_state = !testing_state;     
}
​
int length_between_data_points_to_SP_steps(float spr, float length_between_data, float lead_distance){
      float num_rotations = length_between_data / lead_distance;
      float num_steps = spr * num_rotations;
      return (int) num_steps;
}
​
void move_x_steps(int x){
  stepper1.move(x);
  while (stepper1.distanceToGo() != 0) {
            stepper1.run();
  }
}
