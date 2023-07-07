 %%BELLOW
%THE CODE BELOW IS TO TEST THAT SERIAL COMMUNCATION BETWEEN MATLAB AND
%ARDUINO WILL WORK WITH THE LONGER MESAAGES THAT NEED TO BE PARSED
% /*
% * ALL CODE BELLOW CONCERNS THE LOOP LOGIC OF RUNNIGN A TEST  
% * ALSO THIS HAS SOME COMMANDS AND CAN EXPAND NEW COMMANDS FOR OTHER PROCEDURES
% * THE SERIAL MESSAGE COMES IN THE FORM OF 3 COMMA SEPERATED INTEGERS
%     * FOR THE TEST PROCECUDURE IT 
%       * PASSES "COMMAND,DISTANCE_BETWEEN_DATA_POINTS,DIRECTION"
%       * COMMAND = 2 = TEST
%       * DISTANCE_BETWEEN_DATA_POINTS = DESIRED DISTANCE BETWEEN EACH DATA POINT IN MILLI-METERS
%       * DIRECTION: 0 = MULTIPLY BY 1 = CLOCKWISE = FROM CENTER TO THE FRONT, 1 = MULTIPLY BY -1 = COUNTERCLOCKWISE = FROM THE FRONT TO THE CENTER
%     * FOR MOVE_X THIS PROCEDURE JUST MOVES THE STEPPER A DESIRED NUMBER OF STEPS (MIGHT BE CHANGED TO A DISTANCE OF MILLI-METERES)
%       * PASSES "COMMAND,DISRED_STEPS,DIRECTION"
%       * COMMAND = 4 = MOVE_X
%       * DISIRED_STEPS = DESIRED STEPS TO MOVE
%       * DIRECTION: 0 = MULTIPLY BY 1 = CLOCKWISE = FROM CENTER TO THE FRONT, 1 = MULTIPLY BY -1 = COUNTERCLOCKWISE = FROM THE FRONT TO THE CENTER
% *
% */
%%
clc;
arduino_port = 'COM6'; %need to change for arduino port recognized
s=serialport(arduino_port,115200);
pause(2);
message1 = "2,10,1";
writeline(s,message1);
pause(5);
% flush(s);
clear s;

%%
arduino_port = 'COM6'; %need to change for arduino port recognized
s=serialport(arduino_port,115200);
pause(2);
message1 = "2,5,0";
iterations = 10;

for c = 1:iterations
   flush(s);
   writeline(s,message1);
   pause(5);
   res = readline(s);
   flush(s);
   disp(res);
end
clear s;
%%
flush(s);
clear all;
clc;
%%
% BELLOW
%INITIAL FEEEDBACK LOOP FOR ADJUSTING FORCE GAUGES
%
%


%%
% This will be the initial distance, find average force between most
% flexible ski and least felxible then convert force > distance > steps
% move both steppers to this position
% Serial USB connections

global arudiuno_port inclinometer_port_front inclinometer_port_back force_gage1_port force_gage2_port;
global arudiuno_serial inclinometer_front_serial inclinometer_back_serial force_gage1_serial force_gage2_serial;

arudiuno_port = 'COM3';     % write in arduino port
% inclinometer_port_front = 'COM9';  % write in front inclometer port
inclinometer_port_back = 'COM14';  % write in back inclometer port
force_gage1_port = 'COM8';   % write in loadcell1 port
force_gage2_port = 'COM7';   % write in loadcell2 port

arudiuno_serial = serialport(arudiuno_port, 115200);
inclinometer_front_serial = serialport(inclinometer_port_front, 9600);
inclinometer_back_serial = serialport(inclinometer_port_back, 9600);
force_gage1_serial = serialport(force_gage1_port, 9600);
force_gage2_serial = serialport(force_gage2_port, 9600);

[pitchFront, rollFront] = get_HWT905TTL_data(inclinometer_front_serial);
tollerance_angel = .01;

while ~(rollFront < tollerance_angel && rollFront > -tollerance_angel)
    message = make_message(int2str(MOVE_BOTH_FORCE_GAUGES),actual_force_left, desired_force, precision);
    message = make_message(message, actual_force_right, desired_force, message);
    
    [pitchFront, rollFront] = get_HWT905TTL_data(inclinometer_front_serial);
end 


%%
%define max step size 
% function precentage_of_step = find_precentage_of_step_to_adjust_force_gauge()
% 
% end


%%
function ret_mm = return_to_start(s)
    MOVE_TO_START = 2;
    serial_string = strcat(num2str(MOVE_TO_START),",0,1");
    ret_mm = serial_communication(s, serial_string);
    flush(s);
end 

