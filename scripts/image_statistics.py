import os.path
import re
import cv2
import numpy as np
from tabulate import tabulate
import argparse

def int_sort(filepath):
    return int(re.search(r'(\d+)', filepath).group(0))

def compute_statistics(dirs):
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
    for dir in dirs:
        print(f'Parsing {dir}...', end='\r', flush=True)
        for img_file in sorted(os.listdir(dir), key=int_sort):
            img_path = os.path.join(os.getcwd(), 'dataset', dir, img_file)
            img = cv2.imread(img_path)

            # (height, width, channel)
            h, w, _ = img.shape
            statistics['width'].append(h)
            statistics['height'].append(w)

            statistics['red_channel'].append(np.mean(img[:,:,2]))
            statistics['green_channel'].append(np.mean(img[:,:,1]))
            statistics['blue_channel'].append(np.mean(img[:,:,0]))
        # clear line
        print(' ' * 80, end='\r')
    return statistics
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='image_statistics.py',
                                     description='Outputs height, width, and channel statistics about the dataset')
    parser.add_argument('--filename', type=str, default='statistic.npz')
    args = parser.parse_args()
    out_filename = args.filename
    if not out_filename.endswith('.npz'):
        out_filename += '.npz'

    dataset_path = os.path.join(os.getcwd(), 'dataset')

    objects = [obj.name for obj in os.scandir(dataset_path) if obj.is_dir()]
    dirs = sorted([
        os.path.join(dataset_path, obj)
            for obj in objects
    ])
    statistics = compute_statistics(dirs)

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
    
    data = [
        ['height', max_height, min_height, avg_height, height_std, median_height],
        ['width', max_width, min_width, avg_width, width_std, median_width]
    ]
    print(' Height and width statistics:')
    tab = tabulate(data, headers=['', 'max', 'min', 'mean', 'std', 'median'], tablefmt='fancy_grid')
    print(tab, end='\n\n')

    # round to 3 digits
    avg_red = np.round(np.mean(statistics['red_channel']) / 255, 3)
    avg_green = np.round(np.mean(statistics['green_channel']) / 255, 3)
    avg_blue = np.round(np.mean(statistics['blue_channel']) / 255, 3)

    # round to 3 digits
    std_red = np.round(np.std(statistics['red_channel']) / 255, 3)
    std_green = np.round(np.std(statistics['green_channel']) / 255, 3)
    std_blue = np.round(np.std(statistics['blue_channel']) / 255, 3)

    print(' Channel statistics:')
    data = [
        ['red', avg_red, std_red],
        ['green', avg_green, std_green],
        ['red', avg_blue, std_blue]
    ]
    tab = tabulate(data, headers=['', 'mean', 'std'], tablefmt='fancy_grid')
    print(tab, end='\n\n')

    print(f'Writing data into {out_filename}...')
    np.savez(out_filename,
             avg_red=avg_red,
             avg_green=avg_green,
             avg_blue=avg_blue,
             std_red=std_red,
             std_green=std_green,
             std_blue=std_blue,
    )
    print("Done")
