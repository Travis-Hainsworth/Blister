%% Test Setup

clear all;
clc;

% DEFINE THESE VALUES
model_name = 'line_92';      % Input model name
year = 2020;                 % Input model year
manufacturer = "K2";         % Input ski Manufacturer
model_length_cm = 197;       %   Input Length of ski in cm
test_interval_mm = 5;       % Input the desired distance between data points in mm (multiples of 5 work best)
test_type = 'loaded';        % Test Type (string that is either loaded, unloaded, or torsion)

% Serial USB connections
arudiuno_port = 'COM3';     % write in arduino port
inclinometer_port_front = 'COM12';  % write in inclometer port
inclinometer_port_back = 'COM11'

force_gage1_port = 'COM7';   % write in loadcell1 port
force_gage2_port = 'COM8';   % write in loadcell2 port

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
flush(s);
clear s;
%%
arduino_port = 'COM3';
%s=serialport(arudiuno_port,115200);
pause(2);
serial_string_move_data_points = strcat(num2str(MOVE_X),",",num2str(test_interval_mm),",1");
flush(s);
writeline(s,serial_string_move_data_points);
pause(1);
disp("waiting");
waitfor(s, "NumBytesAvailable");
readData = readline(s);
flush(s);
disp(readData)


serial_string = strcat(num2str(GET_CURRENT_POSITION),",0,1");
%
message = serial_string;
flush(s);
writeline(s,message);
pause(1);
ret_mm = readline(s);
flush(s);
disp(ret_mm);
%%
s=serialport(arudiuno_port,115200); 
pause(2);

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
%the bellow code needs to use the same serial port
%clear s will reset the code on arduino
%%
arduino_port = 'COM6';
s=serialport(arduino_port,115200); 
pause(2);
%%
%FUNCTION TO MOVE SENSORS TO A SPECIFIC DISTANCE THAT IS MEASURED IN MM, COULD PAIR WELL WITH GET CURRENT POSTIION FUNCTION 
distance_in = 19;
distance_mm = floor(254);%floor(convlength([distance_in 0], 'in', 'm'));
direction = 0;
sig = move_x_mm(distance_mm, direction, s);
disp(sig);

%%
%FUNCTION TO GET CURRENT POSITION
%"command,#,#"
mm = get_distance_from_start(s);
disp(mm);

%%
%FUNCTION TO SET CURRENT POSITION
%"command,#,#" most likely = "signal,0,#"
position = 0;
sig = set_current_position(position, s );
disp(sig); 

%%
%FUNCTION TO GET CURRENT POSITION
%"command,#,#"
mm = get_distance_from_start(s);
disp(mm);

%%
%FUNCTION TO MOVE SENSORS TO A SPECIFIC DISTANCE THAT IS MEASURED IN MM, COULD PAIR WELL WITH GET CURRENT POSTIION FUNCTION 
distance_in = 19;
distance_mm = floor(30);%floor(convlength([distance_in 0], 'in', 'm'));
direction = 0;
sig = move_x_mm(distance_mm, direction, s);
disp(sig);

%%
%FUNCTION TO GET CURRENT POSITION
%"command,#,#"
mm = get_distance_from_start(s);
disp(mm);

%%
%FUNCTION TO MOVE TO START FROM CURRENT POSITION
%"command,#,#"
sig = return_to_start(s);
disp(sig);

%%
%FUNCTION TO GET CURRENT POSITION
%"command,#,#"
mm = get_distance_from_start(s);
disp(mm);
%%

clear s;
clc;

%%
arduino_port = 'COM6';
s=serialport(arduino_port,115200); 
pause(2);
distance_mm = 10;
direction = 0;
stop_num = 0;
while stop_num~=42
    %collect data
    sig = move_x_mm(distance_mm, direction, s);
    disp(sig);
    stop_num = str2double(sig);
end
pause(5);
mm1 = get_distance_from_start(s);
disp("mm1");
disp(mm1);
sig = return_to_start(s);
disp(sig);
mm2 = get_distance_from_start(s);
disp("mm2");
disp(mm2);
clear s;

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