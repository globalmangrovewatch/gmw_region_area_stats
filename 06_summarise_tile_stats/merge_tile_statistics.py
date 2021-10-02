import glob
import os
import tqdm
import pandas

def readJSON2Dict(input_file):
    """
    Read a JSON file. Will return a list or dict.

    :param input_file: input JSON file path.

    """
    import json

    with open(input_file) as f:
        data = json.load(f)
    return data

def writeDict2JSON(data_dict, out_file):
    """
    Write some data to a JSON file. The data would commonly be structured as a dict
    but could also be a list.

    :param data_dict: The dict (or list) to be written to the output JSON file.
    :param out_file: The file path to the output file.

    """
    import json

    with open(out_file, "w") as fp:
        json.dump(
            data_dict,
            fp,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
            ensure_ascii=False,
        )


def merge_gmw_tile_stats(tile_stats_dir, out_json_file, uid_lut_file=None, out_feather=None, out_excel=None, excel_sheet=None, out_csv=None):
    tile_files = glob.glob(os.path.join(tile_stats_dir, "*.json"))
    first = True
    for tile_stats_file in tqdm.tqdm(tile_files):
        tile_stats_dict = readJSON2Dict(tile_stats_file)
        if first:
            combined_stats = tile_stats_dict
            first = False
        else:
            for uid in combined_stats:
                if uid in tile_stats_dict:
                    combined_stats[uid]['count'] += tile_stats_dict[uid]['count']
                    combined_stats[uid]['area'] += tile_stats_dict[uid]['area']

    combined_stats_vld = dict()
    for uid in combined_stats:
        if combined_stats[uid]['count'] > 0:
            combined_stats_vld[uid] = combined_stats[uid]

    writeDict2JSON(combined_stats_vld, out_json_file)

    if (out_feather is not None) or (out_excel is not None) or (out_csv is not None):
        df_dict = dict()
        df_dict['uid'] = list()
        df_dict['count'] = list()
        df_dict['area'] = list()

        if uid_lut_file is not None:
            uid_lut_dict = readJSON2Dict(uid_lut_file)
            df_dict['region'] = list()


        for uid in combined_stats_vld:
            df_dict['uid'].append(uid)
            df_dict['count'].append(combined_stats_vld[uid]['count'])
            df_dict['area'].append(combined_stats_vld[uid]['area'])
            if uid_lut_file is not None:
                df_dict['region'].append(uid_lut_dict['id'][uid])

        df_stats = pandas.DataFrame.from_dict(df_dict)
        if out_feather is not None:
            df_stats.to_feather(out_feather)
        if out_csv is not None:
            df_stats.to_csv(out_csv)
        if out_excel is not None:
            if excel_sheet is None:
                excel_sheet = 'gmw_stats'
            df_stats.to_excel(out_excel, sheet_name=excel_sheet)


for lyr in ['mjr', 'min', 'max']:
    out_dir = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/gmw_v3_fnl_{}_v309".format(lyr)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for year in ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']:
        merge_gmw_tile_stats(tile_stats_dir='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/gmw_v3_fnl_{}_{}_v309'.format(lyr, year),
                             out_json_file=os.path.join(out_dir, "gmw_v3_fnl_{}_{}_v309_country_stats.json".format(lyr, year)),
                             uid_lut_file="/scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json",
                             out_feather=os.path.join(out_dir, "gmw_v3_fnl_{}_{}_v309_country_stats.feather".format(lyr, year)),
                             out_excel=os.path.join(out_dir, "gmw_v3_fnl_{}_{}_v309_country_stats.xslx".format(lyr, year)),
                             excel_sheet="{}_{}_v309".format(lyr, year),
                             out_csv=os.path.join(out_dir, "gmw_v3_fnl_{}_{}_v309_country_stats.csv".format(lyr, year)),)




""""
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--indir", type=str, required=True, help="Input directory containing json file stats.")
    parser.add_argument("--outfile", type=str, required=True, help="Output combined statistics JSON file.")
    parser.add_argument("--lutfile", type=str, required=False, help="Optional. LUT file can be provided to populated into the excel or feather files.")
    parser.add_argument("--excel", type=str, required=False, help="Optional. Output Excel file (.xlsx).")
    parser.add_argument("--sheet", type=str, required=False, help="Optional. Name for sheet in the Excel file.")
    parser.add_argument("--csv", type=str, required=False, help="Optional. Output CSV file.")
    parser.add_argument("--feather", type=str, required=False, help="Optional. Output feather file for saving the pandas dataframe.")

    args = parser.parse_args()
    merge_gmw_tile_stats(args.indir, args.outfile, uid_lut_file=args.lutfile, out_feather=args.feather, out_excel=args.excel, excel_sheet=args.sheet, out_csv=args.csv)

"""

