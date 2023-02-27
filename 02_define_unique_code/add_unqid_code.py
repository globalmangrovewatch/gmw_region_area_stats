import rsgislib.vectorattrs


vec_file = "/home/pete/Documents/gmw_v3_regional_stats/data/UNBoundaries_wEEZ.gpkg"
vec_lyr = "UNBoundaries_wEEZ"

out_vec_file = "/home/pete/Documents/gmw_v3_regional_stats/data/UNBoundaries_wEEZ_unq.gpkg"
out_vec_lyr = "UNBoundaries_wEEZ_unq"

lut_json_file = "un_boundaries_m49_un1_lut.json"

rsgislib.vectorattrs.add_unq_numeric_col(
    vec_file=vec_file,
    vec_lyr=vec_lyr,
    unq_col="M49_UN1",
    out_col="m49_un1_uid",
    out_vec_file=out_vec_file,
    out_vec_lyr=out_vec_lyr,
    out_format = "GPKG",
    lut_json_file = lut_json_file,
)
