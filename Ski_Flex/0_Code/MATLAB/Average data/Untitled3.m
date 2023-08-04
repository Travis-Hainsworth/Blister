clc
clear
close all

%% load data
files = ['EI_points4.csv';'EI_points6.csv'];
n = size(files,1);


for i = 1:n
    loadfile = importdata(files(i,:));
    testData(:,i) = loadfile.data(:,2);
end
N = length(testData);
 for i = 1:N
    testAvg(i,:) = mean(rmoutliers(testData(i,:)));
end

figure
hold on
plot(testAvg)
title('Average EI data');
hold off    