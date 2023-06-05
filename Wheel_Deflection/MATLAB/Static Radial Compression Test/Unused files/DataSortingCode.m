clc
clear

data = readmatrix('RadialCompression300lbf4.csv');
data = data(8:end,:);
%data = rmmissing(data);

%time = data(6:79056,2);
topMark = data(:,4);
midMark = data(:,7);

topmin = min(topMark)
topmax = max(topMark)

midmin = min(midMark)
midmax = max(midMark)

totalD = (topmax - topmin) - (midmax - midmin)

%plot(time,V3)


