# Primary Reference: https://github.com/slanj/yolo-tiling/blob/main/tile_yolo.py
# Secondary Reference: https://github.com/nagi1995/yolo-tiling/tile_yolo.py


'''
@ Co-authored by David Schmitt (https://github.com/David-Schmitt)
@ Co-authored by Emerson de Lemmus (https://github.com/emersondelemmus)
@ Purpose: YOLOv1 - YOLOv7 image tiler.
@ Notes: Added directory-level tiling
         Added empty 'null' tile saving along with annotated tiles
         Added creation of Images and Labels directory
         Added user choice to keep tiled files in one directory
            Useful for YOLOv1 - YOLOv4:
                ../datasets/images/im0.jpg  # image
                ../datasets/images/im0.txt  # label
         Added user choice to separate files into separate directories
            Useful for YOLOv5, YOLOR, YOLOX, YOLOv7, PP-YOLO, etc.:
                ../datasets/images/im0.jpg  # image
                ../datasets/labels/im0.txt  # label
         Added progress bars via tqdm

'''

import pandas as pd
import numpy as np
from time import sleep
from tqdm import tqdm, trange
from shapely.geometry import Polygon
import cv2
import math
import os
import shutil
import glob


def tiler(imnames, newpath, falsepath, slice_size, ext):
    print('Tiling...')
    for imname in tqdm(imnames):
        sleep(0.000001)
        im = cv2.imread(imname)
        height, width, _ = im.shape
        h_new = math.ceil(height/slice_size) * slice_size
        w_new = math.ceil(width/slice_size) * slice_size
        im = cv2.resize(im, (w_new, h_new), cv2.INTER_LINEAR)
        labname = imname.replace(ext, '.txt')
        labels = pd.read_csv(labname, sep=' ', names=['class', 'x1', 'y1', 'w', 'h'])
        
        # we need to rescale coordinates from 0-1 to real image height and width
        labels[['x1', 'w']] = labels[['x1', 'w']] * w_new
        labels[['y1', 'h']] = labels[['y1', 'h']] * h_new
        
        boxes = []
        
        # convert bounding boxes to shapely polygons. We need to invert Y and find polygon vertices from center points
        for row in labels.iterrows():
            x1 = row[1]['x1'] - row[1]['w']/2
            y1 = (h_new - row[1]['y1']) - row[1]['h']/2
            x2 = row[1]['x1'] + row[1]['w']/2
            y2 = (h_new - row[1]['y1']) + row[1]['h']/2

            boxes.append((int(row[1]['class']), Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])))
        

        # create tiles and find intersection with bounding boxes for each tile
        for i in range((h_new // slice_size)):
            for j in range((w_new // slice_size)):
                x1 = j*slice_size
                y1 = h_new - (i*slice_size)
                x2 = ((j+1)*slice_size) - 1
                y2 = (h_new - (i+1)*slice_size) + 1

                pol = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
                imsaved = False
                slice_labels = []

                for box in boxes:
                    if pol.intersects(box[1]):
                        inter = pol.intersection(box[1])        
                        
                        if not imsaved:
                            sliced_im = im[i*slice_size:(i+1)*slice_size, j*slice_size:(j+1)*slice_size]
                            
                            filename = imname.split('/')[-1]
                            slice_path = newpath + "/" + filename.replace(ext, f'_{i}_{j}{ext}')                            
                            slice_labels_path = newpath + "/" + filename.replace(ext, f'_{i}_{j}.txt')
                            cv2.imwrite(slice_path, sliced_im)
                            imsaved = True                    
                        
                        # get smallest rectangular polygon (with sides parallel to the coordinate axes) that contains the intersection
                        new_box = inter.envelope 
                        
                        # get central point for the new bounding box 
                        centre = new_box.centroid
                        
                        # get coordinates of polygon vertices
                        x, y = new_box.exterior.coords.xy
                        
                        # get bounding box width and height normalized to slice size
                        new_width = (max(x) - min(x)) / slice_size
                        new_height = (max(y) - min(y)) / slice_size
                        
                        # we have to normalize central x and invert y for yolo format
                        new_x = (centre.coords.xy[0][0] - x1) / slice_size
                        new_y = (y1 - centre.coords.xy[1][0]) / slice_size
                        
                        

                        slice_labels.append([box[0], new_x, new_y, new_width, new_height])
                
                if len(slice_labels) > 0:
                    slice_df = pd.DataFrame(slice_labels, columns=['class', 'x1', 'y1', 'w', 'h'])
                    #print(slice_df)
                    slice_df.to_csv(slice_labels_path, sep=' ', index=False, header=False, float_format='%.6f')
                
                
                if not imsaved and falsepath:
                    sliced_im = im[i*slice_size:(i+1)*slice_size, j*slice_size:(j+1)*slice_size]
                    
                    filename = imname.split('/')[-1]
                    slice_path = falsepath + "/" + filename.replace(ext, f'_{i}_{j}{ext}')
                    cv2.imwrite(slice_path, sliced_im)
                    with open(slice_path.replace(ext, '.txt'), "w") as outfile:
                        outfile.write("")

                    imsaved = True
    
    print("\nTiling successfully completed!\n")


def separate_images_and_text():

    src_folder = r'./images'
    dst_folder = r'./labels/'
    text_ext = '.txt'

    # Create directory if path exists
    isExist = os.path.exists(dst_folder)
    if not isExist:
        os.makedirs(dst_folder)
        print('Created new folder: Labels')

    # search for all files with .txt extension in source directory
    pattern = '/*' + text_ext
    files = glob.glob(src_folder + pattern)

    # move the files with txt extension
    print("\nMoving annotation text files...")
    for file in tqdm(files):
        sleep(0.000001)
        # extract file name from file path
        file_name = os.path.basename(file)
        shutil.move(file, dst_folder)

    print('Tiled annotation files moved successfully!')

#%%

if __name__ == "__main__":

    # give the file extension below
    ext = ".jpg"

    # given the path to save tiled images
    newpath = "./images"

    # Create directory if path exists
    isExist = os.path.exists(newpath)
    if not isExist:
        os.makedirs(newpath)
        print('\nCreated new folder: Images\n')

    # path to images source directory
    directory_name = './input'

    # Create directory if path exists
    isExist = os.path.exists(directory_name)
    if not isExist:
        os.makedirs(directory_name)
        print('Created new folder: Input')

    # paths of images to be tiled, leave empty
    imnames = []

    for filename in os.listdir(directory_name):
        f = os.path.join(directory_name + "/", filename)
        if os.path.isfile(f) and os.path.splitext(filename)[-1] == ext:
            imnames.append(f)

    # directory where non-annotated tiles are stored
    falsefolder = "./images"

    # dimensions of the tiled image
    size = 640

    # Tile Definition Call
    tiler(imnames, newpath, falsefolder, size, ext)

    YesOrNo = input('\nSeparate .JPG and .TXT files? (Recommended for YOLOv5 or newer): Y/N: ')

    if YesOrNo == 'Y' or YesOrNo == 'y':
        # Separate Images and Text, meant for YOLOv5 onwards
        separate_images_and_text()
    else:
        print('\n\nExiting..')