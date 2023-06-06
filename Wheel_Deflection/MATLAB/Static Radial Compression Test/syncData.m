% If we want a force v displacement graph then we need the mocap data to
% have the same sampling frequency as the MTS (plot(MTS load vs mocap
% height)
%
% Mocap has more data points

% Input: 
% mocap = mocap data in matrix form and trimmed by cleanMocapData.m
% MTS_time = the time column from the MTS data read out by cleanMTSData.m

% Output: 
% mocap_synced = trimmed mocap data based upon size of MTS data

function mocap_synced = syncData(mocap, MTS_time)

    ratio = size(mocap,1) / length(MTS_time);
    
    mocap_synced = mocap(1:ratio:end,:);

end