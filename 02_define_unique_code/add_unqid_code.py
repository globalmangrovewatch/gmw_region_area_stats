import numpy

def add_unq_numeric_col(
    vec_file: str,
    vec_lyr: str,
    unq_col: str,
    out_col: str,
    out_vec_file: str,
    out_vec_lyr: str,
    out_format: str = "GPKG",
    lut_json_file: str = None
):
    """
    A function which adds a numeric column based off an existing column in
    the vector file.

    :param vec_file: Input vector file.
    :param vec_lyr: Input vector layer within the input file.
    :param unq_col: The column within which the unique values will be identified.
    :param out_col: The output numeric column
    :param out_vec_file: Output vector file
    :param out_vec_lyr: output vector layer name.
    :param out_format: output file format (default GPKG).
    :param lut_json_file: an optional output LUT file.

    """
    import geopandas
    import rsgislib.vectorutils
    import rsgislib.tools.utils

    out_format = rsgislib.vectorutils.check_format_name(out_format)

    base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)
    unq_vals = base_gpdf[unq_col].unique()

    base_gpdf[out_col] = numpy.zeros((base_gpdf.shape[0]), dtype=int)
    lut = dict()
    lut['id'] = dict()
    lut['val'] = dict()
    num_unq_val = 1
    for unq_val in unq_vals:
        sel_rows = base_gpdf[unq_col] == unq_val
        base_gpdf.loc[sel_rows, out_col] = num_unq_val
        lut['id'][num_unq_val] = unq_val
        lut['val'][unq_val] = num_unq_val
        num_unq_val += 1

    if out_format == "GPKG":
        base_gpdf.to_file(out_vec_file, layer=out_vec_lyr, driver=out_format)
    else:
        base_gpdf.to_file(out_vec_file, driver=out_format)

    if lut_json_file is not None:
        rsgislib.tools.utils.write_dict_to_json(lut, lut_json_file)


vec_file = "/home/pete/Documents/gmw_v3_regional_stats/data/UNBoundaries_wEEZ.gpkg"
vec_lyr = "UNBoundaries_wEEZ"

out_vec_file = "/home/pete/Documents/gmw_v3_regional_stats/data/UNBoundaries_wEEZ_unq.gpkg"
out_vec_lyr = "UNBoundaries_wEEZ_unq"


lut_json_file = "un_boundaries_lut.json"

add_unq_numeric_col(vec_file, vec_lyr, "ISO3CD", "cntry_uid", out_vec_file, out_vec_lyr, "GPKG", lut_json_file)






