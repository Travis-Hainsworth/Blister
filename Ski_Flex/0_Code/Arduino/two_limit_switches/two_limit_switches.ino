#include <AccelStepper.h>
#include <ezButton.h>
#include <SoftwareSerial.h>
#include <TMCStepper.h>
//#include <Streaming.h>


//#define EN_PIN           4      // Enable - RED
#define DIR_PIN          5      // Direction - GREEN
#define STEP_PIN         4      // Step - BLUE
#define SW_SCK           7      // Software Slave Clock (SCK) - YELLOW
#define SW_TX            1      // SoftwareSerial receive pin - GREY
#define SW_RX            0      // SoftwareSerial transmit pin - ORANGE
#define DRIVER_ADDRESS   0b00   // TMC2209 Driver address according to MS1 and MS2
#define R_SENSE          0.11f  // SilentStepStick series use 0.11 ...and so does my fysetc TMC2209 (?)
#define LIMIT_SWITCH_PIN 2
#define LIMIT_SWITCH_PIN_2 3


SoftwareSerial SoftSerial(SW_RX, SW_TX);
TMC2209Stepper TMCdriver(&SoftSerial, R_SENSE, DRIVER_ADDRESS);

AccelStepper stepper1 (1, STEP_PIN, DIR_PIN);
ezButton limitSwitchObj(LIMIT_SWITCH_PIN);
ezButton limitSwitchObj_2(LIMIT_SWITCH_PIN_2);

const float stepsPerRevolution = 200*8;   // change this to fit the number of steps per revolution
const float lead_distance = 5;//distance in mm that one full turn of lead screw

volatile boolean testing_state = true;
volatile int direction = -1;

int number_steps_for_test;
int count;

void setup() {
  Serial.begin(9600);               // initialize hardware serial for debugging
  //SoftSerial.begin(9600);           // initialize software serial for UART motor control
  //TMCdriver.beginSerial(9600); // Initialize UART

  //limitSwitchObj.setDebounceTime(200);
  

  stepper1.setMaxSpeed(1500); //pulse/steps per second
  stepper1.setAcceleration(500); //steps per second per second to accelerate
  stepper1.setCurrentPosition(0);
  stepper1.setMinPulseWidth(30);


  TMCdriver.begin();                                                                                                                                                                                                                                                                                                                            // UART: Init SW UART (if selected) with default 115200 baudrate
  TMCdriver.toff(5);                 // Enables driver in software
  TMCdriver.rms_current(2500);       // Set motor RMS current
  TMCdriver.microsteps(1);            // Set microsteps to 1/2
  TMCdriver.pwm_autoscale(true);     // Needed for stealthChop
  TMCdriver.en_spreadCycle(false);

  //define pins as outputs/inputs
//    pinMode(EN_PIN, OUTPUT);
//    pinMode(STEP_PIN, OUTPUT);
//    pinMode(DIR_PIN, OUTPUT);
  // pinMode(cClockPed, INPUT_PULLUP);
  // pinMode(ClockPed, INPUT_PULLUP);    
  // pinMode(dEncdrSpdCLK, INPUT_PULLUP);
  // pinMode(dEncdrSpdDT, INPUT_PULLUP);


  // while(!Serial);                  // Wait for port to be ready

  // TMCdriver.pdn_disable(1);              // Use PDN/UART pin for communication
  // TMCdriver.I_scale_analog(0);           // Adjust current from the registers
  // TMCdriver.rms_current(500);            // Set driver current 500mA
  // TMCdriver.toff(0x2);               // Enable driver

  // digitalWrite(EN_PIN, LOW);
  
  attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN), switch_dir_1, FALLING); //digitalPinToInterrupt(LIMIT_SWITCH_PIN)
  attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN_2), switch_dir_2, FALLING);

  number_steps_for_test = 0;
  count = 0;
}

void switch_dir_1(){
  stepper1.stop();
  delay(1000);
  direction = 1;
  testing_state = false;
}

void switch_dir_2(){
  stepper1.stop();
  delay(1000);
  direction = -1;
  testing_state = true;
}

void loop() {
  count+=1;
  if (testing_state){
      float length_between_data_points = 10;//signal_dis.toFloat();//desired distance in mm between each datapoint 
      int steps2 = direction*length_between_data_points_to_SP_steps(stepsPerRevolution, length_between_data_points, lead_distance);
      //number_steps_for_test += steps2;
      move_x_steps(steps2);
      stepper_status();
  } else{
      move_x_steps(direction*stepper1.currentPosition());
  }
}

void stepper_status(){
      Serial.println("direction:");
      delay(10);
      Serial.println(direction);
      delay(10);
      Serial.println("number of datapoints");
      delay(10);
      Serial.println(count);
      delay(10);
      Serial.println("number of rotations");
      delay(10);
      Serial.println(stepper1.currentPosition()/(200*8));
      delay(10);
      Serial.println("number of steps for test at this point");
      delay(10);
      Serial.println(stepper1.currentPosition());
      delay(10);
      Serial.println("\n---------------------------------------\n");
      delay(10);
}

void stop_testing(){
    testing_state = false;
    stepper1.stop();
    delay(100);
    //move_x_steps((long) -stepper1.currentPosition());
//    byte sig = 42;
//    Serial.flush();
//    Serial.println(-stepper1.currentPosition());
    testing_state = false; 
    detachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN));   
}

int length_between_data_points_to_SP_steps(float spr, float length_between_data, float lead_distance){
      float num_rotations = length_between_data / lead_distance;
      float num_steps = spr * num_rotations;
      return (int) num_steps;
}

void move_x_steps(int x){
  stepper1.move(x);
    //stepper1.runSpeedToPosition();
  while (stepper1.distanceToGo() != 0){
            stepper1.run();
  }
}
