#include <AccelStepper.h>
#include <MultiStepper.h>
#include <ezButton.h>
#include <SoftwareSerial.h>
#include <TMCStepper.h>


//#define EN_PIN         GND      // Enable - RED
#define DIR_PIN          11      // Direction - GREEN
#define STEP_PIN         12      // Step - BLUE
// #define SW_SCK           7      // Software Slave Clock (SCK) - YELLOW
// #define SW_TX            1      // SoftwareSerial receive pin - GREY
// #define SW_RX            0      // SoftwareSerial transmit pin - ORANGE

// #define EN_PIN_R           4      // Enable
#define DIR_PIN_R          8      // Direction
#define STEP_PIN_R         9      // Step
// #define SW_SCK_R           7      // Software Slave Clock (SCK)
// #define SW_TX_R            A2      // SoftwareSerial receive pi
// #define SW_RX_R            A3      // SoftwareSerial transmit pin

// #define EN_PIN_L           8      // Enable
#define DIR_PIN_L         4      // Direction
#define STEP_PIN_L         5      // Step
// #define SW_SCK_L           11     // Software Slave Clock (SCK)
// #define SW_TX_L            A0      // SoftwareSerial receive pin
// #define SW_RX_L            A1      // SoftwareSerial transmit pin

// #define DRIVER_ADDRESS_INCLINOMTER   0b00   // TMC2209 Driver address according to MS1 and MS2
// #define DRIVER_ADDRESS_R   0b01   // TMC2209 Driver address according to MS1 and MS2
// #define DRIVER_ADDRESS_L  0b10   //figure this out ?????????????????????????????????
// #define R_SENSE          0.11f  // SilentStepStick series use 0.11 ...and so does my fysetc TMC2209 (?)

// #define LIMIT_SWITCH_PIN_1 2
#define LIMIT_SWITCH_PIN_2 3

// SoftwareSerial SoftSerial(SW_RX, SW_TX);
// TMC2209Stepper TMCdriver(&SoftSerial, R_SENSE, DRIVER_ADDRESS_INCLINOMETER);

AccelStepper inclinometer_stepper (AccelStepper::DRIVER, STEP_PIN, DIR_PIN);
AccelStepper left_stepper (AccelStepper::DRIVER, STEP_PIN_L, DIR_PIN_L);
AccelStepper right_stepper (AccelStepper::DRIVER, STEP_PIN_R, DIR_PIN_R);
MultiStepper steppers; 

ezButton limitSwitchObj(LIMIT_SWITCH_PIN_2);

float stepsPerRevolution_inclinometer = 200*4;   // change this to fit the number of steps per revolution
float stepsPerRevolution_force_guages = 200*4;
const float lead_distance = 5;//distance in mm that one full turn of lead screw

volatile boolean testing_state;
int count;

void setup() {
  Serial.begin(115200);               // initialize hardware serial for debugging

  inclinometer_stepper.setMaxSpeed(4500); //pulse/steps per second
  inclinometer_stepper.setAcceleration(4500); //steps per second per second to accelerate
  inclinometer_stepper.setCurrentPosition(0);
  inclinometer_stepper.setMinPulseWidth(30);

  limitSwitchObj.setDebounceTime(200);
  // TMCdriver.begin();                                                                                                                                                                                                                                                                                                                            // UART: Init SW UART (if selected) with default 115200 baudrate
  // TMCdriver.toff(5);                 // Enables driver in software
  // TMCdriver.rms_current(2500);       // Set motor RMS current
  // TMCdriver.microsteps(1);            // Set microsteps to 1/2
  // TMCdriver.pwm_autoscale(true);     // Needed for stealthChop
  // TMCdriver.en_spreadCycle(false);

  int force_guage_maxV_and_accel = 4500;

  left_stepper.setMaxSpeed(force_guage_maxV_and_accel); //pulse/steps per second
  left_stepper.setAcceleration(force_guage_maxV_and_accel); //steps per second per second to accelerate
  //stepper1.setSpeed(1000); //pulse/steps per second
  left_stepper.setCurrentPosition(0);
  left_stepper.setMinPulseWidth(30);
  
  right_stepper.setMaxSpeed(force_guage_maxV_and_accel); //pulse/steps per second
  right_stepper.setAcceleration(force_guage_maxV_and_accel); //steps per second per second to accelerate
  //stepper1.setSpeed(1000); //pulse/steps per second
  right_stepper.setCurrentPosition(0);
  right_stepper.setMinPulseWidth(30);

  // TMCdriver.begin();                                                                                                                                                                                                                                                                                                                            // UART: Init SW UART (if selected) with default 115200 baudrate
  // TMCdriver.toff(5);                 // Enables driver in software
  // TMCdriver.rms_current(2500);       // Set motor RMS current
  // TMCdriver.microsteps(1);            // Set microsteps to 1/2
  // TMCdriver.pwm_autoscale(true);     // Needed for stealthChop
  // TMCdriver.en_spreadCycle(false);
  
  attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN_2), stop_testing, FALLING);

  steppers.addStepper(left_stepper);
  steppers.addStepper(right_stepper);

  count = 0;
  testing_state = true;
}

