from PIL import Image
import os
from pathlib import Path
import statistics

def list_files_recursive(directory):
    path = Path(directory)
    img_r_median = list()
    image_b_median = list()
    image_g_median = list()
    img_height_mean = 0
    img_height_median = list()

    image_width_median = list()
    image_width_mean = 0
    image_count = 0 
    for file_path in path.rglob('*'):
        if file_path.is_file():
            if(str(file_path).endswith(".jpg")):
                img = Image.open(file_path).convert('RGB')
                img_height_mean += img.height
                img_height_median.append(img.height)
                image_width_mean += img.width
                image_width_median.append(img.width)
                r ,g, b = img.split()
                image_count += 1
                
                for i in range(r.width):
                    for j in range(r.height):
                        img_r_median.append(r.getpixel((i,j)))
                        image_b_median.append(b.getpixel((i,j)))
                        image_g_median.append(g.getpixel((i,j)))
    return (statistics.mean(img_r_median)/255, statistics.mean(image_b_median)/255, 
            statistics.mean(image_g_median)/255, statistics.stdev(img_r_median)/255, 
            statistics.stdev(image_b_median)/255, statistics.stdev(image_g_median)/255, 
            statistics.mean(img_height_median),statistics.median(img_height_median),
            statistics.mean(image_width_median),statistics.median(image_width_median),
            image_count,min(img_height_median),max(img_height_median),
            min(image_width_median),max(image_width_median))
                

directory = './dataset'
res = list_files_recursive(directory)

print("image_red_mean", res[0],"\nimg_blue_mean",res[1],
      "\nimage_green_mean",res[2],"\nimage_red_std",res[3],
      "\nimage_blue_std",res[4],
      "\nmin image green std",res[5],
      "image_height_mean", res[6],"\nimg_height_median",res[7],
      "\nimage_width_mean",res[8],"\nimage_width_median",res[9],
      "\nimage_count",res[10],
      "\nmin image height",res[11], "\nmax_image_height",res[12],
      "\nmin image width", res[13], "\nmax_image_width", res[14])