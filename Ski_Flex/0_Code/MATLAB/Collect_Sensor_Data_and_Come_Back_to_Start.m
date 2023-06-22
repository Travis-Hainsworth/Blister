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
%inclinometer_port_back = 'COM11';  % write in back inclometer port
force_gage1_port = 'COM8';   % write in loadcell1 port
force_gage2_port = 'COM7';   % write in loadcell2 port

% % Motor build parameters don't change
% change_per_rev = 5;          %  How many milimeters a single revolution of the stepper motor moves sensor along lead screw
% seconds_per_rev = 2.5;         % Roughly how many seconds it takes stepper to complete one revolution ()
% 
% setup
data_matrix_front = zeros(0, 4);
data_matrix_back = zeros(0, 4);
data_matrix = zeros(0,4);
% pause_time = get_pause_time(test_interval_mm, change_per_rev, seconds_per_rev);


%command_arduino = Commands_for_Arduino;

% RUN TEST (SINGLE SIDE, SINGLE INCLINOMETER)
s=serialport(arudiuno_port,115200); 
pause(2);
stop_num=0;
count = 0;
while stop_num~=42
    %collect data
    [pitchFront, rollFront] = get_HWT905TTL_data(inclinometer_port_front);
    % [pitchBack, rollBack] = get_HWT905TTL_data(inclinometer_port_back);

    [force1, force2]=force_average(force_gage1_port, force_gage2_port,1);

    disp(strcat("Inclometer front data: Pitch-", num2str(pitchFront), " Roll-", num2str(rollFront)));
    % disp(strcat("Inclometer back data: Pitch-", num2str(pitchBack), " Roll-", num2str(rollBack)));
    disp(strcat("Force gage readings: Gage1-", num2str(force1), " gage2-", num2str(force2)));

    row_entry_front = [pitchFront, rollFront, force1, force2];
    % row_entry_back = [pitchBack, rollBack, force1, force2];
    data_matrix_front = [data_matrix_front;row_entry_front];
    % data_matrix_back = [data_matrix_back;row_entry_back];
    % pause(2);
    %MOVE SENSOR
    sig = move_x_mm(test_interval_mm, direction, s);
    disp(sig);
    stop_num = str2double(sig);
  
end
%MOVE BACK TO START
pause(5);
mm1 = get_distance_from_start(s);
% disp("mm1 START: ");
% disp(mm1);
sig = return_to_start(s);
% disp(sig);
mm2 = get_distance_from_start(s);
% disp("mm2 END: ");
% disp(mm2);
flush(s);
clear s;

%%

force_gage1_port = 'COM7';   % write in loadcell1 port
force_gage2_port = 'COM8';   % write in loadcell2 port

[force1, force2]=force_average(force_gage1_port, force_gage2_port,1);
[pitchFront, rollFront] = get_HWT905TTL_data('COM9');



%% Get HWT905TTL pitch and roll data.

function [pitch, roll] = get_HWT905TTL_data(inclinometer_port)

    port=serialport(inclinometer_port,9600); %Open Com Port
    disp(inclinometer_port);
    f = 20;%DataFrequce
    aa=[0 0 0];
    ww=[0 0 0];
    AA = [0 0 0];
    t=0;
    tt = 0;
    a=[0 0 0]';
    w=[0 0 0]';
    A=[0 0 0]';
    while(1)
        Head = read(port,2,'uint8')';
        if (Head(1)==uint8(85))
            switch(Head(2))
                case 81 
                    a = read(port,3,'int16')'/32768*16 ;     
                    End = read(port,3,'uint8')';
                case 82 
                    w = read(port,3,'int16')'/32768*2000 ;    
                    End = read(port,3,'uint8')';
                case 83 
                    A = read(port,3,'int16')'/32768*180;
                    aa=[aa;a'];
                    ww = [ww;w'];
                    AA = [AA;A'];
                    tt = [tt;t];
    
                    disp(A(1));
                    disp(A(2));

                    pitch = A(2);
                    roll = A(1);
    
                    if (size(aa,1)>5*f)%clear history data
                        aa = aa(f:5*f,:);
                        ww = ww(f:5*f,:);
                        AA = AA(f:5*f,:);
                        tt = tt(f:5*f,:);
                    end
    
                    t=t+0.01;
                    End = read(port,3,'uint8')';

                    break
            end    
        end
    end
    clear port;
end

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

%% Force Gage Code
% reads force data from sensor (written by fin)

function [force1,force2] = force_data(portname1,portname2)
    %connects and reads first sensor
    serial1=serialport(portname1,9600); %connects to serial port 
    write(serial1,'?','string');        %queries serial port (required to obtain data)
    force1=read(serial1,5,"string");    %reads data point

    %connects and read second sensor
    serial2=serialport(portname2,9600); %connects to serial port
    write(serial2,'?','string');        %queries serial port (required to obtain data)
    force2=read(serial2,5,"string");    %reads data point

    %converts and outputs data for first sensor
    force1=strrep(force1,' ','');       %removes any spaces in read data
    force1=strrep(force1,'l','1');      %changes L to 1 (weird data read)
    force1=str2double(force1);          %converts data to double

    %converts and outputs data for second sensor
    force2=strrep(force2,' ','');       %removes any spaces in read data
    force2=strrep(force2,'l','1');      %changes L to 1 (weird data read)
    force2=str2double(force2);          %converts data to double

end

% gets the average force data (written by fin)

function [force1,force2] = force_average(portname1, portname2,average)
        
    for i=1:average
        [force1(i),force2(i)]=force_data(portname1,portname2);
    end

    force1=mean(force1);
    force2=mean(force2);
end

