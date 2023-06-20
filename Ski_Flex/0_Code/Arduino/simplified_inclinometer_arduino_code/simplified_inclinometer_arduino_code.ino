#include <AccelStepper.h>
#include <ezButton.h>
#include <SoftwareSerial.h>
#include <TMCStepper.h>
//#include <Streaming.h>


//#define EN_PIN         GND      // Enable - RED
#define DIR_PIN          5      // Direction - GREEN
#define STEP_PIN         4      // Step - BLUE
#define SW_SCK           7      // Software Slave Clock (SCK) - YELLOW
#define SW_TX            1      // SoftwareSerial receive pin - GREY
#define SW_RX            0      // SoftwareSerial transmit pin - ORANGE
#define DRIVER_ADDRESS   0b00   // TMC2209 Driver address according to MS1 and MS2
#define R_SENSE          0.11f  // SilentStepStick series use 0.11 ...and so does my fysetc TMC2209 (?)
#define LIMIT_SWITCH_PIN_1 2
#define LIMIT_SWITCH_PIN_2 3
// #define LIMIT_SWITCH_PIN_3 4
// #define LIMIT_SWITCH_PIN_4 5


SoftwareSerial SoftSerial(SW_RX, SW_TX);
TMC2209Stepper TMCdriver(&SoftSerial, R_SENSE, DRIVER_ADDRESS);

AccelStepper stepper1 (1, STEP_PIN, DIR_PIN);
ezButton limitSwitchObj(LIMIT_SWITCH_PIN_1);

float stepsPerRevolution = 200*8;   // change this to fit the number of steps per revolution
const float lead_distance = 5;//distance in mm that one full turn of lead screw

volatile boolean testing_state = true;

int stepper1_current_position;
int count;

void setup() {
  Serial.begin(115200);               // initialize hardware serial for debugging
  //SoftSerial.begin(9600);           // initialize software serial for UART motor control
  //TMCdriver.beginSerial(9600); // Initialize UART

  //limitSwitchObj.setDebounceTime(200);
  

  stepper1.setMaxSpeed(1500); //pulse/steps per second
  stepper1.setAcceleration(750); //steps per second per second to accelerate
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
  
  attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN_1), stop_testing, FALLING); //digitalPinToInterrupt(LIMIT_SWITCH_PIN)
  // attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN_2), stop_testing, FALLING);
  // attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN_3), stop_testing, FALLING);
  // attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN_4), stop_testing, FALLING);

  stepper1_current_position = 0;
  count = 0;
}

const int STOP_SIGNAL = 42;

void stop_testing(){
    stepper1.stop();
    //testing_state = false;
    send_finish_signal(STOP_SIGNAL);
    detachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN_1));   
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

const int MOVE_TO_START = 2;
const int MOVE_X = 4;
const int SET_CURRENT_POS = 6;
const int SET_MAX_SPEED = 8;
const int SET_ACCELERATION = 10;
const int SET_STEPS_PER_REVOLUTION = 12;
const int GET_CURRENT_POSITION = 14;
const int COMMAND_NOT_RECOGNIZED = 101;

void loop() {
    if (Serial.available() > 0){
          count+=1;
          //limitSwitchObj.loop(); // MUST call the loop() function first

          String message = Serial.readStringUntil("\n");
          Serial.flush();
          
          //String message = "4,32000,0";
          int numValues = 3;
          int message_arr[numValues];
          parse_serial_input(message, numValues, message_arr); 
          int command = message_arr[0];

          // int message_arr[3] = {2,10,1}; // test for the testing logic procedure
          // int message_arr[3] = {4,3200,0}; // test for the move_x logic procedure
          //int signal = message_arr[0];//message_arr[0];

          switch (command) {
            case MOVE_X:
            {
              //"command,distance_mm,direction"
              float length_mm = (float) message_arr[1];
              long direction = get_direction(message_arr[2]);
              long steps = direction*abs(convert_distance_from_mm_to_steps(stepsPerRevolution, length_mm, lead_distance));
              stepper1_current_position+= (int) steps;
              move_x_steps(steps);
              send_finish_signal(steps);
              break;
            }
            case MOVE_TO_START:
            {
              //"command,#,#"
              long steps_from_start = stepper1.currentPosition();
              move_x_steps(-1*steps_from_start);
              send_finish_signal(convert_distance_from_steps_to_mm(stepsPerRevolution, steps_from_start, lead_distance));
              break;
            }
            case SET_CURRENT_POS:
            {
              //"command,#,#" most likely = "signal,0,#"
              long position = (long) message_arr[1];
              stepper1.setCurrentPosition(position);
              send_finish_signal(SET_CURRENT_POS);
              break;
            }
            case SET_MAX_SPEED:
            {
              //"command,max_speed,#"
              float max_speed = (float) message_arr[1];
              stepper1.setMaxSpeed(max_speed);
              send_finish_signal(SET_MAX_SPEED);
            }
            case SET_ACCELERATION:
            {
              //"command,acceleration,#"
              float acceleration = (float) message_arr[1];
              stepper1.setAcceleration(acceleration);
              send_finish_signal(SET_ACCELERATION);
            }
            case SET_STEPS_PER_REVOLUTION:
            {
              //"command,max_speed,#"
              float steps_per_rev = (float) message_arr[1];
              stepsPerRevolution = steps_per_rev;
              send_finish_signal(SET_STEPS_PER_REVOLUTION);
            }
            case GET_CURRENT_POSITION:
            {
              //"command,#,#"
              long current_position = stepper1.currentPosition();
              int current_position_in_mm = convert_distance_from_steps_to_mm(stepsPerRevolution, current_position, lead_distance);
              send_finish_signal(current_position_in_mm);
            }
            default:
            {
              //Serial.println("In default section of switch stament");
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
  stepper1.move(x);
  //stepper1.runSpeedToPosition();
  while (stepper1.distanceToGo() != 0){
      stepper1.run();
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
      Serial.println(abs((float) stepper1.currentPosition()/(200.0*8.0)));
      delay(10);
      Serial.println("number of steps for test at this point");
      delay(10);
      Serial.println(stepper1.currentPosition());
      delay(10);
      Serial.println("\n---------------------------------------\n");
      delay(10);
}
