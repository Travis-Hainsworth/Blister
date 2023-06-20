%% Test Setup

clear all;
clc;

% DEFINE THESE VALUES
model_name = 'line_92';      % Input model name
year = 2020;                 % Input model year
manufacturer = "K2";         % Input ski Manufacturer
model_length_cm = 197;       %   Input Length of ski in cm
test_type = 'loaded';        % Test Type (string that is either loaded, unloaded, or torsion)
test_interval_mm = 50.8;

% Serial USB connections
inclinometer_port_front = 'COM9';  % write in front inclometer port
inclinometer_port_back = 'COM11';  % write in back inclometer port
force_gage1_port = 'COM7';   % write in loadcell1 port
force_gage2_port = 'COM8';   % write in loadcell2 port


% setup
data_matrix_front = zeros(0, 4);
data_matrix_back = zeros(0, 4);
data_matrix = zeros(0,4);
counter = 0;


%% COLLECT DATA POINT

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
    counter = counter + 1;

%%
test_interval_mm = 50.8;
distance_between_mm = 940;
test_distance_mm = test_interval_mm * counter; 

data_matrix = data_merge_fill(data_matrix_front, data_matrix_back, test_interval_mm, test_distance_mm, distance_between_mm)

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
function saveData(data_matrix, plot, dir_name)

    relative_dir_path = strcat('..\..\0_Data\',dir_name);

    if ~exist(relative_dir_path, 'dir')
       mkdir(relative_dir_path);
    end

    S = dir(relative_dir_path);
    N = nnz(~ismember({S.name},{'.','..'})&[S.isdir]);
    test_dir_name = strcat(num2str(N),"_test");
    relative_save_path = strcat(relative_dir_path,'\',test_dir_name);

    mkdir(relative_save_path);

    saveas(plot,strcat(relative_save_path, "\plots.png"));



    
end