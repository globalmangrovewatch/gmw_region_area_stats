import glob
import os
import tqdm
import rsgislib
import pandas

def merge_gmw_tile_stats(tile_stats_dir, out_json_file, uid_lut_file=None, out_feather=None, out_excel=None, excel_sheet=None, out_csv=None):
    rsgis_utils = rsgislib.RSGISPyUtils()
    tile_files = glob.glob(os.path.join(tile_stats_dir, "*.json"))
    first = True
    for tile_stats_file in tqdm.tqdm(tile_files):
        tile_stats_dict = rsgis_utils.readJSON2Dict(tile_stats_file)
        if first:
            combined_stats = tile_stats_dict
            first = False
        else:
            for uid in combined_stats:
                if uid in tile_stats_dict:
                    combined_stats[uid]['count'] += tile_stats_dict[uid]['count']
                    combined_stats[uid]['area'] += tile_stats_dict[uid]['area']

    for uid in combined_stats:
        if combined_stats[uid]['count'] == 0:
            combined_stats.pop(uid)

    rsgis_utils.writeDict2JSON(combined_stats, out_json_file)

    if (out_feather is not None) or (out_excel is not None) or (out_csv is not None):
        df_dict = dict()
        df_dict['uid'] = list()
        df_dict['count'] = list()
        df_dict['area'] = list()

        if uid_lut_file is not None:
            uid_lut_dict = rsgis_utils.readJSON2Dict(uid_lut_file)
            df_dict['region'] = list()

        for uid in combined_stats:
            df_dict['uid'].append(uid)
            df_dict['count'].append(combined_stats[uid]['count'])
            df_dict['area'].append(combined_stats[uid]['area'])
            if uid_lut_file is not None:
                df_dict['region'].append(uid_lut_dict['id'][uid])

        df_stats = pandas.DataFrame.from_dict(df_dict)
        if out_excel is not None:
            if excel_sheet is None:
                excel_sheet = 'gmw_stats'
            df_stats.to_excel(out_excel, excel_sheet)
        if out_feather is not None:
            df_stats.to_feather(out_feather)
        if out_csv is not None:
            df_stats.to_csv(out_csv)


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



