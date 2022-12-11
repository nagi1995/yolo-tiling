# Improved You Only Look Once Image Tiling

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/works-on-my-machine.svg)](https://forthebadge.com)

[![Gem Version](https://img.shields.io/badge/Python-3.9-blue)](https://badge.fury.io/rb/colorls)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com)

A python script that tiles (slices) images to a desired dimensions. Here is a screenshot of sample result using `tile_yolo.py`.

![image](https://i.imgur.com/gmcYj8b.png)

*If you're interested in knowing something for small object detection check out [this gist](https://github.com/obss/sahi).*

# Table of contents

- [Usage](#usage)
- [Installation](#installation)
- [Recommended configurations](#recommended-configurations)
- [Latest Update](#latest-update)
- [Contributing](#contributing)
- [License](#license)

# Usage

[(Back to top)](#table-of-contents)

1. Download `tile_yolo.py`.
2. Place `tile_yolo.py` in the desired directory where user would like tiled images to be stored.

    *Note: `tile_yolo.py` will automatically create the directories it requires.*

3. (Optional) Have a look at [Recommended configurations](#recommended-configurations)  

# Installation

[(Back to top)](#table-of-contents)

1. Install Python (preferably, version <= 10) [Download](https://www.python.org/downloads/release/python-3100/).

   *Note: as of this writing, Python 3.11 or greater may cause error.*

2. Download a python compatible IDE. I recommend Jupyter Notebook, PyCharm, DataSpell, or DeepNote. 

    *Note: I wouldn't recommend a cloud service such as Google Colab due to the large amount of images that may be generated.*

3. Install the required packages listed in `requirements.txt` by running the following command in the terminal: ```pip install -r requirements.txt```

# Recommended configurations

[(Back to top)](#table-of-contents)

1. Users should have an annotated dataset. Check out [Roboflow](https://roboflow.com/) or [LabelImg](https://github.com/heartexlabs/labelImg) for quick and easy YOLO image annotation. Refer to their instructions/installation requirements. 
2. When to use? Image tiling is recommended when the object of interest is very small compared to the parent image. Example: [Small Object Detection: An Image Tiling Based Approach](https://binginagesh.medium.com/small-object-detection-an-image-tiling-based-approach-bce572d890ca#fa1e)
3. `tile_yolo.py` will create the necessary directories to run successfully however, users are encouraged to modify the directory creation code to fit their personal needs!
4. Recommended approach: Place untiled images with their respective annotations into a folder called `Input`. Upon running `tile_yolo.py` the contents in `Input` will tiled to a user's desired dimensions and tiles will be placed into a folder named `Images`. Finally, a user can decide to move the tiled annotation (.txt) files into a separate folder named `Labels` or keep the tiled images and their corresponding annotations together.
 
    *Note: Keeping the tiled images and their annotations in the same directory is recommended for YOLO - YOLOv4*

    *Note: Separating tiled images into `Images` and their annotations into `Labels` is recommended for YOLOv5 - YOLOv7*

The python script can be run in terminal or in an IDE (PyCharm works great!).

# Latest Update

[(Back to top)](#table-of-contents)

## Added several improvements to [nagi1995](https://github.com/nagi1995/yolo-tiling) original

         -Added directory-level tiling (all images in folder instead of a single image) :)

         -Added user choice to keep tiled files in one directory (Recommended for YOLOv1-YOLOv4)
                ../datasets/images/im0.jpg  # image
                ../datasets/images/im0.txt  # label

         -Added user choice to separate files into separate directories (Recommended for YOLOv5, YOLOX, YOLOR, YOLOv7, etc..)
                ../datasets/images/im0.jpg  # image
                ../datasets/labels/im0.txt  # label

         -Added the creation of Images and Labels directory (user can modify code to choose a different directory)

         -Added empty 'null' tile saving (if a tile doesn't have an annotation, user can discard or save them).

         -Added progress bars via tqdm 


# Contributing

[(Back to top)](#table-of-contents)

Your contributions are always welcome! Special thanks to [Mr. David Schmitt](https://github.com/David-Schmitt)!  
