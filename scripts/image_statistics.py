import os
from pathlib import Path
import re
import cv2
import numpy as np
from tabulate import tabulate

def int_sort(filepath):
    return int(re.search(r'(\d+)', filepath).group(0))

def compute_statistics(folders):
    width = []
    height = []
    red_channel = []
    green_channel = []
    blue_channel = []
    
    statistics = {
        'width': width,
        'height': height,
        'red_channel': red_channel,
        'green_channel': green_channel,
        'blue_channel': blue_channel
    }
    for folder in folders:
        for img_path in sorted(os.listdir(folder), key=int_sort):
            img = cv2.imread(cwd / "dataset" / folder / img_path)

            # (height, width, channel)
            h, w, _ = img.shape
            statistics['width'].append(h)
            statistics['height'].append(w)

            statistics['red_channel'].append(np.mean(img[:,:,2]))
            statistics['green_channel'].append(np.mean(img[:,:,1]))
            statistics['blue_channel'].append(np.mean(img[:,:,0]))

    return statistics
                
if __name__ == "__main__":
    cwd = Path.cwd()
    objects = [Path(f.path).name for f in os.scandir(cwd / "dataset") if f.is_dir()]
    folders = sorted([cwd / "dataset" / object for object in objects])

    statistics = compute_statistics(folders)

    max_height = np.max(statistics['height'])
    max_width = np.max(statistics['width'])

    min_height = np.min(statistics['height'])
    min_width = np.min(statistics['width'])

    # round to 3 digits
    avg_height = np.round(np.mean(statistics['height']), 3)
    avg_width = np.round(np.mean(statistics['width']), 3)

    # round to 3 digits
    height_std = np.round(np.std(statistics['height']), 3)
    width_std = np.round(np.std(statistics['width']), 3)

    median_height = int(np.median(statistics['height']))
    median_width = int(np.median(statistics['width']))
    
    data = [['height', max_height, min_height, avg_height, height_std, median_height],
            ['width', max_width, min_width, avg_width, width_std, median_width]]
    tab = tabulate(data, headers=['', 'max', 'min', 'mean', 'std', 'median'], tablefmt='fancy_grid')
    print(tab, end='\n\n')

    # round to 3 digits
    avg_red = np.round(np.mean(statistics['red_channel']) / 255, 3)
    avg_green = np.round(np.mean(statistics['green_channel']) / 255, 3)
    avg_blue = np.round(np.mean(statistics['blue_channel']) / 255, 3)

    # round to 3 digits
    red_std = np.round(np.std(statistics['red_channel']) / 255, 3)
    green_std = np.round(np.std(statistics['green_channel']) / 255, 3)
    blue_std = np.round(np.std(statistics['blue_channel']) / 255, 3)

    data = [['red', avg_red, red_std],
            ['green', avg_green, green_std],
            ['red', avg_blue, blue_std]]
    tab = tabulate(data, headers=['', 'mean', 'std'], tablefmt='fancy_grid')
    print(tab)
