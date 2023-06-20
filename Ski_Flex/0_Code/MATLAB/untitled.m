%% Test Setup

clear all;
clc;

% DEFINE THESE VALUES
model_name = 'line_92';      % Input model name
year = 2020;                 % Input model year
manufacturer = "K2";         % Input ski Manufacturer
model_length_cm = 197;       %   Input Length of ski in cm
test_interval_mm = 15;       % Input the desired distance between data points in mm (multiples of 5 work best)
test_type = 'loaded';        % Test Type (string that is either loaded, unloaded, or torsion)

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

% RUN TEST (SINGLE SIDE, SINGLE INCLINOMETER)
s=serialport(arudiuno_port,115200); 
pause(2);
stop_num=0;
count = 0;
while stop_num~=42

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

    row_entry_front = [pitchFront, rollFront, force1, force2];
    row_entry_back = [pitchBack, rollBack, force1, force2];
    data_matrix_front = [data_matrix_front;row_entry_front];
    data_matrix_back = [data_matrix_back;row_entry_back];

    serial_string = strcat("2,",num2str(test_interval_mm),",0");
    %disp(serial_string);
    pause(2);
    %writedata = string(uint16(test_interval_mm)); % 0x01F4
    flush(s);
    writeline(s,serial_string); 
    pause(pause_time);
    readData2 = readline(s);
    %disp(readData2);
    flush(s);
    stop_num = str2num(readData2);
    count = count + 1;
    disp("number of datapoints");
    disp(count);
    disp("number of rotations");
    disp(stop_num/(200*8));
    disp("numer of steps for test at this point");
    disp(stop_num);
    disp("");
  
end
% data_matrix(end,:) = []; 

flush(s);
clear s;
%%


%%
% command for running specific number of steps
clear all;
clc;

arudiuno_port = 'COM3';
s=serialport(arudiuno_port,115200);
pause(5);

dis = -1; %-1 if not moving by number of steps
steps = 148800;
max_steps = 32767;
if dis ~= -1
    steps = (dis/5)*1600
end

iterations  = 0;
extra_steps = 0;

if steps > max_steps
    iterations = floor(steps/32767);
    extra_steps = mod(steps, max_steps); 
end 

disp(iterations);
disp(extra_steps);

count = 0;
while count ~= extra_steps
    message = strcat('4,',num2str(max_steps),',0');
    flush(s);
    writeline(s,message);
    pause(120);
    count = count + 1;
end

message = strcat('4,',num2str(extra_steps),',0');
flush(s);
writeline(s,message);
pause(5);
% r = readline(s);
% disp(r);
clear s;

%% Testing Sensor Data Collection

data_matrix_front = zeros(0, 4);
data_matrix_back = zeros(0, 4);
data_matrix = zeros(0,4);

inclinometer_port_front = "COM5";
inclinometer_port_back = "COM6";

force_gage1_port = 'COM5'; 
force_gage2_port = 'COM6';

counter = 94;
while(counter ~= 0)
    %[pitchFront, rollFront] = get_HWT905TTL_data("COM5");
    %[pitchBack, rollBack] = get_HWT905TTL_data("COM6");
    pitchFront = .02;
    rollFront = .02;
    pitchBack = .02;
    rollBack = .02;
    force1 = .3;
    force2 = .4;
    
    disp(strcat("Inclometer front data: Pitch-", num2str(pitchFront), " Roll-", num2str(rollFront)));
    disp(strcat("Inclometer back data: Pitch-", num2str(pitchBack), " Roll-", num2str(rollBack)));
    disp(strcat("Force gage readings: Gage1-", num2str(force1), " gage2-", num2str(force2)));

    row_entry_front = [pitchFront, rollFront, force1, force2];
    row_entry_back = [pitchBack, rollBack, force1, force2];
    data_matrix_front = [data_matrix_front;row_entry_front];
    data_matrix_back = [data_matrix_back;row_entry_back];

    counter = counter - 1; 
    

end

%%

test_distance_mm = 715;
dist_between_mm = 940;
test_interval_mm = 10;

data_matrix = data_merge_fill(data_matrix_front, data_matrix_back, test_interval_mm, test_distance_mm, dist_between_mm)


%% DateTime String for datafile creation

% Creates Datetime of start of test
dateTime = strrep(datestr(now),' ','_'); 
dateTime = strrep(dateTime,':','-');
fileName = strcat(model_name, '_',  test_type, '_', dateTime, '.xlsx');

