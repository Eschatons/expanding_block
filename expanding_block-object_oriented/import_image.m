function imOut = import_image(imIn)
% intelligently handles input image as source string OR array
inputErrorStr = 'input should be a nonvector matrix or path to image file';
notVector = size(imIn, 1)>1 && size(imIn, 2) > 1;
formatted = isa(imIn, 'char') || ( isnumeric(imIn) && notVector);

assert(formatted, inputErrorStr );

if isa(imIn, 'char')
    try imread(imIn);
        
    catch
        error('"%s" not a valid image filepath', imIn)
    end
    imOut = imread(imIn);
else
    imOut = imIn;
end