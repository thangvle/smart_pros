function feature = extract_feature(data,win_size,win_inc)

if nargin < 3
    if nargin < 2
        win_size = 256;
    end
    win_inc = 32;
end

[Ndata,Nsignal] = size(data);

feature1 = getrmsfeat(data,win_size,win_inc);

ar_order = 4;
feature2 = getarfeat(data,ar_order,win_size,win_inc);

feature = [feature1 feature2];
