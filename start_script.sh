
organise_files
dir_prefix = "N:\\"

dir_data = "${dir_prefix}DASH\\Runs\\data\\organise.py"
dir_results =  "${dir_prefix}DASH\\Runs\\results\\organise.py"
dir_results_rc = "${dir_prefix}\\DASH\\Runs\\data\\organise_IV.py"
dir_main_tests = "${dir_prefix}DASH\\Tests\\main_tests.py"
dir_RC = "${dir_prefix}DASH\\Tests\\noise_channel_2.py"
dir_IV = "${dir_prefix}DASH\\Tests\\IV_2.py"
dir_generate_roots = "${dir_prefix}DASH\\generate_roots.py"
dir_generate_graphs = "${dir_prefix}DASH\\generate_graph.py"
#!/bin/bash

python_files=(
    "$dir_data"
    "$dir_results"
    "$dir_results_rc"
    "$dir_main_tests"
    "$dir_RC"
    "$dir_IV"
    "$dir_generate_roots"
    "$dir_generate_graphs"
)


for file in "${python_files[@]}"; do
    echo "Executing $file"
    python "$file"
done


#  */30 * * * * N:\\DASH\\start_script.sh