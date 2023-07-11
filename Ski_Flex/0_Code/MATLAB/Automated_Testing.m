%% Test Setup
clear all;
clc;

model_name = 'Black Crow_';                   % Input model name
year = '_';                               % Input model year
manufacturer = "_";                       % Input ski Manufacturer
model_length_cm = '';                      % Input Length of ski in cm
directory_name = strcat(manufacturer, model_name, year, model_length_cm); 
%directory_name = "aluminumn_bar";
test_interval_mm = 50;                        % Input the desired distance between data points in mm (multiples of 5 work best)
direction = 1;                                % Initial Direction

global ardiuno_port inclinometer_port_front inclinometer_port_back force_gage1_port force_gage2_port;
global ardiuno_serial inclinometer_front_serial inclinometer_back_serial force_gage1_serial force_gage2_serial;
global ei_dtheta ei_moment ei_displacment gj_dtheta gj_moment gj_displacment ei_distance_from_tip;

% Serial USB connections
ardiuno_port = 'COM16';                       % write in arduino port
inclinometer_port_front = 'COM11';            % write in front inclometer port
inclinometer_port_back = 'COM12';             % write in back inclometer port
force_gage1_port = 'COM8';                    % write in loadcell1 port
force_gage2_port = 'COM7';                    % write in loadcell2 port

ardiuno_serial = serialport(ardiuno_port, 115200);
inclinometer_front_serial = serialport(inclinometer_port_front, 9600);
inclinometer_back_serial = serialport(inclinometer_port_back, 9600);
force_gage1_serial = serialport(force_gage1_port, 9600);
force_gage2_serial = serialport(force_gage2_port, 9600);
%% Run Full test
num_of_test = 10;
while num_of_test ~= 0
    [data_matrix_front_unloaded, data_matrix_back_unloaded] = sensor_automation(test_interval_mm, direction);
    pause(2);
    
    temp_save_single_test(data_matrix_front_unloaded, "data_matrix_front_unloaded");
    temp_save_single_test(data_matrix_back_unloaded, "data_matrix_back_unloaded");
    test_distance_mm = size(data_matrix_front_unloaded,1)*test_interval_mm;
    dist_between_mm = 863; %change when distance between inclinomters change
    test_distance_mm = size(data_matrix_front_unloaded,1) * test_interval_mm;
    data_matrix_unloaded = data_merge(data_matrix_front_unloaded, data_matrix_back_unloaded, test_interval_mm, test_distance_mm, dist_between_mm);
    temp_save_single_test(data_matrix_unloaded, "Unloaded");
    
    
    sig = return_to_start(ardiuno_serial);
    
    sig = move_force_gauges(ardiuno_serial, 80, 80);

    pause(1);
    
    sig = level_force_gauges(ardiuno_serial, 0, .05, inclinometer_back_serial, 1);
    
    [data_matrix_front_loaded,data_matrix_back_loaded] = sensor_automation(test_interval_mm, direction);
    pause(2);
    
    temp_save_single_test(data_matrix_front_loaded, "data_matrix_front_loaded");
    temp_save_single_test(data_matrix_back_loaded, "data_matrix_back_loaded");
    [front_unl, front_load] = check_and_adjust_size(data_matrix_front_unloaded, data_matrix_front_loaded);%, truncate_from_bottom);
    [back_unl, back_load] = check_and_adjust_size(data_matrix_back_unloaded, data_matrix_back_loaded);%, truncate_from_top);
    unloaded = data_merge(front_unl, back_unl, test_interval_mm, test_distance_mm, dist_between_mm);
    loaded = data_merge(front_load, back_load, test_interval_mm, test_distance_mm, dist_between_mm);
    temp_save_single_test(loaded, "Loaded");
    [ei_x_points, ei_y_points] = get_EI_point(unloaded, loaded, test_interval_mm);
    temp_save_plot_and_points(ei_x_points, ei_y_points, 'EI');
    
    sig = return_to_start(ardiuno_serial);
    sig = move_force_gauges(ardiuno_serial, 0, -20);
    
    [data_matrix_front_torsion,data_matrix_back_torsion] = sensor_automation(test_interval_mm, direction);
    pause(2);
    
    temp_save_single_test(data_matrix_front_torsion, "data_matrix_front_torsion");
    temp_save_single_test(data_matrix_back_torsion, "data_matrix_back_torsion");
    [front_unl, front_tor] = check_and_adjust_size(data_matrix_front_unloaded, data_matrix_front_torsion);%, truncate_from_bottom);
    [back_unl, back_tor] = check_and_adjust_size(data_matrix_back_unloaded, data_matrix_back_torsion);%, truncate_from_top);
    unloaded = data_merge(front_unl, back_unl, test_interval_mm, test_distance_mm, dist_between_mm);
    torsion = data_merge(front_tor, back_tor, test_interval_mm, test_distance_mm, dist_between_mm);
    data_matrix_torsion = data_merge(unloaded, torsion, test_interval_mm, test_distance_mm, dist_between_mm);
    temp_save_single_test(torsion, "Torsion");
    [gj_x_points, gj_y_points] = get_EI_point(unloaded, torsion, test_interval_mm);
    temp_save_plot_and_points(gj_x_points, gj_y_points, 'GJ');
    
    sig = return_to_start(ardiuno_serial);
    sig = move_force_gauges(ardiuno_serial, 0, 20);
    %%
    sig = move_force_gauges(ardiuno_serial, -80, -80);
   
    move_force_gauges_until_desired_force(ardiuno_serial, force_gage1_serial, force_gage2_serial, 0, 5);
    
    save_data_clear_temp(directory_name);
    num_of_test = num_of_test -1;

