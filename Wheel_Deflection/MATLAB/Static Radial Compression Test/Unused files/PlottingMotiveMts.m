clc
clear
close all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Mocap %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
mocap = readmatrix('Travis_500.csv');
mocap = mocap(6:end,:);

% Pull out the time and head marker height
mo_time = mocap(:,2);
mo_head_height = mocap(:,end-1);
mo_mark1_height = mocap(:,end-4);
mo_mark2_height = mocap(:,end-7);
mo_mark3_height = mocap(:,end-11);

% to do.... do all of this massaging to mark heights
% and understand what each line of code does


% Offset the height so that it starts at zero
mo_head_height = mo_head_height - mo_head_height(1);

% Invert because the MTS says deflection is postive
mo_head_height = -mo_head_height;

% Find where the height starts to move (this is when the MTS test begins)
thresh = 0.05; % mm
mo_head_height = mo_head_height( mo_head_height > thresh );

% because we chopped off the beginning of the height data, we need to trim
% the time vector as well
mo_time = mo_time(1:length(mo_head_height));

% We're in MERICA
mo_head_height = mo_head_height * 0.03937008;


% Now, I just want the loading (height increasing), not the dwell and
% restoring
thresh = .025 * 0.03937008;

peak_height = max(mo_head_height);
index_of_top_height = find(mo_head_height > peak_height-thresh);

mo_head_height = mo_head_height(1:index_of_top_height);
% Also need to trim time to match
mo_time = mo_time(1:index_of_top_height);

% This plot validates that we have inverted, cut off initial delay, and
% centered the first datum to be at the origin
% plot(mo_time, mo_head_height)



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% MTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
MTS = readmatrix('MTS_DAQ_Crosshead_Travis500.csv');
MTS = MTS(7:end,:);
MTS_time = MTS(:,3);
MTS_height = MTS(:,1);
MTS_load = MTS(:,2);

% I want our test to start at 0,0
MTS_height = MTS_height - MTS_height(1);
MTS_time = MTS_time - MTS_time(1);

% If we want a force v displacement graph then we need to the mocap data to
% have the same sampling frequency as the MTS (plot(MTS load vs mocap
% height)
%
% Mocap has more data points
ratio = length(mo_time) / length(MTS_time);
mo_head_height_synced = mo_head_height(1:ratio:end);

plot(MTS_load, MTS_height)
hold on
plot(MTS_load, mo_head_height_synced)
xlabel('Force (lbs)')
ylabel('Displacement (in.... lame)')
legend('MTS Height', 'Mocap Head Height')
