clc
clear
close all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Mocap %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
mocap = readmatrix('Travis_500.csv');
mocap = mocap(6:end,:);

% Pull out the head marker height (y-axis), offset it to zero, and invert
% to match MTS orientation
mo_head_height = mocap(:,end-1);
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
MTS = readmatrix('MTS_DAQ_Crosshead_Travis500.csv');
MTS = MTS(7:end,:);
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
%
% Mocap has more data points
ratio = size(mocap,1) / length(MTS_time);

mocap_synced = mocap(1:ratio:end,:);


%%%%%%%%%%%%%%%%%%%%%%%%%% Extract Useful Markers %%%%%%%%%%%%%%%%%%%%%%%%%
mo_time = mocap_synced(:,2);
m_head = mocap_synced(:,end-2:end);
m_rim_top = mocap_synced(:,end-5:end-3);
m_axle = mocap_synced(:,end-8:end-6);


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
figure
subplot(1,2,1)
plot(MTS_time,radial_compression)
title('Radial Compression')
xlabel('Time')
ylabel('Compression (mm)')

subplot(1,2,2)
plot(MTS_load, radial_compression)
title('Load vs Deflection')
xlabel('Load (lbs)')
ylabel('Compression (mm)')



figure
subplot(1,2,1)
plot(MTS_time, radial_compression*0.0393701)
title('For Greg: Radial Compression')
xlabel('Time')
ylabel('Compression (in)')

subplot(1,2,2)
plot(MTS_load, radial_compression*0.0393701)
title('For Greg: Load vs Deflection')
xlabel('Load (lbs)')
ylabel('Compression (in)')