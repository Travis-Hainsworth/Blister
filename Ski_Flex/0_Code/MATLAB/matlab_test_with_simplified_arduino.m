%% Test Setup

clear all;
clc;

% DEFINE THESE VALUES
model_name = 'line_92';      % Input model name
year = 2020;                 % Input model year
manufacturer = "K2";         % Input ski Manufacturer
model_length_cm = 197;       %   Input Length of ski in cm
test_interval_mm = 25;       % Input the desired distance between data points in mm (multiples of 5 work best)
test_type = 'loaded';        % Test Type (string that is either loaded, unloaded, or torsion)

% Serial USB connections
arudiuno_port = 'COM3';     % write in arduino port
inclinometer_port = 'COM12';  % write in inclometer port
force_gage1_port = 'COM5';   % write in loadcell1 port
force_gage2_port = 'COM6';   % write in loadcell2 port

% Motor build parameters don't change
change_per_rev = 5;          %  How many milimeters a single revolution of the stepper motor moves sensor along lead screw
seconds_per_rev = 2.5;         % Roughly how many seconds it takes stepper to complete one revolution ()

% setup
data_matrix = zeros(0, 4); 
%pause_time = get_pause_time(test_interval_mm, change_per_rev, seconds_per_rev);

% RUN TEST (SINGLE SIDE, SINGLE INCLINOMETER)
s=serialport(arudiuno_port,115200); 
pause(2);
stop_num=0;
%count = 0;

MOVE_TO_START = 2;
MOVE_X = 4;
SET_CURRENT_POS = 6;
SET_MAX_SPEED = 8;
SET_ACCELERATION = 10;
SET_STEPS_PER_REVOLUTION = 12;
GET_CURRENT_POSITION = 14;
COMMAND_NOT_RECOGNIZED = 101;

serial_string_move_data_points = strcat(num2str(MOVE_X),",",num2str(test_interval_mm),",1");

while stop_num~=42

    %collect data
    
    pause(2);

    flush(s);
    writeline(s,serial_string_move_data_points);
    pause(1);
    disp("waiting");
    waitfor(s, "NumBytesAvailable");
    readData = readline(s);
    flush(s);
    stop_num = str2num(readData);
    % count = count + 1;
    disp("stop number:");
    disp(stop_num);
end
% data_matrix(end,:) = []; 


serial_string_move_to_start = strcat(num2str(MOVE_TO_START),",1,0");
flush(s);
writeline(s,serial_string_move_data_points);
r = readline(s);
flush(s);
stop_num = str2num(r);
disp(r);

flush(s);
clear s;


%%
%FUNCTION TO MOVE SENSORS TO A SPECIFIC DISTANCE THAT IS MEASURED IN MM, COULD PAIR WELL WITH GET CURRENT POSTIION FUNCTION 
arduino_port = 'COM3';
distance_in = 19;
distance_mm = floor(457.2);%floor(convlength([distance_in 0], 'in', 'm'));
direction = 0;
sig = move_x_mm(distance_mm, direction, arduino_port);
disp(sig);

%%
%FUNCTION TO SET CURRENT POSITION
%"command,#,#" most likely = "signal,0,#"
position = 0;
arduino_port = 'COM3';
sig = set_current_position(position, arduino_port);
disp(sig); 

%%
%FUNCTION TO GET CURRENT POSITION
%"command,#,#"
arduino_port = 'COM3';
mm = get_current_position(arduino_port);
disp(mm);
%%
function ret_mm = get_current_position(arduino_port)
    GET_CURRENT_POSITION = 14;
    s=serialport(arduino_port,115200); 
    pause(2);
    serial_string = strcat(num2str(GET_CURRENT_POSITION),",-1,-1");
    flush(s);
    writeline(s,serial_string);
    pause(1);
    disp("wait");
    waitfor(s, "NumBytesAvailable");
    ret_mm = readline(s);
    flush(s);
    clear s;
end

function ret_signal = move_x_mm(dis_mm, dir, arduino_port)
    MOVE_X = 4;
    s=serialport(arduino_port,115200); 
    pause(2);
    serial_string = strcat(num2str(MOVE_X),",",num2str(dis_mm),",",num2str(dir));
    flush(s);
    writeline(s,serial_string);
    pause(1);
    disp("wait");
    waitfor(s, "NumBytesAvailable");
    ret_signal = readline(s);
    flush(s);
    clear s;
end

function ret_signal = set_current_position(pos,arduino_port)
    SET_CURRENT_POS = 6;
    s=serialport(arduino_port,115200); 
    pause(2);
    serial_string = strcat(num2str(SET_CURRENT_POS),",",num2str(pos),",0");
    flush(s);
    writeline(s,serial_string);
    pause(1);
    disp("wait");
    waitfor(s, "NumBytesAvailable");
    ret_signal = readline(s);
    flush(s);
    clear s;
end