function block = quad_overlap(subBlock)
% creates overlapping blocks of size (4n^2) from blocks of size n

assert(iscell(subBlock), 'subBlock should be a cell array');

dim = size(subBlock);

upper_left = subBlock(1:(dim(1)-1) , 1: (dim(2)-1));
upper_right = subBlock(1: (dim(1)-1), 2: dim(2));
lower_left = subBlock(2:dim(1), 1: (dim(2)-1) );
lower_right = subBlock(2:dim(1), 2:dim(2));

block = cell(dim-1);
x_start = zeros(numel(block));
y_start = zeros(numel(block));

parfor m=1:numel(block)
    block{m} = [upper_left{m}, upper_right{m}; ...
        lower_left{m}, lower_right{m} ];
    
end