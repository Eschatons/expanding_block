function [key, sorted] = dominant_sort(word)
%{
lexigraphic sort of vector with associated keys
outputs a 2-column matrix
if given a vector in order [v1, v2, v3, v4...] with values |v1|, |v2|,
 ... |vn|
%}

if (isvector(word) == 0)
    warning('Input to dominant_sort not a vector, vectorizing anyways')
end


n = numel(word);
word = reshape(word, n, 1);
key = reshape(1:n, n, 1);
dict = [word,key];
sorted_dict = sortrows(dict);
key = sorted_dict(:, 2);
sorted = sorted_dict(:, 1);

end