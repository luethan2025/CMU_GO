from pathlib import Path 
import os
import re

def int_sort(filepath):
    return int(re.search(r'(\d+)', filepath.stem).group(0))

if __name__ == "__main__":
    cwd = Path.cwd()
    objects = [Path(f.path).name for f in os.scandir(cwd / "dataset") if f.is_dir()]

    for object in objects: 
        folder = cwd / "dataset" / object

        count = 0
        for file in sorted(folder.glob("*.jpeg"), key=int_sort):
            new_file = Path(folder / (object + "_" + f"{count:02}" +".jpeg"))
            os.rename(file, new_file)
            count += 1

        count = 0
        for file in sorted(folder.glob("*.jpg"), key=int_sort):
            new_file = Path(folder / (object + "_" + f"{count:02}" +".jpeg"))
            os.rename(file, new_file)
            count += 1