const int STOP_SIGNAL = 42;

void stop_testing(){
    delayMicroseconds(20000);
    int buttonState = digitalRead(LIMIT_SWITCH_PIN_2);
    if (buttonState == LOW) {
      inclinometer_stepper.stop();
      //testing_state = false;
      send_finish_signal(STOP_SIGNAL);
    }
}

/*
* ALL CODE BELLOW CONCERNS THE LOOP LOGIC OF RUNNIGN A TEST  
* ALSO THIS HAS SOME COMMANDS AND CAN EXPAND NEW COMMANDS FOR OTHER PROCEDURES
* THE SERIAL MESSAGE COMES IN THE FORM OF 3 COMMA SEPERATED INTEGERS
    * FOR THE TEST PROCECUDURE IT 
      * PASSES "COMMAND,DISTANCE_BETWEEN_DATA_POINTS,DIRECTION"
      * COMMAND = 2 = TEST
      * DISTANCE_BETWEEN_DATA_POINTS = DESIRED DISTANCE BETWEEN EACH DATA POINT IN MILLI-METERS
      * DIRECTION: 0 = MULIPLY BY 1 = CLOCKWISE = FROM CENTER TO THE FRONT, 1 = MULIPLY BY -1 = COUNTERCLOCKWISE = FROM THE FRONT TO THE CENTER
    * FOR MOVE_X THIS PROCEDURE JUST MOVES THE STEPPER A DESIRED NUMBER OF STEPS (MIGHT BE CHANGED TO A DISTANCE OF MILLI-METERES)
      * PASSES "COMMAND,DISRED_STEPS,DIRECTION"
      * COMMAND = 4 = MOVE_X
      * DISIRED_STEPS = DESIRED STEPS TO MOVE
      * DIRECTION: 0 = MULIPLY BY 1 = CLOCKWISE = FROM CENTER TO THE FRONT, 1 = MULIPLY BY -1 = COUNTERCLOCKWISE = FROM THE FRONT TO THE CENTER
*
*/

void types(String a) { Serial.println("it's a String"); }
void types(int a) { Serial.println("it's an int"); }
void types(char *a) { Serial.println("it's a char*"); }
void types(float a) { Serial.println("it's a float"); }
void types(bool a) { Serial.println("it's a bool"); }

const int MOVE_TO_START = 2;
const int MOVE_X = 4;
const int SET_CURRENT_POS = 6;
const int SET_MAX_SPEED = 8;
const int SET_ACCELERATION = 10;
const int SET_STEPS_PER_REVOLUTION = 12;
const int GET_CURRENT_POSITION = 14;
const int RESET_ARDUINO = 16;
// const int REATTACH_INTERUPT = 18;
// const int DEATTACH_INTERUPT = 20;
// const int SET_ENABLE_SWITCH = 22;
// const int GET_ENABLE_SWITCH = 24;
const int MOVE_FORCE_GAUGES = 24;
const int GET_TESTING_STATE = 26;
// const int STOP_SIGNAL = 42;
const int COMMAND_NOT_RECOGNIZED = 101;

