# Expanding_Block:
Tests an image for copy-move forgery (a portion of an image has been copied
and then moved somewhere else within the image.)
Written in Python 3. Requires skimage, numpy, and scipy.
Written by Efron Licht, based off the algorithm
"An efficient expanding block algorithm for image copy-move forgery detection"
by Gavin Lynch, Frank Y. Shih, and Hong-Yuan Mark Liao, and published in
Information Sciences 239 in 2013.
Free for noncommerical use or modification, but please retain the above credits.
Please ask for commerical use.

## expanding_block.py:

###input:
filename that contains an mxn image (color or grayscale)
known valid formats: '.png', '.jpg'
###output:
    imageConsideredModified, imgOut
    where imageConsideredModified is True | False
    if imageConsideredModified == True,     imgOut is the original image
    if imageConsideredModified == False,    imgOut is a (2m+8) x n x 3 image
	main function.

##block_class
class definitions and initilization.
### Block:
a sub-block of a grayscale image

### expandingBlockInit:
settings for 'efficient' image forgery detection, automatically determined by image size.

## process_bucket:
compares blocks at a pixel-to-pixel level to see if they are similar.

### mask:
creates a masked image which lets the end-user visually see