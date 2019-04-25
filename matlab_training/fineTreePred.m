%a = arduino; % initialize arduino
%pin = 11; % change the pin here

inputData = [];

for i=1:299
    inputData(i) = i; % input data here
end
predictData = transpose(inputData)

%while(1)
%   yfit = fineTree.predictFcn(predictData)
%
%end

% TODO:
% yfit return an array of prediction. Match each of these predict
% accordingly
% Option 1: try queue
% Option 2: try hash map. Hash map returns a value but there will be a lot
% of duplication
