clc
clear
binMat = zeros(1,5);
binMatScale = zeros(1,5);
EI = importdata('EI_points.csv').data(:,2);
n = (length(EI)/5);
BlisterSegments = zeros(1,5);
for i = 1:5
    start = round(1+(i-1)*n);
    stop = round(i*n);
    segment = EI(start:stop);
    binMat(i) = mean(segment);
    binMatScale(i) = scaleMe(binMat(i));
    BlisterSegments(i) = binMatScale(i);
end
Tip = BlisterSegments(1);
Shovel = BlisterSegments(2);
Underfoot = BlisterSegments(3);
Heel = BlisterSegments(4);
Tail = BlisterSegments(5);
BlisterRank = table(Tip,Shovel,Underfoot,Heel,Tail);
disp(BlisterRank)
function value = scaleMe(EI)
    value = floor(EI/44.575)*.5+4;
end