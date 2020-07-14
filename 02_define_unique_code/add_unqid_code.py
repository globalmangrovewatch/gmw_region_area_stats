

def add_unq_id_val(vec_file, vec_lyr, unq_col, unq_id_col, out_vec_file, out_vec_lyr, out_format="GPKG", lut_json_file=None):
    """
    A function which splits a vector layer by an attribute value into either different layers or different output
    files.

    :param vec_file: Input vector file
    :param vec_lyr: Input vector layer
    :param unq_col: The column name used to define unique regions.
    :param unq_id_col: The output column name used to create a numeric unique ID
    :param out_vec_file: The output vector file with the selected features.
    :param out_vec_lyr: The output layer file with the selected features.
    :param out_format: the output vector format (Default: GPKG)
    :param lut_json_file: An output file with the LUT linking numeric ID and region unique value.
                          If None no output is produced.

    """
    import geopandas
    import numpy
    import tqdm

    base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)
    unq_vals = base_gpdf[unq_col].unique()
    base_gpdf[unq_id_col] = numpy.zeros((base_gpdf.shape[0]), dtype=int)

    unq_id_val = 1
    lut = dict()
    lut['id'] = dict()
    lut['val'] = dict()
    for unq_val in tqdm.tqdm(unq_vals):
        base_gpdf.loc[base_gpdf[unq_col] == unq_val, unq_id_col] = unq_id_val
        lut['id'][unq_id_val] = unq_val
        lut['val'][unq_val] = unq_id_val
        unq_id_val += 1

    if out_format == 'GPKG':
        base_gpdf.to_file(out_vec_file, layer=out_vec_lyr, driver=out_format)
    else:
        base_gpdf.to_file(out_vec_file, driver=out_format)

    if lut_json_file is not None:
        import rsgislib
        rsgis_utils = rsgislib.RSGISPyUtils()
        rsgis_utils.writeDict2JSON(lut, lut_json_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--vecfile", type=str, required=True, help="Input File.")
    parser.add_argument("--veclyr", type=str, required=True, help="Input vector layer.")
    parser.add_argument("--unqcol", type=str, required=True, help="Unique Values Column.")
    parser.add_argument("--unqidcol", type=str, required=True, help="Unique ID column.")
    parser.add_argument("--outvecfile", type=str, required=True, help="Output File.")
    parser.add_argument("--outveclyr", type=str, required=True, help="Output vector layer.")
    parser.add_argument("--format", type=str, required=True, help="Output vector format.")
    parser.add_argument("--lut", type=str, required=False, help="Output LUT JSON file.")

    args = parser.parse_args()
    add_unq_id_val(args.vecfile, args.veclyr, args.unqcol, args.unqidcol, args.outvecfile,
                   args.outveclyr, args.format, args.lut)





