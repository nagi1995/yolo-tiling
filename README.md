# Improved YOLO Dataset tiling script

## Added several improvements to [nagi1995](https://github.com/nagi1995/yolo-tiling)

         -Added directory-level tiling
         -Added user choice to keep tiled files in one directory (Useful for YOLOv1-YOLOv4)
                ../datasets/images/im0.jpg  # image
                ../datasets/images/im0.txt  # label
         -Added user choice to separate files into separate directories (Useful for YOLOv5, YOLOX, YOLOR, YOLOv7, etc..)
                ../datasets/images/im0.jpg  # image
                ../datasets/labels/im0.txt  # label
         -Added creation of Images and Labels directory
         -Added empty 'null' tile saving
         -Added progress bars via tqdm


  

Users should have an annotated dataset. If the annotated object of interest is very small compared to the parent image, image tiling is recommended. 
Users are encouraged to chage the directory structures featured in the code to fit their personal systems, however the script will create the necessary directories to successfuly run.

Recommended approach: Place untiled images with their annotations into a folder called Input. The contents will be tiled and placed in a folder named Images. From there the user is given the choice to move the .TXT files into a seperate folder named Labels. 

The python script can be run in terminal or in an IDE (PyCharm works great!). 

## Recommended Annotation Services: [Roboflow](https://roboflow.com/), [LabelImg](https://github.com/heartexlabs/labelImg)


## Image [source](https://github.com/VisDrone/VisDrone-Dataset)
## Annotations should be in yolo format
## In [old version](https://github.com/slanj/yolo-tiling) version of source code, if the image is of dimensions 1360 x 765, and tile size is 512, then 1024 x 512 image is only tiled and remaining is lost
## Here, the dimensions are scaled upwards to nearest multiple of tile size (1536 x 1024 in this case) and images are tiled and annotations are modified according to new dimensions
## Please compare the results in [old version](https://github.com/nagi1995/yolo-tiling/tree/main/old_version) and [this version](https://github.com/nagi1995/yolo-tiling/tree/main/this_version)

