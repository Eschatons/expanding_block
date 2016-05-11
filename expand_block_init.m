classdef expand_block_init
    %expanding block algorithm settings
    properties
        blockSize = 32 
        % width and height of a block; total is blockSizeAin^2.
        
        blockDistance = 16   
        % distance between blocks; generally 1/4 of block size
        
        numBuckets
        % number of buckets used to compare blocks
        
        pvalThreshold
        % a value betwen 0 and 1 used for probability threshold
        
        minArea = 512
        %minimum area of duplicated region
    end
end