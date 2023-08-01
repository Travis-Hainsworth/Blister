%% Setup Variables using recently cleaned data from Data_Cleaning.

%read the profile(unweighted pitch)
profile = averaged_unloaded_matrix(:,1);
%read the flex (weighted pitch)
flex = averaged_loaded_matrix(:,1);
%read forces from strain guages, and subtract the "unweighted" from
%weighted to get a net force

%force 1 is left, force 2 is right
force1 = averaged_loaded_matrix(:,3)-averaged_unloaded_matrix(:,3);
force2 = averaged_loaded_matrix(:,4)-averaged_unloaded_matrix(:,4);

%% Setup Variables using Sample_Data.m see file in directory.

%read the profile(unweighted pitch)
profile = data_matrix_unloaded1(:,1);
%read the flex (weighted pitch)
flex = data_matrix_loaded1(:,1);
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
measurements = length(flex);
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
displacement(1:measurements) = deg2rad(profile - flex);

%% Net Force
%net force in lbs
forceNet = force1+force2-rollermass;

%% EI calcuation
EI = zeros(measurements,1);
for n = 2:(measurements)
    dTheta(n) = dirTheta(n,displacement);
    moment(n) = momentz(n-1,forceNet,initialOffSet);
    EI(n) = moment(n)/dTheta(n);
end
plotEI = EI(3:measurements-1);
plot(plotEI);
% figure
% plot(displacement);
% figure
% plot(dTheta)

%% Moment about z(x)
%calculate moment about z at x in newton meters
%1.3558 is the conversion of ft-lbs to Nm
%12 is to convert to feet form inches

function [moment] = momentz(n,forceNet,initialOffSet)
    moment = (forceNet(n) * distanceFromTip(n,initialOffSet)) * 1.3558/24;
end

%% Distance From Tip

function [distanceFromTip] = distanceFromTip(n,initialOffSet)
    %the distance of the measured pitch form the applied load in inches
    distanceFromTip = initialOffSet+n*2;
end

%% Change in Theta at X

function [dTheta] = dirTheta(n,displacement)
    %calcualte the change in theta (the displacement) at a given x location
    %39.37 converts inches to meters
    theta = abs(displacement(n-1)-displacement(n))+abs(displacement(n)-displacement(n+1));
    dTheta = theta*39.37/4; %in radians/meter
end