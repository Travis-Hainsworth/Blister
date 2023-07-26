%%
clear,clc,close;
t=importdata('EI_points.csv');
t = t.data;
data=t(:,2);
binCounts = convertToBins(data);
index = binCounts(1);
tip = data(1:index);
shovel = data(index+1:index+binCounts(2));
index = index+binCounts(2);
underfoot = data(index+1:index+binCounts(3));
index = index+binCounts(3);
heel = data(index+1:index+binCounts(4));
index = index + binCounts(4);
tail = data(index+1 : end);
averagetip=mean(tip);
averageshovel = mean(shovel);
averageunderfoot = mean(underfoot);
averageheel = mean(heel);
averagetail = mean(tail);
% tip=0;
% shovel=0;
% underfoot=0;
% heel=0;
% tail=0;
if averagetip < 78.28
    tip=4;
elseif averagetip >= 78.28 && averagetip < 122.83
    tip=5;
elseif averagetip >= 122.83 && averagetip < 167.43
    tip=5.5;
elseif averagetip >= 167.43 && averagetip < 212.03
    tip=6;
elseif averagetip >= 212.03 && averagetip < 256.58
    tip=6.5;
elseif averagetip >= 256.58 && averagetip < 301.43
    tip=7;
elseif averagetip >= 301.43 && averagetip < 345.73
    tip=7.5;
elseif averagetip >= 345.73 && averagetip < 390.33
    tip=8;
elseif averagetip >= 390.33 && averagetip < 434.88
    tip=8.5;
elseif averagetip >= 434.88 && averagetip < 479.48
    tip=9;
elseif averagetip >= 479.88 && averagetip < 524.04
    tip=9.5;
elseif averagetip >= 524.04
    tip=10;
end
if averageshovel < 78.28
    shovel=4;
elseif averageshovel >= 78.28 && averageshovel < 122.83
    shovel=5;
elseif averageshovel >= 122.83 && averageshovel < 167.43
    shovel=5.5;
elseif averageshovel >= 167.43 && averageshovel < 212.03
    shovel=6;
elseif averageshovel >= 212.03 && averageshovel < 256.58
    shovel=6.5;
elseif averageshovel >= 256.58 && averageshovel < 301.43
    shovel=7;
elseif averageshovel >= 301.43 && averageshovel < 345.73
    shovel=7.5;
elseif averageshovel >= 345.73 && averageshovel < 390.33
    shovel=8;
elseif averageshovel >= 390.33 && averageshovel < 434.88
    shovel=8.5;
elseif averageshovel >= 434.88 && averageshovel < 479.48
    shovel=9;
elseif averageshovel >= 479.88 && averageshovel < 524.04
    shovel=9.5;
elseif averageshovel >= 524.04
    shovel=10;
end
if averageunderfoot < 78.28
    underfoot=4;
elseif averageunderfoot >= 78.28 && averageunderfoot < 122.83
    underfoot=5;
elseif averageunderfoot >= 122.83 && averageunderfoot < 167.43
    underfoot=5.5;
elseif averageunderfoot >= 167.43 && averageunderfoot < 212.03
    underfoot=6;
elseif averageunderfoot >= 212.03 && averageunderfoot < 256.58
    underfoot=6.5;
elseif averageunderfoot >= 256.58 && averageunderfoot < 301.43
    underfoot=7;
elseif averageunderfoot >= 301.43 && averageunderfoot < 345.73
    underfoot=7.5;
elseif averageunderfoot >= 345.73 && averageunderfoot < 390.33
    underfoot=8;
elseif averageunderfoot>= 390.33 && averageunderfoot < 434.88
    underfoot=8.5;
elseif averageunderfoot >= 434.88 && averageunderfoot < 479.48
    underfoot=9;
elseif averageunderfoot >= 479.88 && averageunderfoot < 524.04
    underfoot=9.5;
elseif averageunderfoot >= 524.04
    underfoot=10;
end
if averageheel < 78.28
    heel=4;
elseif averageheel >= 78.28 && averageheel < 122.83
    heel=5;
elseif averageheel >= 122.83 && averageheel < 167.43
    heel=5.5;
elseif averageheel >= 167.43 && averageheel < 212.03
    heel=6;
elseif averageheel >= 212.03 && averageheel < 256.58
    heel=6.5;
elseif averageheel >= 256.58 && averageheel < 301.43
    heel=7;
elseif averageheel >= 301.43 && averageheel < 345.73
    heel=7.5;
elseif averageheel >= 345.73 && averageheel < 390.33
    heel=8;
elseif averageheel >= 390.33 && averageheel < 434.88
    heel=8.5;
elseif averageheel >= 434.88 && averageheel < 479.48
    heel=9;
elseif averageheel >= 479.88 && averageheel < 524.04
    heel=9.5;
elseif averageheel >= 524.04
    heel=10;
end
if averagetail < 78.28
    tail=4;
elseif averagetail >= 78.28 && averagetail < 122.83
    tail=5;
elseif averagetail >= 122.83 && averagetail < 167.43
    tail=5.5;
elseif averagetail >= 167.43 && averagetail < 212.03
    tail=6;
elseif averagetail >= 212.03 && averagetail < 256.58
    tail=6.5;
elseif averagetail >= 256.58 && averagetail < 301.43
    tail=7;
elseif averagetail >= 301.43 && averagetail < 345.73
    tail=7.5;
elseif averagetail >= 345.73 && averagetail < 390.33
    tail=8;
elseif averagetail >= 390.33 && averagetail < 434.88
    tail=8.5;
elseif averagetail >= 434.88 && averagetail < 479.48
    tail=9;
elseif averagetail >= 479.88 && averagetail < 524.04
    tail=9.5;
elseif averagetail >= 524.04
    tail=10;
end
tip
shovel
underfoot
heel
tail
x=[tip,shovel,underfoot,heel,tail];
blister=mean(x)
function binCounts = convertToBins(data)
    % Determine the bin edges
    numBins = 5;
    binEdges = linspace(min(data), max(data), numBins+1);
    % Calculate the bin counts
    binCounts = histcounts(data, binEdges);
end