end
%% Manually move force motors
sig = move_force_gauges(ardiuno_serial, -10, -10);
disp(sig);
%% Manually move inclinometer motor
sig = move_x_mm(800,0, ardiuno_serial);
disp(sig);
%% Return inclinometer motor back to start
sig = return_to_start(ardiuno_serial);
disp(sig)
%% Automated Data Collection Function
function [data_matrix_front,data_matrix_back] = sensor_automation(test_interval_mm, direction) %inclinometer_front_serial
    global ardiuno_serial inclinometer_front_serial inclinometer_back_serial force_gage1_serial force_gage2_serial;
    data_matrix_front = zeros(0, 4);
    data_matrix_back = zeros(0, 4);
    stop_num=0;

    flush(inclinometer_front_serial);

    [pitchFront_temp, rollFront_temp] = get_HWT905TTL_data(inclinometer_front_serial);

    flush(inclinometer_back_serial);

    [pitchBack_temp, rollBack_temp] = get_HWT905TTL_data(inclinometer_back_serial);

    

    while stop_num~=42
        %collect data
        pause(.125); 
        flush(inclinometer_front_serial);
        [pitchFront, rollFront] = get_HWT905TTL_data(inclinometer_front_serial);
        flush(inclinometer_back_serial);
        [pitchBack, rollBack] = get_HWT905TTL_data(inclinometer_back_serial);
        [force1, force2]=force_average(force_gage1_serial, force_gage2_serial, 1);

        row_entry_front = [pitchFront, rollFront, force1, force2];
        row_entry_back = [pitchBack, rollBack, force1, force2];

        data_matrix_front = [data_matrix_front;row_entry_front];
        disp("data_matrix_front: ");
        disp(data_matrix_front);
        data_matrix_back = [data_matrix_back;row_entry_back];
        disp("data_matrix_back: ");
        disp(data_matrix_back);
        
        %MOVE SENSOR
        sig = move_x_mm(test_interval_mm, direction, ardiuno_serial);
        disp(sig);
        stop_num = str2double(sig);
    end

    flush(inclinometer_front_serial);

    [pitchFront_temp, rollFront_temp] = get_HWT905TTL_data(inclinometer_front_serial);

    flush(inclinometer_back_serial);

    [pitchBack_temp, rollBack_temp] = get_HWT905TTL_data(inclinometer_back_serial);


end
%% Sensor Functions
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
    flush(port);
end

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
    flush(serial2);
end

% gets the average force data (written by fin)
function [force1,force2] = force_average(ser1, ser2,average)  
    for i=1:average
        [force1(i),force2(i)]=force_data(ser1,ser2);
    end
    force1=mean(force1);
    force2=mean(force2);
