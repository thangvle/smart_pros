%shuffling data, has to do in command window
% random_EMG = EMGrawdataS5(randperm(size(EMGrawdataS5,1), :)); 

yfit = fineTree.predictFcn(random_EMG)

%incorporate output with C code
