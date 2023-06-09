%%











%% Setup Matrices to hold test data from sensors
%Or add more depending on how much redudancy you want.
counter = 1;
Max_num_of_tests = 60;

data_matrix_unloaded1 = zeros(Max_num_of_tests, 4);
data_matrix_unloaded2 = zeros(Max_num_of_tests, 4);
data_matrix_unloaded3 = zeros(Max_num_of_tests, 4);

data_matrix_loaded1 = zeros(Max_num_of_tests, 4);
data_matrix_loaded2 = zeros(Max_num_of_tests, 4);
data_matrix_loaded3 = zeros(Max_num_of_tests, 4);

%% Counter Reset for each test
%reset counter between tests to ensure data properly inserts into matrices.
clear s;
clc;
counter = 1;

%%

s=serialport('COM11',9600);
distance_between_data = 5; %in milimeters

%s=serialport('COM11',9600);
%readData = readline(s) % reads "Ready"
%start the stepper motor
stop_num=0;

flush(s);
pause(1);
writedata = string(uint16(distance_between_data)); % 0x01F4
writeline(s,writedata) % write data

pause(3);
readData2 = readline(s);
flush(s);
disp(readData2);


%%

distance_between_data = 10; %in milimeters

s=serialport('COM11',9600);
%readData = readline(s) % reads "Ready"
%start the stepper motor
stop_num=0;
%listen for



while stop_num~=42
    %sense/write area


    tic

    [pitch, roll]=accel_average('COM7',1);
    [force1, force2]=force_average('COM5','COM6',1);

    toc

    %replace these matrix variable names with a new matrix every new test.
    data_matrix_unloaded3(counter,1) = pitch;
    data_matrix_unloaded3(counter,2) = roll;
    data_matrix_unloaded3(counter,3) = force1;
    data_matrix_unloaded3(counter,4) = force2;

    disp("Sensor Readings: ");
    disp(data_matrix_unloaded3(counter, :));
    counter = counter + 1;



    %trigger rotation of stepper motor
    flush(s);
    pause(1);
    writedata = string(uint16(distance_between_data)); % 0x01F4
    pause(1);
    writeline(s,writedata) % write data
    %pause for movement
    %check if limit switch is hit
    pause(3);
    readData2 = readline(s);
    flush(s);
    stop_num = hex2dec(readData2);
    disp(stop_num);
end
% write(s,writedata,'uint16') % write data
% for i=1:2 % read 2 lines of data
%    readData = readline(s)
% end
flush(s);
clear s;
%% Recording Unloaded Data
%Press run on this block to record data to data_matrix, every run will add new row. 
[pitch, roll]=accel_average('COM7',1);
[force1, force2]=force_average('COM5','COM6',1);


%replace these matrix variable names with a new matrix every new test.
data_matrix_unloaded3(counter,1) = pitch;
data_matrix_unloaded3(counter,2) = roll;
data_matrix_unloaded3(counter,3) = force1;
data_matrix_unloaded3(counter,4) = force2;

disp("Sensor Readings: ");
disp(data_matrix_unloaded3(counter, :));
counter = counter + 1;

%% Check unloaded Test 1

disp(data_matrix_unloaded1);

%% Check unloaded Test 2

disp(data_matrix_unloaded2);

%% Check unloaded Test 3

disp(data_matrix_unloaded3);

%% Counter Reset for each test
%reset counter between tests to ensure data properly inserts into matrices.

counter = 1;

%% Recording Loaded Data
%Press run on this block to record data to data_matrix, every run will add new row. 
disp("Now recording loaded measuerments");

[pitch, roll]=accel_average('COM7',1);
[force1, force2]=force_average('COM5','COM6',1);

data_matrix_loaded3(counter,1) = pitch;
data_matrix_loaded3(counter,2) = roll;
data_matrix_loaded3(counter,3) = force1;
data_matrix_loaded3(counter,4) = force2;