void loop() {
    limitSwitchObj.loop();
    if (Serial.available() > 0){
          count+=1;
          String message = Serial.readStringUntil("\n");
          Serial.flush();
          
          // String message = "10,750,0"; // working
          // String message = "24,0,0"; //  working
          // String message = "22,1,0"; // working
          // String message = "4,25,0"; // working
          // delay(1000);
          // String message = "24,100,100"; // working

          int numValues = 3;
          int message_arr[numValues];
          parse_serial_input(message, numValues, message_arr); 
          int command = message_arr[0];

          switch (command) {
            case MOVE_X:
            {
              //"command,distance_mm,#" negative distance means go towards back, and postive ditance is move towards front
              float length_mm = (float) message_arr[1];
              // Serial.println(length_mm);
              //long direction = get_direction(message_arr[2]);
              // Serial.println(direction);
              //long steps = direction*abs(convert_distance_from_mm_to_steps(stepsPerRevolution_inclinometer, length_mm, lead_distance));
              long steps = convert_distance_from_mm_to_steps(stepsPerRevolution_inclinometer, length_mm, lead_distance);
              //stepper1_current_position+= (int) steps;
              move_x_steps(steps);
              send_finish_signal(steps);
              break;
            }
            case MOVE_FORCE_GAUGES:
            {
              delay(2000);
              //"command,distance_mm,direction"
              float left_sensor_move_mm = (float) message_arr[1];
              long left_steps = convert_distance_from_mm_to_steps(stepsPerRevolution_force_guages, left_sensor_move_mm, lead_distance);
              float right_sensor_move_mm = (float) message_arr[2];
              long right_steps = convert_distance_from_mm_to_steps(stepsPerRevolution_force_guages, right_sensor_move_mm, lead_distance);

              int longest;
              left_stepper.move(left_steps);
              right_stepper.move(right_steps);
              if(abs(left_steps)>=abs(right_steps)){
                  while (left_stepper.distanceToGo() != 0) {
                        left_stepper.run();
                        right_stepper.run();
                  }
              }else{
                  while (right_stepper.distanceToGo() != 0) {
                        right_stepper.run();
                        left_stepper.run();
                  }
              }

              // long positions[2]; // Array of desired stepper positions
              // positions[0] = left_steps;
              // positions[1] = right_steps;
              // steppers.moveTo(positions); //////////////////////////////////////// ONLY HAS MOVETO SO WOULD NEED TO RESET CURRENT POSITION TO 0 AFTER EACH MOVE THEN COUNT NUMBER OF STEPS WITH A COUNTER TO USE RETRUN TO START
              // steppers.runSpeedToPosition(); // Blocks until all are in position
              // left_stepper.setCurrentPosition(0);
              // right_stepper.setCurrentPosition(0);
              send_finish_signal(MOVE_FORCE_GAUGES);
              break;
            }
            case MOVE_TO_START:
            {
              //"command,#,#"
              long steps_from_start = inclinometer_stepper.currentPosition();
              move_x_steps(-1*steps_from_start);
              send_finish_signal(convert_distance_from_steps_to_mm(stepsPerRevolution_inclinometer, steps_from_start, lead_distance));
              break;
            }
            case SET_CURRENT_POS:
            {
              //"command,#,#" most likely = "signal,0,#"
              long position = (long) message_arr[1];
              inclinometer_stepper.setCurrentPosition(position);
              send_finish_signal(SET_CURRENT_POS);
              break;
            }
            case SET_MAX_SPEED:
            {
              //"command,max_speed,#"
              float max_speed = (float) message_arr[1];
              inclinometer_stepper.setMaxSpeed(max_speed);
              send_finish_signal(SET_MAX_SPEED);
              break;
            }
            case SET_ACCELERATION:
            {
              //"command,acceleration,#"
              // Serial.println("set acceleration");
              // Serial.println(message_arr[0]);
              // Serial.println(message_arr[1]);
              // Serial.println(message_arr[2]);
              float acceleration = (float) message_arr[1];
              inclinometer_stepper.setAcceleration(acceleration);
              send_finish_signal(SET_ACCELERATION);
              break;
            }
            case SET_STEPS_PER_REVOLUTION:
            {
              //"command,max_speed,#"
              float steps_size = (float) message_arr[1];
              stepsPerRevolution_inclinometer = steps_size*200;
              send_finish_signal(stepsPerRevolution_inclinometer);//SET_STEPS_PER_REVOLUTION);
              break;
            }
            case GET_CURRENT_POSITION:
            {
              //"command,#,#"
              long current_position = inclinometer_stepper.currentPosition();
              int current_position_in_mm = convert_distance_from_steps_to_mm(stepsPerRevolution_inclinometer, current_position, lead_distance);
              send_finish_signal(current_position_in_mm);
              break;
            }
            case GET_TESTING_STATE:
            {
              //"command,#,#"
              // long current_position = stepper1.currentPosition();
              // int current_position_in_mm = convert_distance_from_steps_to_mm(stepsPerRevolution_inclinometer, current_position, lead_distance);
              send_finish_signal(testing_state);
              break;
            }
            case RESET_ARDUINO:
            {
              setup();
              send_finish_signal(RESET_ARDUINO);
              break;
            }
            default:
            {
              send_finish_signal(COMMAND_NOT_RECOGNIZED);
              break;
            }
          }  
    }
}

void send_finish_signal(int sig){
    Serial.flush();
    Serial.println(sig);
}

long get_direction(int dir){
  if(dir == 0){return (long) 1;}
  else        {return (long) -1;}
}

long convert_distance_from_mm_to_steps(float spr, float length_mm, float lead_distance){
      float num_rotations = length_mm / lead_distance;
      float num_steps = spr * num_rotations;
      return (long) num_steps;
}

int convert_distance_from_steps_to_mm(float spr, float length_steps, float lead_distance){
      float num_rotations = length_steps / spr;
      float num_mm = num_rotations * lead_distance;
      return (int) num_mm;
}

void move_x_steps(long x){
  inclinometer_stepper.move(x);
  while (inclinometer_stepper.distanceToGo() != 0){
       inclinometer_stepper.run();
  }
}

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

void stepper_status(){
      Serial.println("number of datapoints");
      delay(10);
      Serial.println(count);
      delay(10);
      Serial.println("number of rotations");
      delay(10);
      Serial.println(abs((float) inclinometer_stepper.currentPosition()/(200.0*8.0)));
      delay(10);
      Serial.println("number of steps for test at this point");
      delay(10);
      Serial.println(inclinometer_stepper.currentPosition());
      delay(10);
      Serial.println("\n---------------------------------------\n");
      delay(10);
}
