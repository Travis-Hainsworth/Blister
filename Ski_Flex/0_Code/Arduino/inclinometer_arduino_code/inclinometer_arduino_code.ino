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
#define LIMIT_SWITCH_PIN 2

SoftwareSerial SoftSerial(SW_RX, SW_TX);
TMC2209Stepper TMCdriver(&SoftSerial, R_SENSE, DRIVER_ADDRESS);

AccelStepper stepper1 (1, STEP_PIN, DIR_PIN);
ezButton limitSwitchObj(LIMIT_SWITCH_PIN);

const float stepsPerRevolution = 200*8;   // change this to fit the number of steps per revolution
const float lead_distance = 5;//distance in mm that one full turn of lead screw

volatile boolean testing_state = true;

int number_steps_for_test;
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
  
  attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN), stop_testing, FALLING); //digitalPinToInterrupt(LIMIT_SWITCH_PIN)

  number_steps_for_test = 0;
  count = 0;
}

void stop_testing(){
    stepper1.stop();
    testing_state = false;
    //delay(100);
    //move_x_steps((long) -stepper1.currentPosition());
    byte sig = 42;
    Serial.flush();
    Serial.println(sig);
    testing_state = false; 
    detachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN));   
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

const int TEST = 2;
const int MOVE_X = 4;

void loop() {
    if (Serial.available() > 0){
          count+=1;
          //limitSwitchObj.loop(); // MUST call the loop() function first

          String message = Serial.readStringUntil("\n");
          
          //String message = "4,32000,0";
          int numValues = 3;
          int message_arr[numValues];
          parse_serial_input(message, numValues, message_arr); 
          int signal = message_arr[0];

          // int message_arr[3] = {2,10,1}; // test for the testing logic procedure
          // int message_arr[3] = {4,3200,0}; // test for the move_x logic procedure
          //int signal = message_arr[0];//message_arr[0];

          switch (signal) {
            case TEST:
            {
              // Serial.println("IN TEST PROCEDURE");
              float distance_between_data_points = (float) message_arr[1];
              long direction = get_direction(message_arr[2]);
              test_logic(distance_between_data_points, direction);
              break;
            }
            case MOVE_X:
            {
              long num_steps = (long) message_arr[1];
              long dir = get_direction(message_arr[2]);
              // Serial.flush();
              // Serial.println(num_steps);
              move_x_steps(dir*abs(num_steps));
              //delay(10000);
              Serial.flush();//exit(1);
              break;
            }
            // case SET_CURRENT_POS:
            // {
            //   stepper1.setCurrentPosition(message_arr[0]);
            //   break;
            // }
            default:
            {
              //Serial.println("In default section of switch stament");
              break;
            }
          }  
    }
}

void test_logic(float length_between_data_points, long direction){
  if (testing_state){
      //float length_between_data_points = 10;//signal_dis.toFloat();//desired distance in mm between each datapoint 
      long steps2 = direction*abs(length_between_data_points_to_SP_steps(stepsPerRevolution, length_between_data_points, lead_distance));
      number_steps_for_test += steps2;
      //stepper_status();
      move_x_steps(steps2);
      stepper1.stop();
      Serial.flush();
      Serial.println(stepper1.currentPosition());
  }else if(testing_state == false){
      // detachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN));
      //stepper_status();
      move_x_steps((long) -stepper1.currentPosition());
      //stepper1.stop();
      byte sig = 42;
      Serial.flush();
      Serial.println(sig);
      //stepper1.stop()
      //delay(10000);
      //stepper1.setCurrentPosition(0);
      Serial.flush();//exit(1);
  }
}

long get_direction(int dir){
  if(dir == 0){return (long) 1;}
  else        {return (long) -1;}
}

int length_between_data_points_to_SP_steps(float spr, float length_between_data, float lead_distance){
      float num_rotations = length_between_data / lead_distance;
      float num_steps = spr * num_rotations;
      return (long) num_steps;
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