end


%% Matlab Arduino Functions using serial communication
function out = clear_and_reset_serial_ports()
    global ardiuno_serial inclinometer_front_serial inclinometer_back_serial force_gage1_serial force_gage2_serial;
    global ardiuno_port inclinometer_port_front inclinometer_port_back force_gage1_port force_gage2_port;
    try 
        clear ardiuno_serial inclinometer_front_serial inclinometer_back_serial force_gage1_serial force_gage2_serial;
    catch
        disp("Serials are not connected yet.");
    end
    ardiuno_serial = serialport(ardiuno_port, 115200);
    inclinometer_front_serial = serialport(inclinometer_port_front, 9600);
    inclinometer_back_serial = serialport(inclinometer_port_back, 9600);
    force_gage1_serial = serialport(force_gage1_port, 9600);
    force_gage2_serial = serialport(force_gage2_port, 9600);
end

function ret_mm = return_to_start(s)
    MOVE_TO_START = 2;
    serial_string = strcat(num2str(MOVE_TO_START),",0,1");
    ret_mm = serial_communication(s, serial_string);
    flush(s);
end 

function ret_signal = move_x_mm(dis_mm, dir, s)
    MOVE_X = 4;
    serial_string = strcat(num2str(MOVE_X),",",num2str(dis_mm),",",num2str(dir));
    disp(serial_string);
    ret_signal = serial_communication(s, serial_string);
    flush(s);
end

function ret_signal = move_force_gauges(s, left_mm, right_mm)
    MOVE_FORCE_GAUGES = 24;
    serial_string = strcat(num2str(MOVE_FORCE_GAUGES),",",num2str(left_mm),",",num2str(right_mm));
    ret_signal = serial_communication(s, serial_string);
    flush(s);
end

function ret_signal = move_force_gauges_until_desired_force(s, force_gauge_left, force_gauge_right, desired_force, step_size)
    MOVE_FORCE_GAUGES = 24;
    [force_left, force_right]=force_average(force_gauge_left, force_gauge_right, 1);

    if force_right < desired_force && force_left < desired_force
        while force_left < desired_force || force_right < desired_force
            serial_string = strcat(num2str(MOVE_FORCE_GAUGES),",",num2str(step_size),",",num2str(step_size));
            ret_signal = serial_communication(s, serial_string);
            [force_left, force_right]=force_average(force_gauge_left, force_gauge_right, 1);
        end
    else
        while force_left > desired_force || force_right > desired_force
            serial_string = strcat(num2str(MOVE_FORCE_GAUGES),",",num2str(-1*step_size),",",num2str(-1*step_size));
            ret_signal = serial_communication(s, serial_string);
            [force_left, force_right]=force_average(force_gauge_left, force_gauge_right, 1);
        end
    end
    
    flush(s);
end

function ret_signal = level_force_gauges(s, desired_angle, precision, inclinometer, step_size)
    MOVE_FORCE_GAUGES = 24;
    [pitch, roll] = get_HWT905TTL_data(inclinometer);
    disp(strcat("pitch: ", num2str(pitch)));
    disp(strcat("roll: ", num2str(roll)));
    ret_signal = 24;
    while ~(roll < (desired_angle + precision) && roll > ((-desired_angle) + (-precision)))
        % step_size = gradient descent step size adjustment(roll, desired_angle, step_size)
        message = make_message(int2str(MOVE_FORCE_GAUGES),roll, desired_angle, precision, step_size);
        ret_signal = serial_communication(s, message);
        [pitch, roll] = get_HWT905TTL_data(inclinometer);
        disp(strcat("pitch: ", num2str(pitch)));
        disp(strcat("roll: ", num2str(roll)));
    end
    flush(s);
end

function message = make_message(m, actual_angle, desired_angle, precision, step_size)
    message = m;
    if actual_angle <= desired_angle+precision && actual_angle >= desired_angle-precision % make this a fuction that takes in actual and desired, concatenates and retruns message
          message = strcat(message,',0',',0');
    elseif actual_angle < desired_angle
          message = strcat(message,',0',',',num2str(step_size)); 
    else
          message = strcat(message,',',num2str(step_size),',0'); 
    end 
