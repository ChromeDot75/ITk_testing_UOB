import uproot 
import os
from main_tests import ts_roots

#print(ts_roots)

target_charge = 48.0
found_1fc = None 
#print(type(target_charge))

def find_lengths(ts_roots):
    lengths = {}
    for run_number, scans_list in ts_roots.items():
        lengths[run_number] = len(scans_list)
    return lengths

lengths = find_lengths(ts_roots)
#print(lengths)


general_path = r"N:\CERN\W3_Run_63\data\strun63_"

start, end = 4, 18

files = [f"{general_path}{i}.root" for i in range(start, end)]

#print(files)

uproot_objects = {}  

for i, file_path in enumerate(files):
    key = f"fh{i+1}"
    uproot_objects[key] = uproot.open(file_path)

#print(uproot_objects)
    
for key, uproot_obj in uproot_objects.items():
    charge = uproot_obj['configuration/module_0/chip_4/Calibration voltage']
    charge = float(str(charge))
    print(charge==target_charge) 
    #print(type(charge))
    if charge == target_charge: 
        found_1fc = files[key[2:] - 1]
        break

#print(uproot_objects)
    

charges = {key: uproot_obj['configuration/module_0/chip_4/Calibration voltage'] 
           for key, uproot_obj in uproot_objects.items()}


"""
for key, charge in charges.items():

    print(f"{key}: {charge}, ", end='')

   Float_t charges[12] =
{0.749,0.998,1.248,1.497,1.746,1.996,2.993,4.010,5.007,6.004,7.999,9.897};
   Float_t chargesInDAC[12] = {   35,   48,   61,   74,   87,  100,
152,  205,  258,  309,  413,  511};

   // Use points from JK's sim
   //  including Q to mV conversion
   Float_t chargesInDAC[10] =
     {6, 22, 38, 48, 62,
      74, 100, 152, 204, 308};
   Float_t charges[10] =
     {0.192, 0.4993, 0.806, 0.99, 1.267,
      1.4969, 1.996, 2.993, 3.991, 5.985};

"""


#Run_14 - 42TS - /14 =   3    3 cycles
#R-26 - 266/14 = 19            18  cycle
#R-28 148/14 = 10.6             11 c
#R-29 164/14 = 11.7             11 c
#R_34       19.3                 18 cycles 
#R-37      53.6                  47 cycles 
