import numpy
import rsgislib.vectorattrs

def add_unq_numeric_col(
    vec_file: str,
    vec_lyr: str,
    unq_col: str,
    out_col: str,
    out_vec_file: str,
    out_vec_lyr: str,
    out_format: str = "GPKG",
    lut_json_file: str = None,
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
    import pandas

    import rsgislib.tools.utils
    import rsgislib.vectorutils

    out_format = rsgislib.vectorutils.check_format_name(out_format)

    base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)
    unq_vals = base_gpdf[unq_col].unique()

    base_gpdf[out_col] = numpy.zeros((base_gpdf.shape[0]), dtype=int)
    lut = dict()
    lut["id"] = dict()
    lut["val"] = dict()
    num_unq_val = 1
    for unq_val in unq_vals:
        if pandas.api.types.is_integer_dtype(unq_val):
            unq_val = int(unq_val)
        elif pandas.api.types.is_float_dtype(unq_val):
            unq_val = float(unq_val)
        elif pandas.api.types.is_string_dtype(unq_val):
            unq_val = str(unq_val)

        sel_rows = base_gpdf[unq_col] == unq_val
        base_gpdf.loc[sel_rows, out_col] = num_unq_val
        lut["id"][num_unq_val] = unq_val
        lut["val"][unq_val] = num_unq_val
        num_unq_val += 1

    if out_format == "GPKG":
        base_gpdf.to_file(out_vec_file, layer=out_vec_lyr, driver=out_format)
    else:
        base_gpdf.to_file(out_vec_file, driver=out_format)

    if lut_json_file is not None:
        rsgislib.tools.utils.write_dict_to_json(lut, lut_json_file)


vec_file = "/home/pete/Documents/gmw_v3_regional_stats/data/UNboundaries_wEEZ_fix.gpkg"
vec_lyr = "UNboundaries_wEEZ_fix"

fid_vec_file = "/home/pete/Documents/gmw_v3_regional_stats/data/UNboundaries_wEEZ_fix_fid.gpkg"
fid_vec_lyr = "UNboundaries_wEEZ_fix_fid"

rsgislib.vectorattrs.add_fid_col(vec_file, vec_lyr, fid_vec_file, fid_vec_lyr, out_format = 'GPKG', out_col = 'gmw_fid')


out_vec_file = "/home/pete/Documents/gmw_v3_regional_stats/data/UNboundaries_wEEZ_fix_unq.gpkg"
out_vec_lyr = "UNboundaries_wEEZ_fix_unq"

lut_json_file = "un_boundaries_fid_lut.json"

add_unq_numeric_col(
    vec_file=fid_vec_file,
    vec_lyr=fid_vec_lyr,
    unq_col="gmw_fid",
    out_col="gmw_fid_uid",
    out_vec_file=out_vec_file,
    out_vec_lyr=out_vec_lyr,
    out_format = "GPKG",
    lut_json_file = lut_json_file,
)