%% cancat data together, fill in missing data

function output = data_merge_fill(data_matrix_front, data_matrix_back, test_interval_mm, test_distance_mm, dist_between_mm)
        num_of_missing_points = (dist_between_mm-test_distance_mm)/test_interval_mm;
        front_force_data = data_matrix_front(end, 3:4);
        back_force_data = data_matrix_back(1, 3:4);

        force1_front = front_force_data(1);
        force2_front = front_force_data(2);
        
        force1_back = back_force_data(1);
        force2_back = back_force_data(2);

        pitch_roll_front_data = data_matrix_front

        force1_average = (force1_back+force1_front)/2;
        force2_average = (force2_back+force2_front)/2;

        pitch = 0;
        roll = 0; 

        row_entry = [pitch, roll, force1_average, force2_average];
        
        for i = 1:num_of_missing_points
            data_matrix_front = [data_matrix_front; row_entry];
        end

        data_matrix = [data_matrix_front;data_matrix_back];

        output = data_matrix;
end




%% Old Inclinometer Code

% gets average accel data OLD inclinometer (written by fin)
function [pitch,roll] = accel_average(port_name,average)

    for i=1:average
        [pitch(i),roll(i)]=accel_data(port_name);
    end

    pitch=mean(pitch);
    roll=mean(roll);
end

% reads accel data from sensor OLD inclomin(written by fin)

function [pitch,roll] = accel_data(port_name)
    serial=serialport(port_name,115200); %defines serial port object (inclinometer)
    
    data=read(serial,63,"string");%reads data from sensor
    data = split(data,","); %splits string to pull each measurment
    
    pitch=str2double(data(5)); %converts pitch to double from string
    roll=str2double(data(6)); %converts roll to double from string
end

% gets the average force data (written by fin)

function [force1,force2] = force_average(portname1, portname2,average)
        
    for i=1:average
        [force1(i),force2(i)]=force_data(portname1,portname2);
    end

    force1=mean(force1);
    force2=mean(force2);
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

%% Calculate pause time that it takes

function output = get_pause_time(dis_between_data, change_per_rev, sec_per_rev)
    output = ceil(sec_per_rev * (dis_between_data/change_per_rev));
end

function output = get_physics_based_pause_time(acceleration, max_v, steps)
    
end
%% Get sensor data from force gages and inclinometers 

function [pitch, roll, force1, force2] = collect_sensor_data(inclinometer_port, load_cell1_port, load_cell2_port)
    [pitch, roll] = get_HWT905TTL_data(inclinometer_port);
    %[force1, force2]=force_average(load_cell1_port, load_cell2_port,1); 
    force1 = 0;
    force2 = 0;
    %[force1, force2]=force_average(load_cell1_port, load_cell2_port,1); 
end

%% Get HWT905TTL pitch and roll data.

function [pitch, roll] = get_HWT905TTL_data(inclinometer_port)

    s=serialport(inclinometer_port,9600); %Open Com Port
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
        Head = read(s,2,'uint8')';
        if (Head(1)==uint8(85))
            switch(Head(2))
                case 81 
                    a = read(s,3,'int16')'/32768*16 ;     
                    End = read(s,3,'uint8')';
                case 82 
                    w = read(s,3,'int16')'/32768*2000 ;    
                    End = read(s,3,'uint8')';
                case 83 
                    A = read(s,3,'int16')'/32768*180;
                    aa=[aa;a'];
                    ww = [ww;w'];
                    AA = [AA;A'];
                    tt = [tt;t];
    
                    disp(A(1));
                    disp(A(2));

                    pitch = A(1);
                    roll = A(2);
    
                    if (size(aa,1)>5*f)%clear history data
                        aa = aa(f:5*f,:);
                        ww = ww(f:5*f,:);
                        AA = AA(f:5*f,:);
                        tt = tt(f:5*f,:);
                    end
    
                    t=t+0.01;
                    End = read(s,3,'uint8')';

                    break
            end    
        end
    end
    clear s;
end
%%
%GOOD TROUBLE SHOOTING MESSAGES IF NECESSARY
 % disp("number of datapoints");
    % disp(count);
    % disp("number of rotations");
    % disp(stop_num/(200*8));
    % disp("numer of steps for test at this point");
    % disp(stop_num);
    % disp("");

