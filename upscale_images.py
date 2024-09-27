import numpy as np
import math
from PIL import Image 
from pathlib import Path 
import cv2
import os 

RESIZE_WIDTH = 500
RESIZE_HEIGHT = 500

if __name__ == "__main__":
    cwd = Path.cwd()
    objects = [Path(f.path).name for f in os.scandir(cwd / "dataset") if f.is_dir()]

    for object in objects: 
        src_folder = cwd / "dataset" / object
        dest_folder = cwd / "rescaled_dataset" / object
        
        count = 1
        for file in os.listdir(src_folder): 
            print("File " + str(count) + "/" + str(len(os.listdir(src_folder))) + " in " + object, end = "\r")
            count += 1 
            img = np.array(Image.open(src_folder / file)) 
            if (img.shape[0] != img.shape[1]): 
                smaller_dimension = np.argmin([img.shape[0],img.shape[1]])
                scale = RESIZE_WIDTH / img.shape[smaller_dimension] 
                new_shape = (int(img.shape[1]*scale), 500) if (smaller_dimension == 0) else (500, int(img.shape[0]*scale))
                resized_img = cv2.resize(img, new_shape, interpolation=cv2.INTER_CUBIC)
                top = math.floor((resized_img.shape[0] - RESIZE_HEIGHT)/2)
                bottom = resized_img.shape[0] - math.ceil((resized_img.shape[0] - RESIZE_HEIGHT)/2)
                left = math.floor((resized_img.shape[1] - RESIZE_WIDTH)/2)
                right = resized_img.shape[1] - math.ceil((resized_img.shape[1] - RESIZE_WIDTH)/2)
                new_img = Image.fromarray(resized_img[top:bottom, left:right])
            else: 
                new_img = Image.fromarray(cv2.resize(img, (RESIZE_WIDTH, RESIZE_HEIGHT), interpolation=cv2.INTER_CUBIC))
            
            if ((new_img.size[0] != 500) or (new_img.size[1] != 500)): 
                print("Whoopsie. File " + str(count) + "/" + str(len(os.listdir(src_folder))) + " in " + object) 
            new_img.save(dest_folder / file)
        print("")
