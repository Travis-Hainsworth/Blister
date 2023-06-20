%% Test Setup intial/unloaded

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
inclinometer_port_front = 'COM12';  % write in front inclometer port
inclinometer_port_back = 'COM11';  % write in back inclometer port
force_gage1_port = 'COM7';   % write in loadcell1 port
force_gage2_port = 'COM8';   % write in loadcell2 port


% setup
data_matrix_front = zeros(0, 4);
data_matrix_back = zeros(0, 4);
data_matrix_unloaded = zeros(0,4);
counter = 0;
temp_counter = 20;


%% COLLECT DATA POINT UNLOADED

%while(temp_counter ~= 0)

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
    temp_counter = temp_counter -1;
%end

%% Save unloaded data matrix
test_interval_mm = 50.8;
distance_between_mm = 940;
test_distance_mm = test_interval_mm * counter; 

data_matrix_unloaded = data_merge_fill(data_matrix_front, data_matrix_back, test_interval_mm, test_distance_mm, distance_between_mm)

%% Test Setup loaded
data_matrix_front = zeros(0, 4);
data_matrix_back = zeros(0, 4);
data_matrix_loaded = zeros(0,4);
counter = 0;
temp_counter = 20;


%% COLLECT DATA POINT for LOADED

%while(temp_counter ~= 0)

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
    temp_counter = temp_counter -1;
%end
%% Save loaded data matrix
test_interval_mm = 50.8;
distance_between_mm = 940;
test_distance_mm = test_interval_mm * counter; 

data_matrix_loaded = data_merge_fill(data_matrix_front, data_matrix_back, test_interval_mm, test_distance_mm, distance_between_mm)
%% Test Setup torsion 
data_matrix_front = zeros(0, 4);
data_matrix_back = zeros(0, 4);
data_matrix_torsion = zeros(0,4);
counter = 0;
temp_counter = 20;
%% COLLECT DATA POINT for LOADED

%while(temp_counter ~= 0)

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
    temp_counter = temp_counter -1;
%end
%% Save torsion data matrix
test_interval_mm = 50.8;
distance_between_mm = 940;
test_distance_mm = test_interval_mm * counter; 

data_matrix_torsion = data_merge_fill(data_matrix_front, data_matrix_back, test_interval_mm, test_distance_mm, distance_between_mm)
%% Generate PLOTS

%read the profile(unweighted pitch)
profile = data_matrix_unloaded(:,1);
%read the flex (weighted pitch)
flex = data_matrix_loaded(:,1);
%read forces from strain guages, and subtract the "unweighted" from
%weighted to get a net force

%force 1 is left, force 2 is right
force1 = data_matrix_loaded(:,3)-data_matrix_unloaded(:,3);
force2 = data_matrix_loaded(:,4)-data_matrix_unloaded(:,4);

% Variables to setup Manually

%measurements is the number of lines measured per round, = length/4
measurements = length(flex);
%rollermass = lass of rollers imparting force on skis in lbs
rollermass = 24.2;
%initialOffset = distance from applied load or clamp at the tip to the
%first measurement in inches
initialOffSet = 4.5;


%set empty string for moments
moment = zeros(measurements,1);
dTheta = zeros(measurements,1);

% Displacement
%displacement in radians
displacement = zeros(1,measurements+1)';
displacement(1:measurements) = deg2rad(profile - flex);

% Net Force
%net force in lbs
forceNet = force1+force2-rollermass;

% EI calcuation
EI = zeros(measurements,1);
for n = 2:(measurements)
    dTheta(n) = dirTheta(n,displacement);
    moment(n) = momentz(n-1,forceNet,initialOffSet);
    EI(n) = moment(n)/dTheta(n);
end
plotEI = EI(3:measurements-1);

tiledlayout(2,1);
nexttile;
plot(plotEI);
title('EJ');

gcf

% figure
% plot(displacement);
% figure
% plot(dTheta)
% Generate GJ plot

%read the profile(unweighted pitch)
tProf = data_matrix_unloaded(:,1);
%read the flex (weighted pitch)
rotation = data_matrix_torsion(:,1);
%read forces from strain guages, and subtract the "unweighted" from
%weighted to get a net force

%force 1 is left, force 2 is right
force1 = data_matrix_torsion(:,3)-data_matrix_unloaded(:,3);
force2 = data_matrix_torsion(:,4)-data_matrix_unloaded(:,4);

% Variables to setup Manually

%measurements is the number of lines measured per round, = length/4
measurements = length(rotation);
%rollermass = lass of rollers imparting force on skis in lbs
rollermass = 24.2;
%initialOffset = distance from applied load or clamp at the tip to the
%first measurement in inches
initialOffSet = 4.5;


%set empty string for moments
moment = zeros(measurements,1);
dTheta = zeros(measurements,1);

% Displacement
%displacement in radians
displacement = zeros(1,measurements+1)';
displacement(1:measurements) = deg2rad(tProf - rotation);

% Net Torque
%net force in lbs
torqueNet = abs(force1-force2)*3.75/12*1.356;

% GJ calcuation
GJ = zeros(measurements,1);
for n = 2:(measurements)
    dTheta(n) = dirTheta(n,displacement);
    GJ(n) = torqueNet(n)/dTheta(n);
end
plotGJ = abs(GJ(2:measurements-1));

p = tiledlayout(2,1);
nexttile;
plot(plotEI);
title('EJ');

nexttile;
plot(plotGJ);
title('GJ');


% figure
% plot(displacement);
% figure
% plot(dTheta)

%%


%% Save Data and Plots

directory_name = 'sampleTest1';

saveData(data_matrix_unloaded, data_matrix_loaded, data_matrix_torsion, gcf, directory_name);




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

% gets the average force data (written by fin)

function [force1,force2] = force_average(portname1, portname2,average)
        
    for i=1:average
        [force1(i),force2(i)]=force_data(portname1,portname2);
    end

    force1=mean(force1);
    force2=mean(force2);
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
function saveData(data_matrix_unloaded, data_matrix_loaded, data_matrix_torsion, plot, dir_name)

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
    writematrix(data_matrix_unloaded, strcat(relative_save_path, "\unloaded.csv" ));
    writematrix(data_matrix_loaded, strcat(relative_save_path, "\loaded.csv" ));
    writematrix(data_matrix_unloaded, strcat(relative_save_path, "\torsion.csv" ));
    
end
%% EJ functions 
% Moment about z(x)
%calculate moment about z at x in newton meters
%1.3558 is the conversion of ft-lbs to Nm
%12 is to convert to feet form inches

function [moment] = momentz(n,forceNet,initialOffSet)
    moment = (forceNet(n) * distanceFromTip(n,initialOffSet)) * 1.3558/24;
end

% Distance From Tip

function [distanceFromTip] = distanceFromTip(n,initialOffSet)
    %the distance of the measured pitch form the applied load in inches
    distanceFromTip = initialOffSet+n*2;
end

% Change in Theta at X

function [dTheta] = dirTheta(n,displacement)
    %calcualte the change in theta (the displacement) at a given x location
    %39.37 converts inches to meters
    theta = abs(displacement(n-1)-displacement(n))+abs(displacement(n)-displacement(n+1));
    dTheta = theta*39.37/4; %in radians/meter
end

