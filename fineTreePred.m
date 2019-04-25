%shuffling data, has to do in command window
%random_EMG = EMGrawdataS7(randperm(size(EMGrawdataS7,1), :)); 

yfit = fineTreeCompact.predictFcn(EMGrawdataS2)

%incorporate output with C code
