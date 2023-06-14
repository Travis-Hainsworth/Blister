%%BELLOW
%THE CODE BELOW IS TO TEST THAT SERIAL COMMUNCATION BETWEEN MATLAB AND
%ARDUINO WILL WORK WITH THE LONGER MESAAGES THAT NEED TO BE PARSED
%%
arduino_port = 'COM5'; %need to change for arduino port recognized
s=serialport(arduino_port,115200);
%%
message1 = "2,0,100";

iterations = 10;

for c = 1:100
   flush(s);
   writeline(s,message1);
   pause(5);
   res = readline(s);
   flush(s);
   disp(res);
end
%%
fluBsh(s);
clear all;
clc;
%%
% BELLOW
%INITIAL FEEEDBACK LOOP FOR ADJUSTING FORCE GAUGES
%
%
%%
%FUNCTION TO MAKE COMMA SEPERTAED MESSAGE FOR SERIAL COMMUNCATION FOR FEED
%BACK LOOP LOGIC
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
%%
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