end

function ret_mm = get_distance_from_start(s)
    GET_CURRENT_POSITION = 14;
    serial_string = strcat(num2str(GET_CURRENT_POSITION),",0,1");
    %ret_mm = serial_communication(s, serial_string);
    custom_write(s, serial_string);
    ret_mm = custom_read(s);
    flush(s);
end 

function ret_state = get_testing_state(s)
    GET_TESTING_STATE = 26;
    serial_string = strcat(num2str(GET_TESTING_STATE),",0,1");
    %ret_mm = serial_communication(s, serial_string);
    custom_write(s, serial_string);
    ret_state = custom_read(s);
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

function ret_signal = reset_arduino(s)
    RESET_ARDUINO = 16;
    serial_string = strcat(num2str(RESET_ARDUINO),",0,0");
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end

function ret_signal = set_enable_switch(s,enable)
    SET_enable_switch = 22;
    serial_string = strcat(num2str(SET_enable_switch),",",num2str(enable),",0");
    disp(serial_string);
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end

function ret_signal = reattach_interrupt(s)%ls is the back or front limit switch (0 = back, 1 = front)
    REATTACH_INTERUPT = 18;
    serial_string = strcat(num2str(REATTACH_INTERUPT),",0,0");
    custom_write(s, serial_string);
    ret_signal = custom_read(s);
    flush(s);
end

function ret_signal = deattach_interrupt(s)%ls is the back or front limit switch (0 = back, 1 = front)
    DEATTACH_INTERUPT = 20;
    serial_string = strcat(num2str(DEATTACH_INTERUPT),",0,0");
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
%% Data Manipulation/Saving Functions
function output = data_merge(data_matrix_front, data_matrix_back, test_interval_mm, test_distance_mm, dist_between_mm);
        num_of_missing_points = (dist_between_mm-test_distance_mm)/test_interval_mm;
        front_force_data = data_matrix_front(end, 3:4);
        back_force_data = data_matrix_back(1, 3:4);
        front_inclinometer_data = data_matrix_front(end,1:2);
        back_inclinometer_data = data_matrix_back(1,1:2);
        pitch_front = front_inclinometer_data(1);
        roll_front = front_inclinometer_data(2);
        pitch_back = back_inclinometer_data(1);
        roll_back = back_inclinometer_data(2);
        force1_front = front_force_data(1);
        force2_front = front_force_data(2);
        force1_back = back_force_data(1);
        force2_back = back_force_data(2);
        force1_slope = abs(force1_back-force1_front)/(num_of_missing_points+1);
        force2_slope = abs(force2_back-force2_front)/(num_of_missing_points+1);
        pitch_slope = (pitch_front-pitch_back)/(num_of_missing_points+1);
        roll_slope = (roll_front-roll_back)/(num_of_missing_points+1);
        for i = 1:num_of_missing_points
            missing_row_entry = [pitch_front-(i*pitch_slope), roll_front-(i*roll_slope), force1_front-(i*force1_slope), force2_front-(i*force2_slope)];
            data_matrix_front = [data_matrix_front; missing_row_entry];
        end
        data_matrix = [data_matrix_front;data_matrix_back];
        output = data_matrix;
end

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
    column_names = {'pitch', 'roll', 'forceLeft', 'forceRight'};
    unloaded_data = [column_names; num2cell(data_matrix_unloaded)];
    loaded_data = [column_names; num2cell(data_matrix_loaded)];
    torsion_data = [column_names; num2cell(data_matrix_torsion)];
    writecell(unloaded_data, strcat(relative_save_path, "\unloaded.csv" ));
    writecell(loaded_data, strcat(relative_save_path, "\loaded.csv" ));
    writecell(torsion_data, strcat(relative_save_path, "\torsion.csv" ));
end

