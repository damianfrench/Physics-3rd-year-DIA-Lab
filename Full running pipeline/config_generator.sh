#!/bin/bash
# Usage: ./generate_config.sh <run_dir> <deg_bg> <deg_gauss1> <deg_gauss2> <deg_gauss3> <sigma1> <sigma2> <sigma3>

run_dir=$1
deg_bg=$2
deg_gauss1=$3
deg_gauss2=$4
deg_gauss3=$5
sigma1=$6
sigma2=$7
sigma3=$8

# Create the config file
cat > "$run_dir/config_used" << EOF
nstamps_x         10       /*** Number of stamps along X axis ***/
nstamps_y         10       /*** Number of stamps along Y axis ***/
sub_x             1        /*** Number of sub_division of the image along X axis ***/
sub_y             1        /*** Number of sub_division of the image along Y axis ***/
half_mesh_size    9        /*** Half kernel size ***/
half_stamp_size   15       /*** Half stamp size ***/
deg_bg            $deg_bg
saturation        230000   /** degree to fit background variations **/
pix_min           5.0      /*** Minimum value of the pixels to fit *****/
min_stamp_center  130      /*** Minimum value for object to enter kernel fit *****/
ngauss            3        /*** Number of Gaussians *****/
deg_gauss1        $deg_gauss1
deg_gauss2        $deg_gauss2
deg_gauss3        $deg_gauss3
sigma_gauss1      $sigma1  /*** Sigma of 1st Gaussian ****/
sigma_gauss2      $sigma2  /*** Sigma of 2nd Gaussian ****/
sigma_gauss3      $sigma3  /*** Sigma of 3rd Gaussian ****/
deg_spatial       0        /*** Degree of the fit of the spatial variations of the Kernel ****/
EOF
