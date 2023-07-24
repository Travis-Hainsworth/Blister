#include <AccelStepper.h>
#include <MultiStepper.h>
#include <ezButton.h>

#define DIR_PIN          11      // Direction - GREEN
#define STEP_PIN         12      // Step - BLUE

#define DIR_PIN_R          8      // Direction
#define STEP_PIN_R         9      // Step

#define DIR_PIN_L         4      // Direction
#define STEP_PIN_L         5      // Step

#define LIMIT_SWITCH_PIN_2 3
#define LIMIT_SWITCH_PIN_1 2

AccelStepper inclinometer_stepper (AccelStepper::DRIVER, STEP_PIN, DIR_PIN);
AccelStepper left_stepper (AccelStepper::DRIVER, STEP_PIN_L, DIR_PIN_L);
AccelStepper right_stepper (AccelStepper::DRIVER, STEP_PIN_R, DIR_PIN_R);
MultiStepper steppers; 

ezButton limitSwitchObj(LIMIT_SWITCH_PIN_2);

float stepsPerRevolution_inclinometer = 200*4;   // change this to fit the number of steps per revolution
float stepsPerRevolution_force_guages = 200*4;
const float lead_distance = 5;//distance in mm that one full turn of lead screw

volatile boolean kill_switch_pressed;

void setup() {
  Serial.begin(115200);               // initialize hardware serial for debugging

  inclinometer_stepper.setMaxSpeed(4500); //pulse/steps per second
  inclinometer_stepper.setAcceleration(4500); //steps per second per second to accelerate
  inclinometer_stepper.setCurrentPosition(0);
  inclinometer_stepper.setMinPulseWidth(30);

  limitSwitchObj.setDebounceTime(200);

  int force_guage_maxV_and_accel = 4500;

  left_stepper.setMaxSpeed(force_guage_maxV_and_accel); //pulse/steps per second
  left_stepper.setAcceleration(force_guage_maxV_and_accel); //steps per second per second to accelerate
  left_stepper.setCurrentPosition(0);
  left_stepper.setMinPulseWidth(30);
  
  right_stepper.setMaxSpeed(force_guage_maxV_and_accel); //pulse/steps per second
  right_stepper.setAcceleration(force_guage_maxV_and_accel); //steps per second per second to accelerate
  right_stepper.setCurrentPosition(0);
  right_stepper.setMinPulseWidth(30);
  
  attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN_2), stop_testing, FALLING);
  attachInterrupt(digitalPinToInterrupt(LIMIT_SWITCH_PIN_1), killed_switch_triggered, FALLING);

  steppers.addStepper(left_stepper);
  steppers.addStepper(right_stepper);

  kill_switch_pressed = false;
}

const int STOP_SIGNAL = 42;
const int KILL_SWITCH_SIGNAL = 86;

void killed_switch_triggered(){
    delayMicroseconds(20000);
    int buttonState = digitalRead(LIMIT_SWITCH_PIN_1);
    if (buttonState == LOW){
      kill_switch_pressed = true;
      inclinometer_stepper.stop();
      left_stepper.stop();
      right_stepper.stop();
      send_finish_signal(KILL_SWITCH_SIGNAL);
    }
}

void stop_testing(){
    delayMicroseconds(20000);
    int buttonState = digitalRead(LIMIT_SWITCH_PIN_2);
    if (buttonState == LOW) {
      inclinometer_stepper.stop();
      send_finish_signal(STOP_SIGNAL);
    }
}

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
const int MOVE_FORCE_GAUGES = 24;
const int COMMAND_NOT_RECOGNIZED = 101;

void loop() {
    limitSwitchObj.loop();
    if (Serial.available() > 0 && ~kill_switch_pressed){
          String message = Serial.readStringUntil("\n");
          Serial.flush();

          int numValues = 3;
          int message_arr[numValues];
          parse_serial_input(message, numValues, message_arr); 
          int command = message_arr[0];

          switch (command) {
            case MOVE_X:
            {
              //"command,distance_mm,#" negative distance means go towards back, and postive ditance is move towards front
              float length_mm = (float) message_arr[1];
              long steps = convert_distance_from_mm_to_steps(stepsPerRevolution_inclinometer, length_mm, lead_distance);
              move_x_steps(steps);
              send_finish_signal(MOVE_X);
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
            case RESET_ARDUINO:
            {
              //"command,#,#"
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
    }else{
      send_finish_signal(KILL_SWITCH_SIGNAL);
      kill_switch_pressed = false;
    }
}

void send_finish_signal(int sig){
    Serial.flush();
    Serial.println(sig);
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
  char buffer[inputString.length() + 1];
  inputString.toCharArray(buffer, inputString.length() + 1);

  char *ptr = NULL;
  byte index = 0;
  ptr = strtok(buffer, ",");  
  while (ptr != NULL){
    message_arr[index] = String(ptr).toInt();
    index++;
    ptr = strtok(NULL, ",");
  } 
}
