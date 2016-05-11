function group = assign_to_group(block, init)
group = cell(init.numBuckets, 1);
blocks_per_group = (floor(numel(group)./numel(blocks)));
unrounded_bpg = numel(group)./numel(blocks);

try assert(blocks_per_group - unrounded_bpg == 0, 'genericerror')
catch
    warning(['number of groups:    %g \n', ...
        'does not divide number of blocks:   %g: \n' ...
        'this may cause unintended behavior'], numel(group), numel(block));
end

v1 = 1:blocks_per_group:numel(block);
v2 = v1-1+blocks_per_group;
v2(end) = numel(block);
for j=1:numel(group);
    group{j} = block(v1(j):v2(j));
end
