clear
clc
close all

% Reserve 30 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%-------------------------------------------------------------------------%
%                           Define Color Palette                          %
%-------------------------------------------------------------------------%
coolors = ["#BCE784",...
           "#5DD39E",...
           "#348AA7",...
           "#525174",...
           "#513B56"];
%-------------------------------------------------------------------------%
%                                Load Data                                %
%-------------------------------------------------------------------------%
% Load data:
%load("StansFlow.mat")
load("R30nt1.mat")
load("R30nt2.mat")
load("R30nt3.mat")
load("R30nt4.mat")
load("R30nt5.mat")

% Condense data into a single 3D array
tests = {test1, test2, test3, test4, test5};

% % Take a look at results on 1 plot
% figure
% hold on
% for i = 1:5
%     plot(tests{i}(:,1),tests{i}(:,2))
% end
% title('Raw Data')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')

%-------------------------------------------------------------------------%
%                             Interpolate Data                            %
%-------------------------------------------------------------------------%
% If we want to create error bars, we need 1 consistent independent 
% variable (i.e., load)
% So, make that variable:
min_loads = [0,0,0,0,0];
max_loads = [0, 0, 0, 0, 0];
for i = 1:5
    min_loads(i) = min(tests{i}(:,1));
    max_loads(i) = max(tests{i}(:,1));
end

independent_lower_bounds = max(min_loads);
independent_upper_bounds = min(max_loads);

load_united = independent_lower_bounds : 0.1 : independent_upper_bounds;

