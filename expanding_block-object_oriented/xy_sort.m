function [x, y, sorted] = xy_sort(blocks)

sortval = blocks.variance

%{
lexigraphic sort of blocks by y and x position
outputs a 3-column matrix
if given a vector in order [v1, v2, v3, v4...] with values |v1|, |v2|,
 ... |vn|
%}

%input handling
assert(isa(blocks{1}, 'block'), ['arrays passed to xy_sort' ...
    'should be "block" objects'])
if (isvector(blocks) == 0)
    warning('Input to xy_sort not a vector, vectorizing anyways')
end



x = zeros(numel(blocks), 1);
y = zeros(numel(blocks), 1);

parfor m=1:numel(blocks)
    y(m) = mod(m-1, dim(1))+1;
    x(m) = ceil(m/dim(2));
end

n = numel(block);
block = reshape(block, n, 1);
dict = [block, y, x];
sorted_dict = sortrows(dict);
key = sorted_dict(:, 2);
sorted = sorted_dict(:, 1);

end