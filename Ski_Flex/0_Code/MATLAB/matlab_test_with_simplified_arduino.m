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
arudiuno_port = 'COM6';     % write in arduino port
inclinometer_port = 'COM12';  % write in inclometer port
force_gage1_port = 'COM5';   % write in loadcell1 port
force_gage2_port = 'COM6';   % write in loadcell2 port

% Motor build parameters don't change
change_per_rev = 5;          %  How many milimeters a single revolution of the stepper motor moves sensor along lead screw
seconds_per_rev = 2.5;         % Roughly how many seconds it takes stepper to complete one revolution ()

% setup
data_matrix = zeros(0, 4); 
pause_time = get_pause_time(test_interval_mm, change_per_rev, seconds_per_rev);

% RUN TEST (SINGLE SIDE, SINGLE INCLINOMETER)
s=serialport(arudiuno_port,115200); 
pause(2);
stop_num=0;
%count = 0;


while stop_num~=42

    serial_string = strcat("2,",num2str(test_interval_mm),",1");
    %disp(serial_string);
    pause(2);
    %writedata = string(uint16(test_interval_mm)); % 0x01F4
    flush(s);
    writeline(s,serial_string);
    pause(1);
    waitfor(s, "NumBytesAvailable");
    readData2 = readline(s);
    %disp(readData2);
    flush(s);
    stop_num = str2num(readData2);
    % count = count + 1;
    disp("stop number:");
    disp(stop_num);
    % disp("number of rotations");
    % disp(stop_num/(200*8));
    % disp("numer of steps for test at this point");
    % disp(stop_num);
    % disp("");
  
end
% data_matrix(end,:) = []; 

flush(s);
clear s;
