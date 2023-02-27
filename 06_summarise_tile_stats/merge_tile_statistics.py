import glob
import os
import tqdm
import pandas
import rsgislib.tools.utils

def merge_gmw_tile_stats(tile_stats_dir, out_json_file, uid_lut_file=None, out_feather=None, out_excel=None, excel_sheet=None, out_csv=None):
    tile_files = glob.glob(os.path.join(tile_stats_dir, "*.json"))
    first = True
    for tile_stats_file in tqdm.tqdm(tile_files):
        tile_stats_dict = rsgislib.tools.utils.read_json_to_dict(tile_stats_file)
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

    rsgislib.tools.utils.write_dict_to_json(combined_stats_vld, out_json_file)

    if (out_feather is not None) or (out_excel is not None) or (out_csv is not None):
        df_dict = dict()
        df_dict['uid'] = list()
        df_dict['count'] = list()
        df_dict['area'] = list()

        if uid_lut_file is not None:
            uid_lut_dict = rsgislib.tools.utils.read_json_to_dict(uid_lut_file)
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
            xls_writer = pandas.ExcelWriter(out_excel, engine='xlsxwriter')
            df_stats.to_excel(xls_writer, sheet_name=excel_sheet)
            xls_writer.save()



out_dir = f"/home/pete/Documents/gmw_v3_regional_stats/data/stats/country_stats/gmw_v3_stats"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

for year in ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']:
    merge_gmw_tile_stats(tile_stats_dir=f'/home/pete/Documents/gmw_v3_regional_stats/data/stats/country_stats/tile_stats/gmw_{year}_v3',
                         out_json_file=os.path.join(out_dir, f"gmw_v3_{year}_m49_un1_stats.json"),
                         uid_lut_file="../02_define_unique_code/un_boundaries_m49_un1_lut.json",
                         out_feather=os.path.join(out_dir, f"gmw_v3_{year}_m49_un1_stats.feather"),
                         out_excel=os.path.join(out_dir, f"gmw_v3_{year}_m49_un1_stats.xlsx"),
                         excel_sheet=f"gmw_v3_{year}",
                         out_csv=os.path.join(out_dir, f"gmw_v3_{year}_m49_un1_stats.csv"),)
