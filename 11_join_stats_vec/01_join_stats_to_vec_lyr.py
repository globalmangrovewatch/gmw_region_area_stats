import geopandas
import pandas

vec_file = "/home/pete/Documents/gmw_v3_regional_stats/data/UNboundaries_wEEZ_fix_unq.gpkg"
vec_lyr = "UNboundaries_wEEZ_fix_unq"
unq_col="gmw_fid_uid"

extent_stats_file = "../09_correct_mangrove_areas/gmw_v3_gmw_fid_uid_areas_corrected.feather"

data_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)

extent_stats_df = pandas.read_feather(extent_stats_file)

data_ext_stats_gpdf = pandas.merge(data_gpdf, extent_stats_df, how='inner', left_on = 'gmw_fid_uid', right_on = 'gmw_fid_uid')

data_ext_stats_gpdf.to_file("UNboundaries_wEEZ_fix_gmw_stats.gpkg", layer="UNboundaries_wEEZ_fix_gmw_stats", driver="GPKG")

data_ext_stats_df = data_ext_stats_gpdf.drop("geometry", axis=1)
data_ext_stats_df.to_excel("UNboundaries_wEEZ_fix_gmw_stats.xlsx")

