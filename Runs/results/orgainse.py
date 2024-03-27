import os 
import shutil
import re

dir = r"N:\DASH\Runs\results"

parent_dir = r"N:\DASH\Runs"

organise = re.compile(r'JaneDoe3[X|Y]_.*?_(\d+)_.*\.(json|txt)')

for file in os.listdir(dir):
    fp = os.path.join(dir, file)
    #print("Processing file: ", fp)
    if os.path.isfile(fp):
        match = organise.match(file)
        if match:
            run_number = int(match.group(1))
            print("There was a match")
            existing_results_folder = os.path.join(parent_dir, f'Run_ {run_number}')
            results_folder = os.path.join(parent_dir, f'Run_{run_number}', 'results')
            if not os.path.exists(results_folder):
                os.makedirs(results_folder)
            destination_file = os.path.join(results_folder, file)
            if not os.path.exists(destination_file):
                shutil.copy(fp, results_folder)
            else: 
                print(f"File {file} already exists in {results_folder}. Skipping")
        else: 
            print(f"File {fp} does not match the expected pattern. Will skip it.")