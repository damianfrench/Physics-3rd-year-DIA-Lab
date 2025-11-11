#! /bin/csh -f
set run_no = $1
echo "Starting pipeline.csh"
# path for this file lol C:\Users\georg\OneDrive\Documents\DIAphotometry\register\loop.csh
# Base config template
set config_template = /home/diastudent1/Workspace/isis/register/default_config
set run_dir = /home/Workspace_DG2/run${run_no}
mkdir -p $run_dir

# Generate config file in memory and write it once
# the same as ./config_generator.sh $run_dir background_degrees gauss1_degrees gauss2_degrees gauss3_degrees $sigma1 $sigma2 $sigma3
./config_generator.sh $run_dir $2 $3 $4 $5 $6 $7 $8

# Run subtract.csh in background
echo "Running subtract.csh for run ${run_no}"
./subtract.csh $run_no
