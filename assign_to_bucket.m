function bucket = assign_to_bucket(group)
% Place the blocks from groups i-1, i, and i+1 into bucket i

bucket = cell(numel(group), 1);
for i=1:numel(group)
    if (i>1 && i<numel(group))
        bucket{i} = [group{i-1}, group{i}, group{i+1}];
    elseif i > 1
        bucket{i} = [group{i-1}, group{i}];
    else 
        bucket{i} = [group{i}, group{i+1}];
    end
end