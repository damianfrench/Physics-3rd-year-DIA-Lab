#! /bin/csh -f

# --- Extract all config variables in one pass ---
set vars = `awk -f /home/diastudent1/Workspace/isis/register/parse_config.awk /home/diastudent1/Workspace/isis/register/process_config`
# --- Assign variables from the list ---
set dir        = $vars[1]
set dir_mrj    = $vars[2]
set ref_file   = $vars[3]
set date_file  = $vars[4]
set phot_file  = $vars[5]
set dir_config = $vars[6]

# --- Read the first column of the date file ---
set list = `awk '{print $1}' $date_file`
set run_no = $1
set i = 0
 cd $dir

 foreach file ($list)
    echo "Processing file: $file for run_no=$run_no"
    /home/diastudent1/Workspace/isis/DIAphotometry/bin/mrj_phot /home/diastudent1/Workspace/test_images_DG/ref.fits $file -c /home/Workspace_DG2/run${run_no}/config_used | grep scatter >> /home/Workspace_DG2/run${run_no}/stats.txt
    @ i = $i + 1
    mv conv.fits "conv_"$list[$i]
end

