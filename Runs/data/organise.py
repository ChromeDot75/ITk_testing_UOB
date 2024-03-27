import os 
import shutil
import re


dir = "N:\Dash\Runs\data"

parent_dir = "N:\Dash\Runs"

json_organise = re.compile(r'strun(?:_info)?_(\d+)_\d+\.json')
root_organise = re.compile(r'strun(\d+)_\d+\.root')



for file in os.listdir(dir):
    fp = os.path.join(dir, file)
    if os.path.isfile(fp):
        match = json_organise.match(file)
        if match:
            run_number = int(match.group(1))
            new_folder = os.path.join(parent_dir, f'Run_{run_number}', 'data')
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            destination_file = os.path.join(new_folder, file)
            if not os.path.exists(destination_file):
                shutil.copy(fp, new_folder)
            else: 
                print(f"File {file} already exists in {new_folder}. Skipping")


for file in os.listdir(dir):
    fp = os.path.join(dir, file)
    if os.path.isfile(fp):
        match = root_organise.match(file)
        if match:
            run_number = int(match.group(1))
            new_folder = os.path.join(parent_dir, f'Run_{run_number}', 'data')
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            destination_file = os.path.join(new_folder, file)
            if not os.path.exists(destination_file):
                shutil.copy(fp, new_folder)
            else: 
                print(f"File {file} already exists in {new_folder}. Skipping")