function ret_signal = move_x_mm(dis_mm, dir, s)
    MOVE_X = 4;
    serial_string = strcat(num2str(MOVE_X),",",num2str(dis_mm),",",num2str(dir));
    ret_signal = serial_communication(s, serial_string);
    flush(s);
end

function ret_signal = move_force_gauges(left_mm, right_mm)
    MOVE_FORCE_GAUGES = 24;
    serial_string = strcat(num2str(MOVE_FORCE_GAUGES),",",num2str(left_mm),",",num2str(right_mm));
    ret_signal = serial_communication(s, serial_string);
    flush(s);
end

function ret_signal = level_force_gauges(actual_angle, desired_angle, precision)
    MOVE_FORCE_GAUGES = 24;
    message = make_message(int2str(MOVE_FORCE_GAUGES),actual_angle, desired_angle, precision);
    message = make_message(message, actual_angle, desired_angle, message);
    ret_signal = serial_communication(s, message);
    flush(s);
end

function message = make_message(m, actual_angle, desired_angle, precision)
    message = m;
    if actual_angle <= desired_angle+precision && actual_angle >= desired_angle-precision % make this a fuction that takes in actual and desired, concatenates and retruns message
          message = strcat(message,',0');
    elseif actual_angle < desired_angle
          message = strcat(message,',1'); 
    else
          message = strcat(message,',-1'); 
    end 
end

function ret_mm = get_distance_from_start(s)
    GET_CURRENT_POSITION = 14;
    serial_string = strcat(num2str(GET_CURRENT_POSITION),",0,1");
    %ret_mm = serial_communication(s, serial_string);
    custom_write(s, serial_string);
    ret_mm = custom_read(s);
    flush(s);
end 

function ret_signal = set_current_position(pos,s)
    SET_CURRENT_POS = 6;
    serial_string = strcat(num2str(SET_CURRENT_POS),",",num2str(pos),",0");
    %ret_signal = serial_communication(s, serial_string);
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end

function ret_signal = set_stepsPerRev(stepsPerRev, s)
    SET_STEPS_PER_REVOLUTION = 12;
    serial_string = strcat(num2str(SET_STEPS_PER_REVOLUTION),",",num2str(stepsPerRev),",0");
    %ret_signal = serial_communication(s, serial_string);
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end

function ret_signal = set_acceleration(acceleration, s)
    SET_ACCELERATION = 10;
    serial_string = strcat(num2str(SET_ACCELERATION),",",num2str(acceleration),",0");
    %ret_signal = serial_communication(s, serial_string);
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end

function ret_signal = set_max_speed(max_speed,s)
    SET_MAX_SPEED = 8;
    serial_string = strcat(num2str(SET_MAX_SPEED),",",num2str(max_speed),",0");
    %ret_signal = serial_communication(s, serial_string);
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end

function ret_signal = reset_arduino(s)
    RESET_ARDUINO = 16;
    serial_string = strcat(num2str(RESET_ARDUINO),",0,0");
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end

function ret_signal = reset_testing_state(s)
    RESET_TESTING_STATE = 22;
    serial_string = strcat(num2str(RESET_TESTING_STATE),",0,0");
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end


function ret_signal = reattach_interrupt(s)%ls is the back or front limit switch (0 = back, 1 = front)
    REATTACH_INTERUPT = 18;
    serial_string = strcat(num2str(REATTACH_INTERUPT),",0,0");
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end

function ret_signal = deattach_interrupt(s)%ls is the back or front limit switch (0 = back, 1 = front)
    DEATTACH_INTERUPT = 20;
    serial_string = strcat(num2str(DEATTACH_INTERUPT),",0,0");
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end


function sig = serial_communication(s, message)
    custom_write(s,message);
    pause(1);
    disp("wait");
    waitfor(s, "NumBytesAvailable");
    sig = custom_read(s);
end

function custom_write(s, message)
    flush(s);
    writeline(s,message);
end

function out = custom_read(s)
    out = readline(s);
    flush(s);
end


%%
% %FUNCTION TO MAKE COMMA SEPERTAED MESSAGE FOR SERIAL COMMUNCATION FOR
% %FEEDBACK LOOP LOGIC
% 
% s=serialport(arduino_port,9600);
% 
% desired_angle = 20;
% actual_angle_left = 5; %read current sensor, will probably be the move to desired point
% precision = 0.5;
% 
% MOVE_BOTH_FORCE_GAUGES = 2;
% while ~(actual_angle_right <= desired_angle+precision && actual_angle_right >= desired_angle-precision) && ~(actual_angle_left <= desired_angle+precision && actual_angle_left >= desired_angle-precision)
%     message = make_message(int2str(MOVE_BOTH_FORCE_GAUGES),actual_force_left, desired_force, precision);
%     message = make_message(message, actual_force_right, desired_force, message);
%     flush(s);
%     writeline(s,message);
%     pause(.05);
%    %end
% end