% Interpolate each test's displacement onto this unified independent
% variable
displacements = zeros(length(load_united), 5);
for i = 1:5
    actual_load = tests{i}(:,1);
    actual_displacement = tests{i}(:,2);

    % There is a problem though, there are repeated loads with different
    % displacement, how can we interpolate then?
    % We remove the repeated loads
    [actual_load, indices_of_not_repeated, ~] = unique(actual_load);
    % Now remove the corresponding displacements:
    actual_displacement = actual_displacement(indices_of_not_repeated);

    % Now interpolate
    displacements(:,i) = interp1(actual_load, actual_displacement, load_united');
end

% % Have a look at the interpolated data
% figure
% hold on
% for i = 1:5
%     plot(load_united, displacements(:,i))
% end
% title('Interpolated Data')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')
% 
% % Sanity plot to see that interpolation isn't way off
% figure
% hold on
% plot(tests{1}(:,1),tests{1}(:,2),'.')
% plot(load_united, displacements(:,1),'-')
% title('Interpolated Data vs Raw Data of Test 1')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')


%-------------------------------------------------------------------------%
%                           Make Error Bar Plot                           %
%-------------------------------------------------------------------------%
% Pretty plots come from:
% https://www.mathworks.com/matlabcentral/fileexchange/26311-raacampbell-shadederrorbar
%
% Download this script, and put it in your workspace

% Mean and std use the wrong dimensions, so we'll transpose our data
displacements = displacements';
load_united = load_united';

% Now calc the mean and standard deviation
mean_of_displacements = mean(displacements);
standard_deviation = std(displacements);

% Now make the beautiful plot
%figure
shadedErrorBar(load_united, mean_of_displacements, standard_deviation,'lineprops',{'color',coolors(3)})
%plot(load_united,mean_of_displacements)
hold on
% title('Quasi-Static Loading')
% subtitle('Shaded Region: \pm1 \sigma, n=5')
% xlabel('Load (lbs)')
% ylabel('Displacement (in)')

% Stans Flow %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%-------------------------------------------------------------------------%
%                           Define Color Palette                          %
%-------------------------------------------------------------------------%
coolors = ["#BCE784",...
           "#5DD39E",...
           "#348AA7",...
           "#525174",...
           "#513B56"];
%-------------------------------------------------------------------------%
%                                Load Data                                %
%-------------------------------------------------------------------------%
% Load data:
%load("StansFlow.mat")
load("SFmk4_nt1.mat")
load("SFmk4_nt2.mat")
load("SFmk4_nt3.mat")
load("SFmk4_nt4.mat")
load("SFmk4_nt5.mat")

% Condense data into a single 3D array
tests = {test1, test2, test3, test4, test5};

% % Take a look at results on 1 plot
% figure
% hold on
% for i = 1:5
%     plot(tests{i}(:,1),tests{i}(:,2))
% end
% title('Raw Data')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')

%-------------------------------------------------------------------------%
%                             Interpolate Data                            %
%-------------------------------------------------------------------------%
% If we want to create error bars, we need 1 consistent independent 
% variable (i.e., load)
% So, make that variable:
min_loads = [0,0,0,0,0];
max_loads = [0, 0, 0, 0, 0];
for i = 1:5
    min_loads(i) = min(tests{i}(:,1));
    max_loads(i) = max(tests{i}(:,1));
end

independent_lower_bounds = max(min_loads);
independent_upper_bounds = min(max_loads);

load_united = independent_lower_bounds : 0.1 : independent_upper_bounds;

% Interpolate each test's displacement onto this unified independent
% variable
displacements = zeros(length(load_united), 5);
for i = 1:5
    actual_load = tests{i}(:,1);
    actual_displacement = tests{i}(:,2);

    % There is a problem though, there are repeated loads with different
    % displacement, how can we interpolate then?
    % We remove the repeated loads
    [actual_load, indices_of_not_repeated, ~] = unique(actual_load);
    % Now remove the corresponding displacements:
    actual_displacement = actual_displacement(indices_of_not_repeated);

    % Now interpolate
    displacements(:,i) = interp1(actual_load, actual_displacement, load_united');
end

% % Have a look at the interpolated data
% figure
% hold on
% for i = 1:5
%     plot(load_united, displacements(:,i))
% end
% title('Interpolated Data')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')
% 
% % Sanity plot to see that interpolation isn't way off
% figure
% hold on
% plot(tests{1}(:,1),tests{1}(:,2),'.')
% plot(load_united, displacements(:,1),'-')
% title('Interpolated Data vs Raw Data of Test 1')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')


%-------------------------------------------------------------------------%
%                           Make Error Bar Plot                           %
%-------------------------------------------------------------------------%
% Pretty plots come from:
% https://www.mathworks.com/matlabcentral/fileexchange/26311-raacampbell-shadederrorbar
%
% Download this script, and put it in your workspace

% Mean and std use the wrong dimensions, so we'll transpose our data
displacements = displacements';
load_united = load_united';

% Now calc the mean and standard deviation
mean_of_displacements = mean(displacements);
standard_deviation = std(displacements);

% Now make the beautiful plot
%figure
shadedErrorBar(load_united, mean_of_displacements, standard_deviation,'lineprops',{'color',coolors(3)})
%plot(load_united,mean_of_displacements)
hold on
% title('Quasi-Static Loading')
% subtitle('Shaded Region: \pm1 \sigma, n=5')
% xlabel('Load (lbs)')
% ylabel('Displacement (in)')

% Stans Flow %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%-------------------------------------------------------------------------%
%                           Define Color Palette                          %
%-------------------------------------------------------------------------%
coolors = ["#BCE784",...
           "#5DD39E",...
           "#348AA7",...
           "#525174",...
           "#513B56"];
%-------------------------------------------------------------------------%
%                                Load Data                                %
%-------------------------------------------------------------------------%
% Load data:
%load("StansFlow.mat")
load("SFmk4_nt1.mat")
load("SFmk4_nt2.mat")
load("SFmk4_nt3.mat")
load("SFmk4_nt4.mat")
load("SFmk4_nt5.mat")

% Condense data into a single 3D array
tests = {test1, test2, test3, test4, test5};

% % Take a look at results on 1 plot
% figure
% hold on
% for i = 1:5
%     plot(tests{i}(:,1),tests{i}(:,2))
% end
% title('Raw Data')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')

%-------------------------------------------------------------------------%
%                             Interpolate Data                            %
%-------------------------------------------------------------------------%
% If we want to create error bars, we need 1 consistent independent 
% variable (i.e., load)
% So, make that variable:
min_loads = [0,0,0,0,0];
max_loads = [0, 0, 0, 0, 0];
for i = 1:5
    min_loads(i) = min(tests{i}(:,1));
    max_loads(i) = max(tests{i}(:,1));
end

independent_lower_bounds = max(min_loads);
independent_upper_bounds = min(max_loads);

load_united = independent_lower_bounds : 0.1 : independent_upper_bounds;

% Interpolate each test's displacement onto this unified independent
% variable
displacements = zeros(length(load_united), 5);
for i = 1:5
    actual_load = tests{i}(:,1);
    actual_displacement = tests{i}(:,2);

    % There is a problem though, there are repeated loads with different
    % displacement, how can we interpolate then?
    % We remove the repeated loads
    [actual_load, indices_of_not_repeated, ~] = unique(actual_load);
    % Now remove the corresponding displacements:
    actual_displacement = actual_displacement(indices_of_not_repeated);

    % Now interpolate
    displacements(:,i) = interp1(actual_load, actual_displacement, load_united');
end

% % Have a look at the interpolated data
% figure
% hold on
% for i = 1:5
%     plot(load_united, displacements(:,i))
% end
% title('Interpolated Data')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')
% 
% % Sanity plot to see that interpolation isn't way off
% figure
% hold on
% plot(tests{1}(:,1),tests{1}(:,2),'.')
% plot(load_united, displacements(:,1),'-')
% title('Interpolated Data vs Raw Data of Test 1')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')


%-------------------------------------------------------------------------%
%                           Make Error Bar Plot                           %
%-------------------------------------------------------------------------%
% Pretty plots come from:
% https://www.mathworks.com/matlabcentral/fileexchange/26311-raacampbell-shadederrorbar
%
% Download this script, and put it in your workspace

% Mean and std use the wrong dimensions, so we'll transpose our data
displacements = displacements';
load_united = load_united';

% Now calc the mean and standard deviation
mean_of_displacements = mean(displacements);
standard_deviation = std(displacements);

% Now make the beautiful plot
%figure
shadedErrorBar(load_united, mean_of_displacements, standard_deviation,'lineprops',{'color',coolors(3)})
%plot(load_united,mean_of_displacements)
hold on
% title('Quasi-Static Loading')
% subtitle('Shaded Region: \pm1 \sigma, n=5')
% xlabel('Load (lbs)')
% ylabel('Displacement (in)')

% DT Swiss %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%-------------------------------------------------------------------------%
%                           Define Color Palette                          %
%-------------------------------------------------------------------------%
coolors = ["#BCE784",...
           "#5DD39E",...
           "#348AA7",...
           "#525174",...
           "#513B56"];
%-------------------------------------------------------------------------%
%                                Load Data                                %
%-------------------------------------------------------------------------%
% Load data:
%load("StansFlow.mat")
load("DTStest1.mat")
load("DTStest2.mat")
load("DTStest3.mat")
load("DTStest4.mat")
load("DTStest5.mat")

% Condense data into a single 3D array
tests = {test1, test2, test3, test4, test5};

% % Take a look at results on 1 plot
% figure
% hold on
% for i = 1:5
%     plot(tests{i}(:,1),tests{i}(:,2))
% end
% title('Raw Data')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')

%-------------------------------------------------------------------------%
%                             Interpolate Data                            %
%-------------------------------------------------------------------------%
% If we want to create error bars, we need 1 consistent independent 
% variable (i.e., load)
% So, make that variable:
min_loads = [0,0,0,0,0];
max_loads = [0, 0, 0, 0, 0];
for i = 1:5
    min_loads(i) = min(tests{i}(:,1));
    max_loads(i) = max(tests{i}(:,1));
end

independent_lower_bounds = max(min_loads);
independent_upper_bounds = min(max_loads);

load_united = independent_lower_bounds : 0.1 : independent_upper_bounds;

% Interpolate each test's displacement onto this unified independent
% variable
displacements = zeros(length(load_united), 5);
for i = 1:5
    actual_load = tests{i}(:,1);
    actual_displacement = tests{i}(:,2);

    % There is a problem though, there are repeated loads with different
    % displacement, how can we interpolate then?
    % We remove the repeated loads
    [actual_load, indices_of_not_repeated, ~] = unique(actual_load);
    % Now remove the corresponding displacements:
    actual_displacement = actual_displacement(indices_of_not_repeated);

    % Now interpolate
    displacements(:,i) = interp1(actual_load, actual_displacement, load_united');
end

% % Have a look at the interpolated data
% figure
% hold on
% for i = 1:5
%     plot(load_united, displacements(:,i))
% end
% title('Interpolated Data')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')
% 
% % Sanity plot to see that interpolation isn't way off
% figure
% hold on
% plot(tests{1}(:,1),tests{1}(:,2),'.')
% plot(load_united, displacements(:,1),'-')
% title('Interpolated Data vs Raw Data of Test 1')
% xlabel('Load (lbs)')
% ylabel('Displacement (mm)')


%-------------------------------------------------------------------------%
%                           Make Error Bar Plot                           %
%-------------------------------------------------------------------------%
% Pretty plots come from:
% https://www.mathworks.com/matlabcentral/fileexchange/26311-raacampbell-shadederrorbar
%
% Download this script, and put it in your workspace

% Mean and std use the wrong dimensions, so we'll transpose our data
displacements = displacements';
load_united = load_united';

% Now calc the mean and standard deviation
mean_of_displacements = mean(displacements);
standard_deviation = std(displacements);



% Now make the beautiful plot
shadedErrorBar(load_united, mean_of_displacements, standard_deviation,'lineprops',{'color',coolors(1)})
title('Quasi-Static Loading on Bike Rims with Tires')
subtitle('Shaded Region: \pm1 \sigma, n=5')
xlabel('Load (lbs)')
ylabel('Displacement (in)')
%plot(load_united,mean_of_displacements)
legend('We Are One Union (Carbon Fiber)','DT Swiss (Aluminum Alloy)','Stans Flow MK4 (Aluminum Alloy)')
%title('WAOU: Quasi-Static Loading')
%subtitle('Shaded Region: \pm1 \sigma, n=5')
%xlabel('Load (lbs)')
%ylabel('Displacement (in)')
%hold on