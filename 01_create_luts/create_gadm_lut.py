

def create_gadm_lut(vec_file, vec_lyr, gid_col, ctry_name_col, lut_json_file):
    """
    A function which splits a vector layer by an attribute value into either different layers or different output
    files.

    :param vec_file: Input vector file
    :param vec_lyr: Input vector layer
    :param gid_col: The column name for the GID.
    :param ctry_name_col: The column name for the country names.
    :param lut_json_file: An output file with the LUT linking numeric ID and region unique value.

    """
    import geopandas
    import rsgislib

    base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)

    lut = dict()
    lut['gid'] = dict()
    lut['ctry'] = dict()
    for i, row in base_gpdf.iterrows():
        lut['gid'][row[gid_col]] = row[ctry_name_col]
        lut['ctry'][row[ctry_name_col]] = row[gid_col]

    rsgis_utils = rsgislib.RSGISPyUtils()
    rsgis_utils.writeDict2JSON(lut, lut_json_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--vecfile", type=str, required=True, help="Input File.")
    parser.add_argument("--veclyr", type=str, required=True, help="Input vector layer.")
    parser.add_argument("--gidcol", type=str, required=True, help="Unique Values Column.")
    parser.add_argument("--ctrycol", type=str, required=True, help="Unique ID column.")
    parser.add_argument("--lut", type=str, required=True, help="Output LUT JSON file.")

    args = parser.parse_args()
    create_gadm_lut(args.vecfile, args.veclyr, args.gidcol, args.ctrycol, args.lut)





