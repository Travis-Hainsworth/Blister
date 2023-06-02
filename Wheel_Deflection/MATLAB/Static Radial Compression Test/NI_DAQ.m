


d = daq("ni"); %initializing DAQ on script

d.Rate = 100; %Sampling frequency in Hz

ch = addinput(d, "cDAQ1Mod1","ai0", "Bridge");
ch.Name = "S-Beam Load Cell";
ch.BridgeMode = 'Full';
ch.NominalBridgeResistance = 350; %resistance is taken by matlab and compensates for the excitation voltage
ch.ADCTimingMode = "HighSpeed"; %has modes that can help eliminate noise from measurement: HighResolution

ch.ExcitationSource = 'Internal';


ch.ExcitationVoltage = 2.5; %lower excitation voltage means lower data resolution. The mod only supports internal excitation up to 2.5V, and excitation is proportional to the output signal (.003 mv/V)


%data = read(d,5000);
clc
fprintf("Reading\n")
data = read(d,seconds(10));
fprintf("Done Reading\n")


dat=data.Variables;
dat = dat - dat(1); %passing variable around instead of the dataset, matlab doesn't altering the dataset in this way.

OF = abs(10000*dat/(0.003)); %matlab takes excitation Voltage into account with resistance input, so force conversion is max load * mv differential/full scale output (mv/v)
%min(dat)


close all

plot(data.Time, OF)
ylabel('Load (lbf)')
xlabel('Time (s)')
title('Force Data')

PeakForce = max(OF)
