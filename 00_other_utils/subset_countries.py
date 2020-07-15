import json

def subset_by_attribute(vec_file, vec_lyr, sub_col, sub_vals, out_vec_file, out_vec_lyr, out_format="GPKG"):
    """
    A function which subsets an input vector layer based on a list of values.

    :param vec_file: Input vector file.
    :param vec_lyr: Input vector layer
    :param sub_col: The column used to subset the layer.
    :param sub_vals: A value of values used to subset the layer.
    :param out_vec_file: The output vector file
    :param out_vec_lyr: The output vector layer
    :param out_format: The output vector format.

    """
    import geopandas
    import pandas
    base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)

    first = True
    for val in sub_vals:
        print(val)
        tmp_gpdf = base_gpdf[base_gpdf[sub_col] == val]
        if first:
            out_gpdf = tmp_gpdf.copy(deep=True)
            first = False
        else:
            out_gpdf = pandas.concat([out_gpdf, tmp_gpdf])

    if out_gpdf.shape[0] > 0:
        if out_format == 'GPKG':
            out_gpdf.to_file(out_vec_file, layer=out_vec_lyr, driver=out_format)
        else:
            out_gpdf.to_file(out_vec_file, driver=out_format)
    else:
        raise Exception("No output file as no features selected.")

countries = [
            "Brazil",
            "Australia",
            "Palau",
            "Indonesia",
            "Nigeria",
            "Guinea-Bissau",
            "Suriname",
            "Belize",
            "Venezuela",
            "Côte d'Ivoire",
            "Bangladesh",
            "Papua New Guinea",
            "Pakistan",
            "Egypt",
            "Cambodia",
            "Sri Lanka",
            "Panama",
            "Vanuatu",
            "Senegal",
            "Tanzania",
            ]

with open('../gadm_lut.json') as f:
    lut = json.load(f)
    gid_lut = lut["gid"]
    ctry_lut = lut["ctry"]

sel_gids = list()
for country in countries:
    if country in ctry_lut:
        sel_gids.append(ctry_lut[country])
    else:
        print("ERROR: Country not in LUT: '{}'".format(country))

vec_file = "/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC.gpkg"
out_vec_file = "/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_subset.gpkg"
subset_by_attribute(vec_file, 'National', 'gid_0', sel_gids, out_vec_file, 'National', out_format="GPKG")


