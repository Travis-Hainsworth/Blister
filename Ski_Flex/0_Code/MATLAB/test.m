%%
clear all;
close all;
clc

% force_gage1_port = 'COM7';   % write in loadcell1 port
% force_gage2_port = 'COM8';   % write in loadcell2 port

%ser_ard=serialport("COM3",9600);
ser_inc=serialport("COM13",9600); %Open Com Port
ser_force_1 = serialport("COM7",9600);
ser_force_2 = serialport("COM8",9600);
[pitchFront, rollFront] = get_HWT905TTL_data(ser_inc);
stop_num =0;

while stop_num~=42
    [pitchFront, rollFront] = get_HWT905TTL_data(ser_inc);
    [force1, force2]=force_average(ser_force_1, ser_force_2,1);
    %MOVE SENSOR
    sig = move_x_mm(test_interval_mm, direction, ser_ard);
    disp(sig);
    stop_num = str2double(sig);
  
end
%MOVE BACK TO START
pause(5);
mm1 = get_distance_from_start(ser_ard);
% disp("mm1 START: ");
% disp(mm1);
sig = return_to_start(ser_ard);
% disp(sig);
mm2 = get_distance_from_start(ser_ard);
% disp("mm2 END: ");
% disp(mm2);
flush(ser_ard);
clear ser_ard;
clear ser_force_1;
clear ser_force_2;
clear ser_ard;

%% Get HWT905TTL pitch and roll data.

function [pitch, roll] = get_HWT905TTL_data(port)
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
end


%% Force Gage Code
% reads force data from sensor (written by fin)

function [force1,force2] = force_data(serial1,serial2)
    %connects and reads first sensor
    %serial1=serialport(portname1,9600); %connects to serial port 
    write(serial1,'?','string');        %queries serial port (required to obtain data)
    force1=read(serial1,5,"string");    %reads data point

    %connects and read second sensor
    %serial2=serialport(portname2,9600); %connects to serial port
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

    flush(serial1);
    flush(serail2);

end

% gets the average force data (written by fin)

function [force1,force2] = force_average(ser1, ser2,average)
        
    for i=1:average
        [force1(i),force2(i)]=force_data(ser1,ser2);
    end

    force1=mean(force1);
    force2=mean(force2);
end

function ret_mm = return_to_start(   ser)
    MOVE_TO_START = 2;
    serial_string = strcat(num2str(MOVE_TO_START),",0,1");
    ret_mm = serial_communication( ser, serial_string);
    flush(ser);
end 

function ret_signal = move_x_mm(  dis_mm, dir, ser)
    MOVE_X = 4;
    serial_string = strcat(num2str(MOVE_X),",",num2str(dis_mm),",",num2str(dir));
    ret_signal = serial_communication(ser, serial_string);
    flush(ser);
end

function ret_mm = get_distance_from_start(  ser)
    GET_CURRENT_POSITION = 14;
    serial_string = strcat(num2str(GET_CURRENT_POSITION),",0,1");
    %ret_mm = serial_communication(s, serial_string);
    write(ser, serial_string);
    ret_mm = read(ser);
    flush(ser);
end 

function ret_signal = set_current_position(  pos,ser)
    SET_CURRENT_POS = 6;
    serial_string = strcat(num2str(SET_CURRENT_POS),",",num2str(pos),",0");
    %ret_signal = serial_communication(s, serial_string);
    write(ser, serial_string);
    ret_signal = read(ser);
    flush(ser);
end

function ret_signal = set_stepsPerRev(  stepsPerRev, ser)
    SET_STEPS_PER_REVOLUTION = 12;
    serial_string = strcat(num2str(SET_STEPS_PER_REVOLUTION),",",num2str(stepsPerRev),",0");
    %ret_signal = serial_communication(s, serial_string);
    write(ser, serial_string);
    ret_signal = read(ser);
    flush(ser);
end

function ret_signal = set_acceleration(  acceleration, ser)
    SET_ACCELERATION = 10;
    serial_string = strcat(num2str(SET_ACCELERATION),",",num2str(acceleration),",0");
    %ret_signal = serial_communication(s, serial_string);
    write(ser, serial_string);
    ret_signal = read(ser);
    flush(ser);
end

function ret_signal = set_max_speed(  max_speed,ser)
    SET_MAX_SPEED = 8;
    serial_string = strcat(num2str(SET_MAX_SPEED),",",num2str(max_speed),",0");
    %ret_signal = serial_communication(s, serial_string);
    write(ser, serial_string);
    ret_signal = read(ser);
    flush(ser);
end

function sig = serial_communication(  ser, message)
    write(ser,message);
    pause(1);
    disp("wait");
    waitfor(s, "NumBytesAvailable");
    sig = read(ser);
end

function write(  ser, message)
    flush(ser);
    writeline(ser,message);
end

function out = read(  ser)
    out = readline(ser);
    flush(ser);
end