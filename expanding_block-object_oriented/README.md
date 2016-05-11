# expanding_block
detects copy-move forgery in images through comparing expanding blocks of pixels

dominant_sort:
small script which creates key values for a vector: (i.e, if a vector is V=[3, 5, 1], creates
dict =
  [3 1]
  [5, 2]
  [1 3]
...

Then sorts output lexigraphically:
sorted_dict =
  [1, 3]
  [3, 1]
  [5. 2]
This creates the hash lookup table used by expanding_block
