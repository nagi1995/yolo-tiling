# Reference: https://github.com/slanj/yolo-tiling/blob/main/tile_yolo.py

import pandas as pd
from shapely.geometry import Polygon
import cv2
import math


def tiler(imnames, newpath, falsepath, slice_size, ext):
    for imname in imnames:
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
        
        
        #print('Image:', imname)
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
                            #print(slice_path)
                            cv2.imwrite(slice_path, sliced_im)
                            # sliced_im.save(slice_path)
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

                    sliced_im.save(slice_path)
                    #print('Slice without boxes saved')
                    imsaved = True
    
    print("tiling successfully completed")


#%%


if __name__ == "__main__":
    
    # give the file extension below
    ext = ".jpg"
    
    # given the path to save tiled images
    newpath = "./"
    
    # paths of original images to be tiled
    imnames = ["./you_image_name1.extension", "./you_image_name2.extension", "./you_image_name3.extension"]
    falsefolder = None
    # dimensions of the tiled image
    size = 512
    tiler(imnames, newpath, falsefolder, size, ext)
    