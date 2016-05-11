function [mask, imgOut] = expanding_block(imgIn, varargin)
% an expanding block algorithm to detect copy-paste duplication within
% an image

%% PROGRAM DESCRIPTION:
% INPUT
%{
    imIn: a RGB image, either as an mxnx3 array or a string
    varargin: an expand_block_init OBJECT: parameters described in expanding_block_init.m.    
%}

% OUTPUT
%{
    mask:   a spare 2d array the same width and height as image_in, 
            with value 1 in regions considered 'copies' and value 0
            elsewhere

    imgOut: the original image, grayscaled, except at pixels with '1's in
            the mask. these areas are given red channel values of 255.
 
% LIST OF DEPENDENCIES
OBJECTS:
expand_block_init: an OBJECT which contains the parameters for this
suppose the image has N overlapping blocks of size P^2

block:
    block.pixel: an Nx1 cell array. Each element is NxN uint8 gpuArray

    block.dim: a 2-element vector containning the # of blocks that fit into
    each dimension of the image

    block.avg_gray: a size-N double vector containing the average gray
    values of the corresponding element in block.pixel

    block.variance: a size-N double vector containing the variance of the 
    corresponding element in block.pixel

    std-deviation: a size-N double vector containing the std_deviation of
    the corresponding element in block.pixel

    block.x: a size-N double vector containing x position of the
    corresponding element in block.pixel

    block.y: a size-N double vector containing x position of the
    corresponding element in block.pixel


import_image(imgIn): imports an image as %FILENAME or m x n x 3 matrix
img_to_subBlocks(img, init): creates init.blockDistance sized subBlocks
quad_overlap(subBlock): creates overlapping blocks (init.blockDistance^2)
in size from subBlocks; records x-position and y-position of starting
blocks and holds in array

%}


%%  0 input handling:
imgIn = import_image(imgIn);

% grayscale image and trim to a size divisible by init.blockDistance

if size(imgIn, 3) == 3
    img_gray_full = rgb2gray(imgIn);
elseif size(imgIn, 3) == 1
    warning('Image only has single channel: treating as grayscale');
    img_gray_full = imgIn;
else
    error('Image not RGB or single-channel')
end

assert(nargin <= 2, 'at most one varargin')

if nargin == 2
    init = varargin{1};
    assert(isa(init, 'expand_block_init'), ['varargin must be an' ...
        'expand_block init OBJECT']);
else
    init = expand_block_init;
end

overScan = mod(size(img_gray_full), init.blockDistance);
%{ 
%hold extra pixels for reconstruction later:
extraPixels = img_gray_full( (end-overScan(1)) : end, (end-overScan(2)):end);
%}


img = img_gray_full( 1:end-(overScan(1)), 1:(end-overScan(2)) );

%% 1: Divide an image into small overlapping blocks of blockSize^2


%{
EFRON'S METHOD: 
% construct blockDistance x blockDistance subBlocks
%}
subBlock = img_to_subBlocks(img, init);

% CREATE BLOCKS

% Create block:
block = overlap_block;
block.dim = size((img-init.blockSize)./init.blockDistance);
[block.x, block.y, block.pixel] = quad_overlap_gpu(subBlock);

%{
TAYLOR'S METHOD:
?
%}

%% 2. For each block, compute the average gray value as dominnt feature

% We also compute variance
[block.avg_gray, block.variance] = block_variance(block.pixel);


%% 3. Sort the blocks based on the dominant feature
%{ 
ENHANCED EXPANDING BLOCK ALGORITHM

    leixgraphically sort variance
    here, sorted is the column vector of variance {0<V<255*blockSize^2}
    and key is the corresponding block in the original decomposition
%}
block = block_sort(block, 'variance');

%{
REGULAR EXPADING BLOCK ALGORITHM:
    here, sorted is the columm vector of average gray values {0<G<255}
%}
%block = block_sort(block)


%% 4. From the sorted blocks, place the blocks evenly into numBuckets groups
group = assign_to_group(block, init);

%% 5.  Create numBuckets buckets. 
% Place the blocks from groups i-1, i, and i+1 into bucket i.
bucket = assign_to_bucket(group);

%% 6-9. Expanding Block Comparison:
S = ceil(log2(blockSize));  
S = 1:m;   
S = 2.^m;

parfor n=1:numel(buckets)
    for m = 1:numel(S)
        bucket{n} = process_bucket(bucket{n}, S(n))
    end
end


%% 10. Cleanup: Create mask image from duplicated blocks;
mask = create_mask(bucket, init, size(img_gray_full)); 
% this a matrix of ZEROS where the image is presumed 'clean' and ONES there
% the image is presumed to have copy-pasted elements
imgOut = write_masked(mask, img_gray_full);       
% this image is GRAYSCALE
end