
clc; 
load('fineTreeClassification.mat')
y = zeros(300, 2);
clear a; 
a = arduino;
% load('fineTreeClassification.mat')
% 
% yfit = fineTree.predictFcn(EMGrawdataS5);
% for col = 1:300 
%     s1 = "Rest"
%     if (strcmp(s1,"Rest"))
%         writeDigitalPin(a, 'D11', 0);
%     else
%         writeDigitalPin(a, 'D11', 1);
%     end
%         
% end

while true
    for i = 1:300
        y(i) = readVoltage(a, 'A0');
    end
end
