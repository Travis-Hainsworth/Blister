% Get the indecies of the columns that pertain to the specific markers
% MTS head, Top of the rim, and center of the axel. Could be added upon 
% to include other points of interest.

% Input: 
% mocap_synced = trimmed data from the motion capture
% I = index of the MTS head column
% RimTop = the index of the RimTop y-axis indicator
% Center = the index of the Center y-axis indicator

% Output: 
% mo_time = the time column from mocap_synced
% m_head = the columns pertaining to the head indicator
% m_rim_top = the columns pertaining to the rim top indicator
% m_axel = the columns pertaining to the axel indicator

function [mo_time, m_head, m_rim_top, m_axle] = getUsefulMarkers(mocap_synced, I, RimTop, Center)

    mo_time = mocap_synced(:,2);
    
    %need to sort these depending on how the excel file was saved
    m_head = mocap_synced(:,I-1:I+1);
    
    m_rim_top = mocap_synced(:,RimTop-1:RimTop+1);
    m_axle = mocap_synced(:,Center-1:Center+1);

end