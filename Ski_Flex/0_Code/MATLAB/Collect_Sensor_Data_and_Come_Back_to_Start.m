%%
%% Test Setup

clear all;
clc;

% DEFINE THESE VALUES
% model_name = 'line_92';      % Input model name
% year = 2020;                 % Input model year
% manufacturer = "K2";         % Input ski Manufacturer
% model_length_cm = 197;       %   Input Length of ski in cm
test_interval_mm = 15;       % Input the desired distance between data points in mm (multiples of 5 work best)
direction = 1;

% Serial USB connections
arudiuno_port = 'COM3';     % write in arduino port
inclinometer_port_front = 'COM9';  % write in front inclometer port
inclinometer_port_back = 'COM11';  % write in back inclometer port
force_gage1_port = 'COM7';   % write in loadcell1 port
force_gage2_port = 'COM8';   % write in loadcell2 port

% % Motor build parameters don't change
% change_per_rev = 5;          %  How many milimeters a single revolution of the stepper motor moves sensor along lead screw
% seconds_per_rev = 2.5;         % Roughly how many seconds it takes stepper to complete one revolution ()
% 
% setup
data_matrix_front = zeros(0, 4);
data_matrix_back = zeros(0, 4);
data_matrix = zeros(0,4);
% pause_time = get_pause_time(test_interval_mm, change_per_rev, seconds_per_rev);


command_arduino = Commands_for_Arduino;

% RUN TEST (SINGLE SIDE, SINGLE INCLINOMETER)
s=serialport(arudiuno_port,115200); 
pause(2);
stop_num=0;
count = 0;
while stop_num~=42
    %collect data
    [pitchFront, rollFront] = get_HWT905TTL_data(inclinometer_port_front);
    [pitchBack, rollBack] = get_HWT905TTL_data(inclinometer_port_back);

    [force1, force2]=force_average(force_gage1_port, force_gage2_port,1);

    disp(strcat("Inclometer front data: Pitch-", num2str(pitchFront), " Roll-", num2str(rollFront)));
    disp(strcat("Inclometer back data: Pitch-", num2str(pitchBack), " Roll-", num2str(rollBack)));
    disp(strcat("Force gage readings: Gage1-", num2str(force1), " gage2-", num2str(force2)));

    row_entry_front = [pitchFront, rollFront, force1, force2];
    row_entry_back = [pitchBack, rollBack, force1, force2];
    data_matrix_front = [data_matrix_front;row_entry_front];
    data_matrix_back = [data_matrix_back;row_entry_back];
    
    %MOVE SENSOR
    sig = command_arduino.move_x_mm(test_interval_mm, direction, s);
    disp(sig);
    stop_num = str2double(sig);
  
end
%MOVE BACK TO START
pause(5);
mm1 = command_arduino.get_distance_from_start(s);
% disp("mm1 START: ");
% disp(mm1);
sig = command_arduino.return_to_start(s);
% disp(sig);
mm2 = command_arduino.get_distance_from_start(s);
% disp("mm2 END: ");
% disp(mm2);
flush(s);
clear s;

%%
function ret_mm = return_to_start(obj, s)
            MOVE_TO_START = 2;
            serial_string = strcat(num2str(MOVE_TO_START),",0,1");
            ret_mm = serial_communication(s, serial_string);
            flush(s);
        end 
        
        function ret_signal = move_x_mm(obj, dis_mm, dir, s)
            MOVE_X = 4;
            serial_string = strcat(num2str(MOVE_X),",",num2str(dis_mm),",",num2str(dir));
            ret_signal = serial_communication(s, serial_string);
            flush(s);
        end
        
        function ret_mm = get_distance_from_start(obj, s)
            GET_CURRENT_POSITION = 14;
            serial_string = strcat(num2str(GET_CURRENT_POSITION),",0,1");
            %ret_mm = serial_communication(s, serial_string);
            write(s, serial_string);
            ret_mm = read(s);
            flush(s);
        end 
        
        function ret_signal = set_current_position(obj, pos,s)
            SET_CURRENT_POS = 6;
            serial_string = strcat(num2str(SET_CURRENT_POS),",",num2str(pos),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(s, serial_string);
            ret_signal = read(s);
            flush(s);
        end
        
        function ret_signal = set_stepsPerRev(obj, stepsPerRev, s)
            SET_STEPS_PER_REVOLUTION = 12;
            serial_string = strcat(num2str(SET_STEPS_PER_REVOLUTION),",",num2str(stepsPerRev),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(s, serial_string);
            ret_signal = read(s);
            flush(s);
        end
        
        function ret_signal = set_acceleration(obj, acceleration, s)
            SET_ACCELERATION = 10;
            serial_string = strcat(num2str(SET_ACCELERATION),",",num2str(acceleration),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(s, serial_string);
            ret_signal = read(s);
            flush(s);
        end
        
        function ret_signal = set_max_speed(obj, max_speed,s)
            SET_MAX_SPEED = 8;
            serial_string = strcat(num2str(SET_MAX_SPEED),",",num2str(max_speed),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(s, serial_string);
            ret_signal = read(s);
            flush(s);
        end
        
        function sig = serial_communication(obj, s, message)
            write(s,message);
            pause(1);
            disp("wait");
            waitfor(s, "NumBytesAvailable");
            sig = read(s);
        end
        
        function write(obj, s, message)
            flush(s);
            writeline(s,message);
        end
        
        function out = read(obj, s)
            out = readline(s);
            flush(s);
        end