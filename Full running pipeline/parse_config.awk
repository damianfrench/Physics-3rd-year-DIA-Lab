/IM_DIR/       {dir=$2}
/MRJ_DIR/      {dir_mrj=$2}
/REF_SUB/      {ref_file=$2}
/INFILE/       {date_file=$2}
/VARIABLES/    {phot_file=$2}
/CONFIG_DIR/   {dir_config=$2}
END {
  print dir, dir_mrj, ref_file, date_file, phot_file, dir_config
}