
import geopandas
import rsgislib.tools.utils


vec_file = "/Users/pete/Dropbox/University/Research/Data/World/GADM_EEZ_WMWC/un_boundaries/UNBoundaries_wEEZ.gpkg"
#vec_file = "/home/pete/Documents/gmw_v3_regional_stats/data/UNBoundaries_wEEZ_unq.gpkg"
vec_lyr = "UNBoundaries_wEEZ"

base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)

lut = dict()
lut['gid'] = dict()
lut['ctry'] = dict()
for i, row in base_gpdf.iterrows():
    if row["ISO3CD"] in lut['gid']:
        if lut['gid'][row["ISO3CD"]] != row["ROMNAM"]:
            print("Names do not match: '{}' != '{}'".format(lut['gid'][row["ISO3CD"]], row["ROMNAM"]))
    lut['gid'][row["ISO3CD"]] = row["ROMNAM"]
    lut['ctry'][row["ROMNAM"]] = row["ISO3CD"]

rsgislib.tools.utils.write_dict_to_json(lut, "../un_boundaries_lut.json")