disp(data_matrix_loaded3(counter, :));
counter = counter + 1;

%% Check Loaded Test 1

disp(data_matrix_loaded1);

%% Check Loaded Test 2

disp(data_matrix_loaded2);

%% Check Loaded Test 3

disp(data_matrix_loaded3);

%% Save Raw Data to Excels files if needed.
% Auto Creates excel file named with model, loaded unloaded or torsion, and
% datetime.

% Data to be saved
matrix_to_save = data_matrix_loaded3;

% Input model name
model_name = 'line_92';

% Test Type (string that is either loaded, unloaded, or torsion)
test_type = 'loaded';


% Auto Creates excel file named with model, loaded or unloaded, and
% datetime.
t = now;
dateTime = strrep(datestr(t),' ','_');
dateTime = strrep(dateTime,':','-');
fileName = strcat(model_name, '_',  test_type, '_', dateTime, '.xlsx');

save_data_to_excel(matrix_to_save, fileName);

%% Data Collection Functions
% Save Pitch, Roll, Force1, and Force2 to matrix passed to function

function updateMatrix(pitch, roll, force1, force2, matrix, index)
    disp(index)
    matrix(index,1) = pitch;
    matrix(index,2) = roll;
    matrix(index,3) = force1;
    matrix(index,4) = force2;
end

% gets average accel data (written by fin)
function [pitch,roll] = accel_average(port_name,average)

    for i=1:average
        [pitch(i),roll(i)]=accel_data(port_name);
    end

    pitch=mean(pitch);
    roll=mean(roll);
end

% reads accel data from sensor (written by fin)

function [pitch,roll] = accel_data(port_name)
serial=serialport(port_name,115200);       %defines serial port object (inclinometer)

data=read(serial,63,"string");          %reads data from sensor
data = split(data,",");                 %splits string to pull each measurment

pitch=str2double(data(5));               %converts pitch to double from string
roll=str2double(data(6));                %converts roll to double from string
end

% gets the average force data (written by fin)

function [force1,force2] = force_average(portname1, portname2,average)
        
    for i=1:average
        [force1(i),force2(i)]=force_data(portname1,portname2);
    end

    force1=mean(force1);
    force2=mean(force2);
end

% reads force data from sensor (written by fin)

function [force1,force2] = force_data(portname1,portname2)
%connects and reads first sensor
serial1=serialport(portname1,9600); %connects to serial port 
write(serial1,'?','string');     %queries serial port (required to obtain data)
force1=read(serial1,5,"string");   %reads data point

%connects and read second sensor
serial2=serialport(portname2,9600); %connects to serial port
write(serial2,'?','string');     %queries serial port (required to obtain data)
force2=read(serial2,5,"string");   %reads data point

%converts and outputs data for first sensor
force1=strrep(force1,' ','');       %removes any spaces in read data
force1=strrep(force1,'l','1');      %changes L to 1 (weird data read)
force1=str2double(force1);           %converts data to double

%converts and outputs data for second sensor
force2=strrep(force2,' ','');       %removes any spaces in read data
force2=strrep(force2,'l','1');      %changes L to 1 (weird data read)
force2=str2double(force2);           %converts data to double
end

% Save Matrix Data to Excel File. 
%Pass in Matrix,and filename of excel file, and Matlab will automatically
%populate first four columns with pitch, roll, force1, and force2 data from
%matrix

function save_data_to_excel(matrix,fileName)
    for i = 1:size(matrix,1)
        writematrix(matrix(i,1),fileName,'Sheet',1,'Range', strcat('A', num2str(i)));
        writematrix(matrix(i,2),fileName,'Sheet',1,'Range', strcat('B', num2str(i)));
        writematrix(matrix(i,3),fileName,'Sheet',1,'Range', strcat('C', num2str(i)));
        writematrix(matrix(i,4),fileName,'Sheet',1,'Range', strcat('D', num2str(i)));
    end
end

