def subset_by_attribute(vec_file, vec_lyr, sub_col, sub_vals, out_vec_file, out_vec_lyr, out_format="GPKG",
                        match_type='equals'):
    """
    A function which subsets an input vector layer based on a list of values.

    :param vec_file: Input vector file.
    :param vec_lyr: Input vector layer
    :param sub_col: The column used to subset the layer.
    :param sub_vals: A list of values used to subset the layer. If using contains or start then regular expressions
                     supported by the re library can be provided.
    :param out_vec_file: The output vector file
    :param out_vec_lyr: The output vector layer
    :param out_format: The output vector format.
    :param match_type: The type of match for the subset. Options: equals (default) - the same value.
                       contains - string is anywhere within attribute value.
                       start - string matches the start of the attribute value.

    """
    import geopandas
    import pandas

    match_type = match_type.lower()
    if match_type not in ['equals', 'contains', 'start']:
        raise Exception("The match_type must be either 'equals', 'contains' or 'start'")

    base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)

    first = True
    for val in sub_vals:
        print(val)
        if match_type == 'equals':
            tmp_gpdf = base_gpdf[base_gpdf[sub_col] == val]
        elif match_type == 'contains':
            tmp_gpdf = base_gpdf[base_gpdf[sub_col].str.contains(val, na=False)]
        elif match_type == 'start':
            tmp_gpdf = base_gpdf[base_gpdf[sub_col].str.match(val, na=False)]
        else:
            raise Exception("The match_type must be either 'equals', 'contains' or 'start'")

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


subset_by_attribute('wdpa_july2020_regions.gpkg', 'polys', 'DESIG_ENG', ['Ramsar', 'RAMSAR'],
                    'wdpa_july2020_regions_ramsar.gpkg', 'polys', out_format="GPKG", match_type='contains')

