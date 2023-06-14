#include <AccelStepper.h>
#include <MultiStepper.h>
//#include <ezButton.h>
#include <SoftwareSerial.h>
#include <TMCStepper.h>

#define EN_PIN_R           4      // Enable
#define DIR_PIN_R          5      // Direction
#define STEP_PIN_R         6      // Step
#define SW_SCK_R           7      // Software Slave Clock (SCK)
#define SW_TX_R            A2      // SoftwareSerial receive pi
#define SW_RX_R            A3      // SoftwareSerial transmit pin

#define EN_PIN_L           8      // Enable
#define DIR_PIN_L          9      // Direction
#define STEP_PIN_L         10      // Step
#define SW_SCK_L           11     // Software Slave Clock (SCK)
#define SW_TX_L            A0      // SoftwareSerial receive pin
#define SW_RX_L            A1      // SoftwareSerial transmit pin

#define DRIVER_ADDRESS_R   0b00   // TMC2209 Driver address according to MS1 and MS2
#define DRIVER_ADDRESS_L  0b01   //figure this out ?????????????????????????????????
#define R_SENSE          0.11f  // SilentStepStick series use 0.11 ...and so does my fysetc TMC2209 (?)
//#define LIMIT_SWITCH_PIN 2

// SoftwareSerial SoftSerial_R(SW_RX_R, SW_TX_R);
// TMC2209Stepper TMCdriver_R(&SoftSerial_R, R_SENSE, DRIVER_ADDRESS_R);

// SoftwareSerial SoftSerial_L(SW_RX_L, SW_TX_L);
// TMC2209Stepper TMCdriver_L(&SoftSerial_L, R_SENSE, DRIVER_ADDRESS_L);

AccelStepper left_stepper (AccelStepper::DRIVER, STEP_PIN_L, DIR_PIN_L);
int left_steps;
int unloaded_left_steps;
AccelStepper right_stepper (AccelStepper::DRIVER, STEP_PIN_R, DIR_PIN_R);
int right_steps; //number of steps from complete rest (might be a load downward)
int unloaded_right_steps;//number of steps from unloaded rpofile of ski to the loaded state.
//ezButton limitSwitchObj(LIMIT_SWITCH_PIN);
MultiStepper steppers;

const float stepsPerRevolution = 200*8; // change this to fit the number of steps per revolution
const float lead_distance = 5; //distance in mm that one full turn of lead screw

volatile boolean max_force_state = true;

const int MOVE_BOTH_FORCE_GAUGES = 2;
const int MOVE_LEFT_FORCE_GAUGE = 3;
const int MOVE_RIGHT_FORCE_GAUGE = 4;

void setup() {
  Serial.begin(115200);               // initialize hardware serial for debugging
  // SoftSerial_R.begin(115200);           // initialize software serial for UART motor control
  // TMCdriver_R.beginSerial(115200); // Initialize UART
  // SoftSerial_L.begin(115200);           // initialize software serial for UART motor control
  // TMCdriver_L.beginSerial(115200); // Initialize UART
 
  left_stepper.setMaxSpeed(1000); //pulse/steps per second
  left_stepper.setAcceleration(500.0); //steps per second per second to accelerate
  //stepper1.setSpeed(1000); //pulse/steps per second
  left_stepper.setCurrentPosition(0);
  
  right_stepper.setMaxSpeed(1000); //pulse/steps per second
  right_stepper.setAcceleration(500.0); //steps per second per second to accelerate
  //stepper1.setSpeed(1000); //pulse/steps per second
  right_stepper.setCurrentPosition(0);

  // TMCdriver_R.begin();                                                                                                                                                                                                                                                                                                                            // UART: Init SW UART (if selected) with default 115200 baudrate
  // TMCdriver_R.toff(5);                 // Enables driver in software
  // TMCdriver_R.microsteps(0);         // Set microsteps
  // //TMCdriver_R.intpol(true);
  // TMCdriver_R.en_spreadCycle(false);
  // TMCdriver_R.pwm_autoscale(true);     // Needed for stealthChop
  
  // TMCdriver_L.begin();                                                                                                                                                                                                                                                                                                                            // UART: Init SW UART (if selected) with default 115200 baudrate
  // TMCdriver_L.toff(5);                 // Enables driver in software
  // TMCdriver_L.microsteps(0);         // Set microsteps
  // //TMCdriver_L.intpol(true);
  // TMCdriver_L.en_spreadCycle(false);
  // TMCdriver_L.pwm_autoscale(true);     // Needed for stealthChop

  //attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN), stop_testing, FALLING); //digitalPinToInterrupt(LIMIT_SWITCH_PIN)

  steppers.addStepper(left_stepper);
  steppers.addStepper(right_stepper);

  left_steps = 0;
  unloaded_left_steps = 0;
  right_steps = 0;
  unloaded_left_steps = 0;
}

//stepBackward conterclockwise rotation
//stepForward clockwise rotation 
//setPinsInverted  

// serial print variable type
void types(String a) { Serial.println("it's a String"); }
void types(int a) { Serial.println("it's an int"); }
void types(char *a) { Serial.println("it's a char*"); }
void types(float a) { Serial.println("it's a float"); }
void types(bool a) { Serial.println("it's a bool"); }

void parse_serial_input(String inputString, int& numValues, int* message_arr){
  //// convert String to char*
  char buffer[inputString.length() + 1];
  inputString.toCharArray(buffer, inputString.length() + 1);

  //// parse out comma seprated values
  char *ptr = NULL;
  byte index = 0;
  ptr = strtok(buffer, ",");  // delimiter
  while (ptr != NULL){
    message_arr[index] = String(ptr).toInt();//-'0';
    index++;
    ptr = strtok(NULL, ",");
  }
  
}

void move_x_steps(int left_steps, int right_steps){
  // left_stepper.move(left_steps);
  // right_stepper.move(right_steps);
  // int longest;
  // if(abs(left_steps)>=abs(right_steps)){
  //     while (left_stepper.distanceToGo() != 0) {
  //           left_stepper.run();
  //           right_stepper.run();
  //     }
  // }else{
  //     while (right_stepper.distanceToGo() != 0) {
  //           right_stepper.run();
  //           left_stepper.run();
  //     }
  // }
  long positions[2]; // Array of desired stepper positions
  positions[0] = left_steps;
  positions[1] = right_steps;
  steppers.moveTo(positions);
  steppers.runSpeedToPosition(); // Blocks until all are in position
  left_stepper.setCurrentPosition(0);
  right_stepper.setCurrentPosition(0);
}

void loop() {
  //limitSwitchObj.loop(); // MUST call the loop() function first
  if (Serial.available() > 0){
    String message = Serial.readStringUntil('\n');
    int numValues = 3;
    int message_arr[numValues];
    parse_serial_input(message, numValues, message_arr); 
    int signal = message_arr[0];  

    switch (signal) {
      case MOVE_BOTH_FORCE_GAUGES:
        Serial.flush();
        Serial.println("in move both force gauges");
        move_x_steps(message_arr[1],message_arr[2]);
        //move both x steps
        break;
      case MOVE_LEFT_FORCE_GAUGE:
        //get input from turn nob
        //move left stepper number of steps according to nob
              //might be usefull to have matlab read this input from a diffrent arduino board then pass in the number of corresponding steps
        break;
      case MOVE_RIGHT_FORCE_GAUGE:
        //get input from turn nob
        //move right stepper number of steps according to nob
              //might be usefull to have matlab read this input from a diffrent arduino board then pass in the number of corresponding steps
        break;
      default:
        break;
        //move_x_steps(signal_arr[2]);
    }
  
  }

}











