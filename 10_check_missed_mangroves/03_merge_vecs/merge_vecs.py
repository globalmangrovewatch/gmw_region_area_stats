import glob
import rsgislib.vectorutils

out_file = "/home/pete/Documents/gmw_v3_regional_stats/data/tests/gmw_v3_stats_missed_pxls.gpkg"

first = True
for year in ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']:
    print(year)
    input_vecs = glob.glob(f"/home/pete/Documents/gmw_v3_regional_stats/data/tests/tile_vectors/gmw_{year}_v3/*.gpkg")
    if first:
        rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, f"gmw_{year}_v3", False)
        first = False
    else:
        rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, f"gmw_{year}_v3", True)
