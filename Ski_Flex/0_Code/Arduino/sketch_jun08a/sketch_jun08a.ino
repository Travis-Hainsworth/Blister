#include <AccelStepper.h>
#include <ezButton.h>
#include <SoftwareSerial.h>
#include <TMCStepper.h>
//#include <Streaming.h>

#define EN_PIN           GND      // Enable
#define DIR_PIN          5      // Direction
#define STEP_PIN         6      // Step
#define SW_SCK           7      // Software Slave Clock (SCK)
#define SW_TX            1      // SoftwareSerial receive pin
#define SW_RX            0      // SoftwareSerial transmit pin
#define DRIVER_ADDRESS   0b00   // TMC2209 Driver address according to MS1 and MS2
#define R_SENSE          0.11f  // SilentStepStick series use 0.11 ...and so does my fysetc TMC2209 (?)
#define LIMIT_SWITCH_PIN 2

SoftwareSerial SoftSerial(SW_RX, SW_TX);
TMC2209Stepper TMCdriver(&SoftSerial, R_SENSE, DRIVER_ADDRESS);

AccelStepper stepper1 (1, STEP_PIN, DIR_PIN);
ezButton limitSwitchObj(LIMIT_SWITCH_PIN);

const float stepsPerRevolution = 200*2;   // change this to fit the number of steps per revolution
const float lead_distance = 5; //distance in mm that one full turn of lead screw

volatile boolean testing_state = true;

int number_steps_for_test;

void setup() {
  Serial.begin(9600);               // initialize hardware serial for debugging
  SoftSerial.begin(9600);           // initialize software serial for UART motor control
  TMCdriver.beginSerial(9600);      // Initialize UART

  stepper1.setMaxSpeed(1000); //pulse/steps per second
  stepper1.setAcceleration(500.0); //steps per second per second to accelerate
  //stepper1.setSpeed(1000); //pulse/steps per second
  stepper1.setCurrentPosition(0);
  //stepper1._direction = 1;

  // pinMode(EN_PIN, OUTPUT);           // Set pinmodes
  // pinMode(STEP_PIN, OUTPUT);
  // pinMode(DIR_PIN, OUTPUT);
  // digitalWrite(EN_PIN, LOW);         // Enable TMC2209 board 

  //TMCdriver.rms_current(1.5/sqrt(2));    // motor RMS current "rms_current will by default set ihold to 50% of irun but you can set your own ratio with additional second argument; rms_current(1000, 0.3)."
  TMCdriver.microsteps(1);            // Set microsteps to 1/2
  // TMCdriver.semin(3);                 // [0... 15] If the StallGuard4 result falls below SEMIN*32, the motor current becomes increased to reduce motor load angle.
  // TMCdriver.semax(1);                 // [0... 15]  If the StallGuard4 result is equal to or above (SEMIN+SEMAX+1)*32, the motor current becomes decreased to save energy.
  // TMCdriver.sedn(4);                  // current down step speed 0-11%
  // TMCdriver.seup(2);                  // Current increment steps per measured StallGuard2 value 5 seup0 %00 … %11: 1, 2, 4, 8
  // TMCdriver.blank_time(24);
  // TMCdriver.iholddelay(3);           // 0 - 15 smooth current drop after stop
  TMCdriver.pwm_autoscale(true);    // Needed for stealthChop
  TMCdriver.en_spreadCycle(true);   // false = StealthChop / true = SpreadCycle

  // //define pins as outputs/inputs
  //   pinMode(EN_PIN, OUTPUT);
  //   pinMode(STEP_PIN, OUTPUT);
  //   pinMode(DIR_PIN, OUTPUT);

  
  attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN), stop_testing, CHANGE); //digitalPinToInterrupt(LIMIT_SWITCH_PIN)

  number_steps_for_test = 0;
}

void loop() {
  // int count = 0;
  // while(count!=200*8*2){
  //   digitalWrite(STEP_PIN, !digitalRead(STEP_PIN)); 
  //   delay(1);
  //   count+=1;
  // }
  // exit(1);

  //limitSwitchObj.loop(); // MUST call the loop() function first
  if (testing_state && Serial.available() > 0){
    String hexString = Serial.readStringUntil('\n');
    Serial.flush();
    // Convert the hex string to decimal
    long decimalValue = strtol(hexString.c_str(), NULL, 16);
    

    if(decimalValue == 1280){
      float length_between_data_points = 5;//desired distance in mm between each datapoint 
      int steps2 = length_between_data_points_to_SP_steps(stepsPerRevolution, length_between_data_points, lead_distance);
      number_steps_for_test += steps2;
      move_x_steps(-steps2);
      stepper1.stop();
      byte signal = 3;
      Serial.flush();
      Serial.println(signal);
    }
  }else if(!testing_state){
      // Serial.print('move back');
      stepper1.stop();
      move_x_steps(number_steps_for_test);
      stepper1.stop();
      byte signal = 42;
      Serial.flush();
      Serial.println(signal); //print data
      exit(1);
  }
}

void stop_testing(){
    byte signal = 42;
    Serial.flush();
    Serial.println(signal); //print data
    testing_state = false;

}

int length_between_data_points_to_SP_steps(float spr, float length_between_data, float lead_distance){
      float num_rotations = length_between_data / lead_distance;
      float num_steps = spr * num_rotations;
      return (int) num_steps;
}

void move_x_steps(int x){
  stepper1.move(x);
  while (stepper1.distanceToGo() != 0) {
            stepper1.run();
  }
}
