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
%FUNCTION TO MAKE COMMA SEPERTAED MESSAGE FOR SERIAL COMMUNCATION FOR
%FEEDBACK LOOP LOGIC

s=serialport(arduino_port,9600);

desired_force = 20;
actual_force_left = 5; %read current sensor, will probably be the move to desired point
actual_force_right = 5;
precision = 0.5;

MOVE_BOTH_FORCE_GAUGES = 2;
while ~(actual_force_right <= desired_force+precision && actual_force_right >= desired_force-precision) && ~(actual_force_left <= desired_force+precision && actual_force_left >= desired_force-precision)
    message = make_message(int2str(MOVE_BOTH_FORCE_GAUGES),actual_force_left, desired_force, precision);
    message = make_message(message, actual_force_right, desired_force, message);
    flush(s);
    writeline(s,message);
    pause(.05);
   %end
end

%%
% This will be the initial distance, find average force between most
% flexible ski and least felxible then convert force > distance > steps
% move both steppers to this position


function message = make_message(m, actual_force, desired_force,precision)
    message = m;
    if actual_force <= desired_force+precision && actual_force >= desired_force-precision % make this a fuction that takes in actual and desired, concatenates and retruns message
          message = strcat(message,',0');
    elseif actual_force < desired_force
          message = strcat(message,',1'); 
    else
          message = strcat(message,',-1'); 
    end 
end