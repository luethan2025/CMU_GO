from pathlib import Path 
import shutil
import os

cwd = Path.cwd()

objects = [Path(f.path).name for f in os.scandir(cwd / "dataset") if f.is_dir()]

for object in objects: 
    Path.mkdir(cwd / "renamed_dataset" / object, exist_ok=True)

    folder = cwd / "dataset" / object
    new_dataset_folder = cwd / "renamed_dataset" / object

    count = 0
    for file in folder.glob("*.jpeg"): 
        filepath = Path(new_dataset_folder / (object+"_"+str(count)+".jpeg"))
        shutil.copy(file,filepath)
        # file.rename("apple_" + str(count))
        count += 1
    count = 0
    for file in folder.glob("*.jpg"): 
        filepath = Path(new_dataset_folder / (object+"_"+str(count)+".jpg"))
        shutil.copy(file,filepath)
        # file.rename("apple_" + str(count))
        count += 1
     

