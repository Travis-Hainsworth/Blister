clc
clear
close all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Files %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

mocap_files = {'WAOU700lbf.csv', 'WAOU700lbf_001.csv', 'WAOU700lbf_002.csv', ...
    'WAOU700lbf_003.csv', 'WAOU700lbf_004.csv'};

MTS_files = {'WAOU700lbf_MTS_2-10.csv', 'WAOU700lbf1_MTS_2-10', 'WAOU700lbf2_MTS_2-10', ...
    'WAOU700lbf3_MTS_2-10', 'WAOU700lbf4_MTS_2-10'};

graph_files = {};

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Mocap %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for x = 1:5
    mocap = readmatrix(mocap_files{x});
    mocap = mocap(7:end,:); %Change depending on what row the data starts in the file
    
    %need to find MTS head column
    [MAX,I] = max(mocap(7,1:end));
    Pert = [mocap(7,4:3:end)];
    
    %takes the max out of the array
    for i = 1:4
        if Pert(1,i) == MAX
            Pert(1,i) = 0;
        end
    end
    
    %Finds new max, which is the top of the rim and then sets it to zero.
    %Also scales it to the correct size
    [MidHigh,RimTop] = max(Pert);
    Pert(RimTop) = 0;
    RimTop = (RimTop-1)*3+4;
    
    %Newest max is now the center marker, which is then scaled.
    [MidLow,Center] = max(Pert);
    Center = (Center-1)*3+4;
    
    % Pull out the head marker height (y-axis), offset it to zero, and invert
    % to match MTS orientation
    mo_head_height = mocap(:,I);
    mo_head_height = mo_head_height - mo_head_height(1);
    mo_head_height = -mo_head_height;
    
    % Find where the height starts to move (this is when the MTS test begins)
    thresh = 0.05; % mm
    starting_index = find(mo_head_height > thresh, 1);
    
    % Find where compression ends
    peak_height = max(mo_head_height);
    thresh = .025;
    
    index_of_top_height = find(mo_head_height > peak_height-thresh, 1);
    
    % Now trim all of the mocap data based on these bounds
    mocap = mocap(starting_index:index_of_top_height,:);
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% MTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    MTS = readmatrix(MTS_files{x});
    MTS = MTS(8:end,:); %Change depending on what row the data starts in the file
    MTS_time = MTS(:,3);
    MTS_height = MTS(:,1);
    MTS_load = MTS(:,2);
    
    % I want our test to start at 0,0
    MTS_height = MTS_height - MTS_height(1);
    MTS_time = MTS_time - MTS_time(1);
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Sync Data %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % If we want a force v displacement graph then we need the mocap data to
    % have the same sampling frequency as the MTS (plot(MTS load vs mocap
    % height)
    
    % Mocap has more data points
    ratio = size(mocap,1) / length(MTS_time);
    
    mocap_synced = mocap(1:ratio:end,:);
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%% Extract Useful Markers %%%%%%%%%%%%%%%%%%%%%%%%%
    mo_time = mocap_synced(:,2);
    
    %need to sort these depending on how the excel file was saved
    m_head = mocap_synced(:,I-1:I+1);
    
    m_rim_top = mocap_synced(:,RimTop-1:RimTop+1);
    m_axle = mocap_synced(:,Center-1:Center+1);
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%% Radial Compression Calcs %%%%%%%%%%%%%%%%%%%%%%%
    radial_vector = m_axle - m_rim_top;
    radial_length = sqrt(sum(radial_vector.^2 , 2));
    radial_compression = radial_length - radial_length(1);
    
    % The data is pretty noisy, so I'm going to do a moving mean smoothing
    % filter
    radial_compression = movmean(radial_compression, 50);
    
    % TO DO: get slow mow vid of test and see why this is happening! 
    %   Ideas:
    %       Perhaps it is vibrating as we contact different knobs of the tread
    %       Vibrating from squishing into that mucked up pillow block
    %       Vibrations from the machine's feedback loop

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Plots %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
     M = [MTS_load, radial_compression*0.0393701];
     file = sprintf('DTS_Force_Disp%d.csv', x);
     writematrix(M, file)

     graph_files{x} = readmatrix(file);

%individual graphs for each data set
%     figure
%     subplot(1,2,1)
%     plot(MTS_time, radial_compression*0.0393701)
%     title('For Greg: Radial Compression')
%     xlabel('Time')
%     ylabel('Compression (in)')
%     
%     subplot(1,2,2)
%     plot(MTS_load, radial_compression*0.0393701)
%     title('For Greg: Load vs Deflection')
%     xlabel('Load (lbs)')
%     ylabel('Compression (in)')
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%% Interpolate Data %%%%%%%%%%%%%%%%%%%%%%%%

% If we want to create error bars, we need 1 consistent independent 
% variable (i.e., load)
% So, make that variable:
min_loads = [0,0,0,0,0];
max_loads = [0, 0, 0, 0, 0];
for i = 1:5
    min_loads(i) = min(graph_files{i}(:,1));
    max_loads(i) = max(graph_files{i}(:,1));
end

independent_lower_bounds = max(min_loads);
independent_upper_bounds = min(max_loads);

load_united = independent_lower_bounds : 0.1 : independent_upper_bounds;

% Interpolate each test's displacement onto this unified independent
% variable
displacements = zeros(length(load_united), 5);
for i = 1:5
    actual_load = graph_files{i}(:,1);
    actual_displacement = graph_files{i}(:,2);

    % There is a problem though, there are repeated loads with different
    % displacement, how can we interpolate then?
    % We remove the repeated loads
    [actual_load, indices_of_not_repeated, ~] = unique(actual_load);
    % Now remove the corresponding displacements:
    actual_displacement = actual_displacement(indices_of_not_repeated);

    % Now interpolate
    displacements(:,i) = interp1(actual_load, actual_displacement, load_united');
end

% %Interpolated data without the shaded error bar
% for i = 1:5
%     plot(load_united, displacements(:,i))
% end
% title('Interpolated Data')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')


displacements = displacements';
load_united = load_united';

% Now calc the mean and standard deviation
mean_of_displacements = mean(displacements);
standard_deviation = std(displacements);

% Now make the beautiful plot
 colors = ["#BCE784",...
            "#5DD39E",...
            "#348AA7",...
            "#525174",...
            "#513B56"];

%plot with shaded error bar
figure
hold on
shadedErrorBar(load_united, mean_of_displacements, standard_deviation,'lineprops',{'color',colors(1)}) %change line size
title('Quasi-Static Loading on Bike Rims with Tires')
subtitle('Shaded Region: \pm1 \sigma, n=5')
xlabel('Load (lbs)')
ylabel('Displacement (in)')
plot(load_united,mean_of_displacements)
title('Quasi-Static Loading')
subtitle('Shaded Region: \pm1 \sigma, n=5')
xlabel('Load (lbs)')
ylabel('Displacement (in)')
hold on
