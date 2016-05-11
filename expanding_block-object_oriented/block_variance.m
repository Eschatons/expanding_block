function [avg_gray, variance, std_dev] = block_variance(pixel)
% find the variance of a block and output as a column vector
f_mean = @(A) sum(A(:)/numel(A));
f_variance = @(A, avg) sum(A(:)-avg);
avg_gray =  num2cell(cellfun(f_mean, pixel)); % cell for cellfunc
variance = cellfun(f_variance, pixel, avg_gray);
variance = reshape(variance, numel(variance), 1);
std_dev = sqrt(variance);
end