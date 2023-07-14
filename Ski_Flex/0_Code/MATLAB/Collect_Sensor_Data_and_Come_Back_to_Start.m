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
arudiuno_port = 'COM6';     % write in arduino port
inclinometer_port_front = 'COM11';  % write in front inclometer port
%inclinometer_port_back = 'COM11';  % write in back inclometer port
force_gage1_port = 'COM10';   % write in loadcell1 port
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

%%
clear all;
close all;
disp('Press Ctrl+C to stop collecting data!')              %按Ctrl+C,终止数据的获取
s=serialport('COM12',9600);               %请将COM44换成电脑识别到的COM口，波特率9600换成传感器对应的波特率    Please replace COM44 with the COM port recognized by the PC, and change the baud rate 9600 to the baud rate corresponding to the sensor
f = 20;         %DataFrequce
t=0;
cnt = 1;
aa=[0 0 0];     %加速度XYZ    Acceleration X, Y, Z axis
ww=[0 0 0];     %角速度XYZ    Angular velocity X, Y, Z axis
AA = [0 0 0];   %角度XYZ      Angle X, Y, Z axis
tt = 0;
a=[0 0 0]';
w=[0 0 0]';
A=[0 0 0]';
while(1)
    Head = read(s,2,'uint8')';                              %获取串口数据，其中s文件，已经在上面提及到  Getting serial data, the S file has been mentioned above
    if (Head(1)~=uint8(85))                                 %如果串口的第一个数据不等于85(0x55)，证明不符合协议，不进行数据解析  If the first data of the serial is not equal to 85 (0x55), it proves that it isn't conform to the protocol and haven't perform data analysis
        continue;
    end   
    Head(2)
    switch(Head(2))                                         %获取串口第二个数据   Getting the second data of the serial
        case 81                                             %81(0x51):加速度包   81(0x51): Acceleration data packet
            a = read(s,3,'int16')'/32768*16;                %获取3个16bit的加速度数据，请参考协议说明   Getting three 16bit acceleration data, please refer to the protocol
        case 82                                             %82(0x52):角速度包   82 (0x52): Angular velocity data packet
            w = read(s,3,'int16')'/32768*2000;              %获取3个16bit的角速度数据，请参考协议说明   Getting three 16bit angular velocity data, please refer to the protocol
        case 83                                             %83(0x53):角度包     83 (0x53): Angular data packet
            A = read(s,3,'int16')'/32768*180;               %获取3个16bit的角度数据，请参考协议说明     Getting three 16bit angle data, please refer to the protocol.
            aa = [aa;a'];
            ww = [ww;w'];
            AA = [AA;A'];
            tt = [tt;t];
            
            subplot(3,1,1);plot(tt,aa);title(['Acceleration = ' num2str(a') 'm2/s']);ylabel('m2/s');
            subplot(3,1,2);plot(tt,ww);title(['Gyro = ' num2str(w') '°/s']);ylabel('°/s');
            subplot(3,1,3);plot(tt,AA);title(['Angle = ' num2str(A') '°']);ylabel('°');              
            cnt=0;
            drawnow;
            if (size(aa,1)>5*f)                              %清空历史数据   Clear history data
                aa = aa(f:5*f,:);
                ww = ww(f:5*f,:);
                AA = AA(f:5*f,:);
                tt = tt(f:5*f,:);
            end
            t=t+0.1;                                         %数据默认是10Hz，也就是0.1s，如果更改了产品的输出速率，请把0.1改为其他输出速率   The data default is 10Hz, which is 0.1s. If you change the output rate of the product, please change 0.1 to other output rates
    end 
        
            End = read(s,3,'uint8')';
end
clear s;

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