function temp_save_single_test(data_matrix, type)
    relative_save_path = strcat('..\..\0_Data\Temp_Data_Folder\');
    if ~exist(relative_save_path, 'dir')
       mkdir(relative_save_path);
    end
    column_names = {'pitch', 'roll', 'forceLeft', 'forceRight'};
    data = [column_names; num2cell(data_matrix)];
    writecell(data, strcat(relative_save_path, "\",type,".csv" ));    
end

function temp_save_plot_and_points(x_points, y_points, plot_title)
    relative_save_path = strcat('..\..\0_Data\Temp_Data_Folder\');
    if ~exist(relative_save_path, 'dir')
       mkdir(relative_save_path);
    end
    p = plot(x_points, y_points);
    title(plot_title);
    xlabel("Milimeters");
    ylabel("N*(m^2)");
    points_matrix = [x_points', y_points'];
    column_names = {"milimeters", "N*(m^2)"};
    data = [column_names; num2cell(points_matrix)];
    writecell(data, strcat(relative_save_path, "\",plot_title,"_points.csv" ));
    saveas(p, strcat(relative_save_path, "\",plot_title,"_graph.png"));
end

function save_data_clear_temp(dir_name)
    temp_folder_path = strcat('..\..\0_Data\Temp_Data_Folder\');
    relative_dir_path = strcat('..\..\0_Data\',dir_name);
    if ~exist(relative_dir_path, 'dir')
       mkdir(relative_dir_path);
    end
    S = dir(relative_dir_path);
    N = nnz(~ismember({S.name},{'.','..'})&[S.isdir]);
    test_dir_name = strcat(num2str(N),"_test");
    relative_save_path = strcat(relative_dir_path,'\',test_dir_name);
    mkdir(relative_save_path);
    filePattern = fullfile(temp_folder_path, '*.*');
    copyfile(filePattern, relative_save_path);
    rmdir(temp_folder_path, 's');
    temp_folder_dir = strcat('..\..\0_Data\Temp_Data_Folder\');
    if ~exist(temp_folder_dir, 'dir')
       mkdir(temp_folder_dir);
    end
end

function [m1, m2] = check_and_adjust_size(matrix1, matrix2)%, truncate_location)
    if size(matrix1,1) > size(matrix2,1)
        matrix1 = truncate_matrix(matrix1, size(matrix1,1)-size(matrix2,1));%, truncate_location);
    elseif size(matrix1,1) < size(matrix2,1)
        matrix2 = truncate_matrix(matrix2, size(matrix2,1)-size(matrix1,1));%, truncate_location);
    end
    m1 = matrix1;
    m2 = matrix2;
end

function truncated = truncate_matrix(matrix, num_rows)%, truncate_location)
    % rows = size(matrix,1);
    % middle = floor(rows/2);
    % truncate_from_bottom = 0;
    % trauncate_from_top = 1;
    % if truncate_location == truncate_from_bottom
    for i = size(matrix,1):-1:size(matrix,1)-num_rows+1
        matrix(i, :) = [];
    end
    % elseif truncate_location == truncate_from_top
    %     for i = 1:1:num_rows
    %         matrix(i, :) = [];
    %     end
    % end
    truncated = matrix;
end
%% Generate EI_points
function [X_points, EI_points] = get_EI_point(data_matrix_unloaded, data_matrix_loaded, test_interval_mm)
        global ei_dtheta ei_moment ei_displacment;
        step_size_m = test_interval_mm/1000;
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
        rollermass = 31;

        %initialOffset = distance from applied load or clamp at the tip to the
        %first measurement in meters
        initialOffSet = .14;
        
        %set empty string for moments
        moment = zeros(measurements,1);
        dTheta = zeros(measurements,1);
        
        % Displacement
        %displacement in radians
        displacement = zeros(1,measurements+1)';
        displacement(1:measurements) = deg2rad(profile - flex);
        ei_displacment = displacement;

        % Net Force
        %net force in lbs
        forceNet = force1+force2-rollermass;
        global ei_distance_from_tip;
        ei_distance_from_tip = [];
        
        % EI calcuation
        EI = zeros(measurements,1);
        for n = 2:(measurements)
            dTheta(n) = dirTheta(n,displacement, step_size_m);
            moment(n) = momentz(n-1,forceNet,initialOffSet, measurements, test_interval_mm);
            EI(n) = moment(n)/dTheta(n);
        end
        ei_dtheta = dTheta;
        ei_moment = moment;
        EI_points = EI(3:measurements-1);
        X_points = linspace(0, (size(EI_points,1)-1)*test_interval_mm, size(EI_points,1));
        EI_points = EI_points';
end
%% Generate GJ_points
function [X_points, GJ_points] = get_GJ_points(data_matrix_unloaded, data_matrix_torsion, test_interval_mm)
        global gj_dtheta gj_moment gj_displacment;
        step_size_m = test_interval_mm/1000;

        %read the profile(unweighted pitch)
        tProf = data_matrix_unloaded(:,1);

        %read the flex (weighted pitch)
        rotation = data_matrix_torsion(:,1);

        %read forces from strain guages, and subtract the "unweighted" from
        %weighted to get a net force
        %force 1 is left, force 2 is right
        force1 = data_matrix_torsion(:,3)-data_matrix_unloaded(:,3);
        force2 = data_matrix_torsion(:,4)-data_matrix_unloaded(:,4);

        %measurements is the number of lines measured per round, = length/4
        measurements = length(rotation);

        %rollermass = lass of rollers imparting force on skis in lbs
        rollermass = 31;

        %initialOffset = distance from applied load or clamp at the tip to the
        %first measurement in meters
        initialOffSet = .14;


        %set empty string for moments
        moment = zeros(measurements,1);
        dTheta = zeros(measurements,1);
        EIDistanceFromTip = zeros(measurements:1);

        % Displacement
        %displacement in radians
        displacement = zeros(1,measurements+1)';
        displacement(1:measurements) = deg2rad(tProf - rotation);
        gj_displacment = displacement;

        % Net Torque
        %net force in lbs
        torqueNet = abs(force1-force2)*3.75/12*1.356;

        % GJ calcuation
        GJ = zeros(measurements,1);
        for n = 2:(measurements)
            dTheta(n) = dirTheta(n,displacement, step_size_m);
            GJ(n) = torqueNet(n)/dTheta(n);
        end

        gj_dtheta = dTheta;
        gj_moment = moment;
        GJ_points = abs(GJ(2:measurements-1));
        X_points = linspace(0, (size(GJ_points,1)-1)*test_interval_mm, size(GJ_points,1));
        GJ_points = GJ_points';
end
%% EI/GJ functions 
% Moment about z(x)
%calculate moment about z at x in newton meters
%1.3558 is the conversion of ft-lbs to Nm
%12 is to convert to feet form inches

function ei_matrix = make_ei_matrix(unloaded_data, loaded_data, interval_mm)
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
        rollermass = 31;
        %initialOffset = distance from applied load or clamp at the tip to the
        %first measurement in meters
        initialOffSet = .14;
        
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
        global ei_distance_from_tip;
        ei_distance_from_tip = [];
        for n = 2:(measurements)
            dTheta(n) = dirTheta(n,displacement);
            moment(n) = momentz(n-1,forceNet,initialOffSet,measurements,interval_mm);
            EI(n) = moment(n)/dTheta(n);
        end
        plotEI = EI(3:measurements-1);
end

function [moment] = momentz(n,forceNet,initialOffSet,measurements,test_interval_mm)
    moment = (forceNet(n) * distanceFromTip(n,initialOffSet,measurements,test_interval_mm)) *4.448/2;
end

% Distance From Tip
function [distanceFromTip] = distanceFromTip(n,initialOffSet,measurements,test_interval_mm)
    %the distance of the measured pitch form the applied load in inches
    global ei_distance_from_tip;
    distanceFromTip = (measurements/2 -abs(n-measurements/2))*test_interval_mm/1000+initialOffSet;
    ei_distance_from_tip(end+1) = distanceFromTip;
end

% Change in Theta at X
function [dTheta] = dirTheta(n,displacement, step_size_m)
    %calcualte the change in theta (the displacement) at a given x location
    %39.37 converts inches to meters
    theta = abs(displacement(n-1)-displacement(n))+abs(displacement(n)-displacement(n+1));
    dTheta = theta/(2*step_size_m);%*39.37/4; %in radians/meter
end