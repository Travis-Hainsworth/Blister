%% Setup Variables
%read excel fire titles 'day1testing' into matlab

loadfile = importdata('day2testing2.xlsx');
%take numbers only from data file
dataTable = loadfile.data;
%read the profile(unweighted pitch)
tProf = (dataTable(:,2));
%read the flex (weighted pitch)
rotation = (dataTable(:,6));
%read forces from strain guages, and subtract the "unweighted" from
%weighted to get a net force

%force 1 is left, force 2 is right
force1 = dataTable(:,7)-dataTable(:,3);
force2 = dataTable(:,8)-dataTable(:,4);

%% Setup Variables using recently cleaned data from Data_Cleaning.

%read the profile(unweighted pitch)
tProf = averaged_unloaded_matrix(:,1);
%read the flex (weighted pitch)
rotation = averaged_loaded_matrix(:,1);
%read forces from strain guages, and subtract the "unweighted" from
%weighted to get a net force

%force 1 is left, force 2 is right
force1 = averaged_loaded_matrix(:,3)-averaged_unloaded_matrix(:,3);
force2 = averaged_loaded_matrix(:,4)-averaged_unloaded_matrix(:,4);

%% Setup Variables using Sample_Data.m see file in directory.

%read the profile(unweighted pitch)
tProf = data_matrix_unloaded1(:,1);
%read the flex (weighted pitch)
rotation = data_matrix_loaded1(:,1);
%read forces from strain guages, and subtract the "unweighted" from
%weighted to get a net force
%force 1 is left, force 2 is right
force1 = loaded_matrices(:,3)-unloaded_matrices(:,3);
force2 = loaded_matrices(:,4)-unloaded_matrices(:,4);

%% Setup Variables Looking at an indivduel test not average of tests.

%read the profile(unweighted pitch)
profile = data_matrix_unloaded1(:,1);
%read the flex (weighted pitch)
flex = data_matrix_loaded1(:,1);
%read forces from strain guages, and subtract the "unweighted" from
%weighted to get a net force
%force 1 is left, force 2 is right
force1 = data_matrix_loaded1(:,3)-data_matrix_unloaded1(:,3);
force2 = data_matrix_loaded1(:,4)-data_matrix_unloaded1(:,4);


%% Variables to setup Manually

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

%% Displacement
%displacement in radians
displacement = zeros(1,measurements+1)';
displacement(1:measurements) = deg2rad(tProf - rotation);

%% Net Torque
%net force in lbs
torqueNet = abs(force1-force2)*3.75/12*1.356;

%% GJ calcuation
GJ = zeros(measurements,1);
for n = 2:(measurements)
    dTheta(n) = dirTheta(n,displacement);
    GJ(n) = torqueNet(n)/dTheta(n);
end
plotGJ = abs(GJ(2:measurements-1));
plot(plotGJ);
% figure
% plot(displacement);
% figure
% plot(dTheta)


%% Change in Theta at X
function [dTheta] = dirTheta(n,displacement)
    %calcualte the change in theta (the displacement) at a given x location
    %39.37 converts inches to meters
    theta = abs(displacement(n-1)-displacement(n))+abs(displacement(n)-displacement(n+1));
    dTheta = theta*39.37/4; %in radians/meter
end
