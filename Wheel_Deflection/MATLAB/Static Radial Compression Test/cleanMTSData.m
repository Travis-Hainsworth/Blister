% MTS data processing function 

% Input: 
% filePath = the path to the .csv file containing the data
% collected by the MTS.

% Output:
% MTS = trimmed MTS matrix
% MTS_time = the time column from the MTS data
% MTS_height = the height data for the head of the MTS (this is what is 
% used to synch mocap and MTS data).
% MTS_load = the load (lbf) data from the MTS readout

function [MTS, MTS_time, MTS_height, MTS_load] = cleanMTSData(filePath)
    MTS = readmatrix(filePath);
    MTS = MTS(7:end,:);
    MTS_time = MTS(:,3);
    MTS_height = MTS(:,1);
    MTS_load = MTS(:,2);
    
    % Set test to start at 0,0
    MTS_height = MTS_height - MTS_height(1);
    MTS_time = MTS_time - MTS_time(1);
end