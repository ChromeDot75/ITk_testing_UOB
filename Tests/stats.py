import numpy as np 
from scipy import stats 
import sys 

sys.path.append(r'N:\\DASH\\Tests')
from IV_2 import IV_data_dict
first_IV_reference = {run: data[0][1] for run, data in IV_data_dict.items()}


for run, data in IV_data_dict.items():
    current_reference = first_IV_reference[run]
    len_current_rf = len(current_reference)
    for test_data in data[1:]:
        currents = test_data[1]
        
        if len_current_rf != len(currents):
            print(f"Skip this comparison for run {run}: as lengths of arrays are different")
            continue
        t_stats, p_value = stats.ttest_rel(current_reference, currents)
        #print(f"Paired t-test for run {run}: test {idx}")
        print("t-stats value:", t_stats)
        print("With a p-value of:", p_value)

        
        significant_level = 0.05 
        
        if p_value < significant_level:
            print("We accept the Null hypothesis: Statistically Significant difference does not exists.")
        else: 
            print("We reject Null hypothesis: No statistically siginificant difference.")
        print()
    
