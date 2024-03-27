import os 
import shutil
import re

dir = r"N:\DASH\Runs\results"

parent_dir = r"N:\DASH\Runs"

# Regular expression patterns for all naming conventions
pattern_jane_doe = re.compile(r'JaneDoe3[X|Y]_(\d+)_.*\.json')
pattern_sn20usbhx = re.compile(r'SN20USBHX\d+_\d+_(\d+)_.*\.json')
pattern_sn20usbhy = re.compile(r'SN20USBHY\d+_\d+_(\d+)_.*\.json')

def organize_file(file, run_number):
    if run_number is not None:
        results_folder = os.path.join(parent_dir, f'Run_{run_number}', 'results')
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)
        destination_file = os.path.join(results_folder, file)
        if not os.path.exists(destination_file):
            shutil.copy(fp, results_folder)
        else:
            print(f"File {file} already exists in {results_folder}. Skipping")

for file in os.listdir(dir):
    fp = os.path.join(dir, file)
    if os.path.isfile(fp):
        match_jane_doe = pattern_jane_doe.match(file)
        match_sn20usbhx = pattern_sn20usbhx.match(file)
        match_sn20usbhy = pattern_sn20usbhy.match(file)
        
        if match_jane_doe:
            run_number = int(match_jane_doe.group(1))
            print("Matched JaneDoe3 pattern")
            organize_file(file, run_number)
        elif match_sn20usbhx:
            run_number = int(match_sn20usbhx.group(1))
            print("Matched SN20USBHX pattern")
            organize_file(file, run_number)
        elif match_sn20usbhy:
            run_number = int(match_sn20usbhy.group(1))
            print("Matched SN20USBHY pattern")
            organize_file(file, run_number)
        else:
            print(f"File {fp} does not match any expected pattern. Will skip it.")