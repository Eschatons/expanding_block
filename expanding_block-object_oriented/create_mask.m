function mask = create_mask(bucket, init, img_size)

N = numel(bucket);
recombined = bucket{1:N};
M = numel(recombined);
mask = zeros(img_size);

pullx = @(block) block.x;
pully = @(block) block.y;

x1 = cellfunc(pullx, recombined, 'UniformOutput', false);
y1 = cellfunc(pully, recombined, 'UniformOutput', false);
x2 = x1+(init.blockSize-1);
y2 = y1+(init.blockSize-1);

X = @(m) x1(m):x2(m);
Y = @(m) y1(m):y2(m);
for m=1:M
    mask(X(m), Y(m)) = mask(X(m), Y(m))+1;
end
end