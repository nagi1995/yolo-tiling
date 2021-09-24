# YOLO Dataset tiling script

## Tile (slice) YOLO Dataset for Small Objects Detection
## Image [source](https://github.com/VisDrone/VisDrone-Dataset)
## Annotations should be in yolo format
## In [old version](https://github.com/slanj/yolo-tiling) version of source code, if the image is of dimensions 1360 x 765, and tile size is 512, then 1024 x 512 image is only tiled and remaining is lost
## Here, the dimensions are scaled upwards to nearest multiple of tile size (1536 x 1024) and images are tiled and annotations are modified according to new dimensions
## Please compare the results in [old version](https://github.com/nagi1995/yolo-tiling/tree/main/old_version) and [this version](https://github.com/nagi1995/yolo-tiling/tree/main/this_version)

