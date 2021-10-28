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
                    combined_stats[uid]['count'][0] += tile_stats_dict[uid]['count'][0]
                    combined_stats[uid]['area'][0] += tile_stats_dict[uid]['area'][0]
                    combined_stats[uid]['count'][1] += tile_stats_dict[uid]['count'][1]
                    combined_stats[uid]['area'][1] += tile_stats_dict[uid]['area'][1]

    combined_stats_vld = dict()
    for uid in combined_stats:
        if (combined_stats[uid]['count'][0] > 0) and (combined_stats[uid]['count'][1] > 0):
            combined_stats_vld[uid] = combined_stats[uid]

    writeDict2JSON(combined_stats_vld, out_json_file)

    if (out_feather is not None) or (out_excel is not None) or (out_csv is not None):
        df_dict = dict()
        df_dict['uid'] = list()
        df_dict['count_loss'] = list()
        df_dict['area_loss'] = list()
        df_dict['count_gain'] = list()
        df_dict['area_gain'] = list()

        if uid_lut_file is not None:
            uid_lut_dict = readJSON2Dict(uid_lut_file)
            df_dict['region'] = list()


        for uid in combined_stats_vld:
            df_dict['uid'].append(uid)
            df_dict['count_gain'].append(combined_stats_vld[uid]['count'][0])
            df_dict['area_gain'].append(combined_stats_vld[uid]['area'][0])
            df_dict['count_loss'].append(combined_stats_vld[uid]['count'][1])
            df_dict['area_loss'].append(combined_stats_vld[uid]['area'][1])
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


out_dir = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/gmw_v3_chng_f1996_v312"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

for year in ['2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']:
    merge_gmw_tile_stats(tile_stats_dir='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/chng_f1996/gmw_v3_f1996_t{}_v312'.format(year),
                         out_json_file=os.path.join(out_dir, "gmw_v3_chng_f1996_t{}_v312_country_stats.json".format(year)),
                         uid_lut_file="/scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json",
                         out_feather=os.path.join(out_dir, "gmw_v3_chng_f1996_t{}_v312_country_stats.feather".format(year)),
                         out_excel=os.path.join(out_dir, "gmw_v3_chng_f1996_t{}_v312_country_stats.xlsx".format(year)),
                         excel_sheet="chng_f1996_t{}_v312".format(year),
                         out_csv=os.path.join(out_dir, "gmw_v3_chng_f1996_t{}_v312_country_stats.csv".format(year)))


out_dir = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/gmw_v3_annual_chng_v312"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
for i, year in enumerate(years):
    if year != '2020':
        merge_gmw_tile_stats(tile_stats_dir='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/annual_chngs/gmw_v3_f{}_t{}_v312'.format(year, years[i+1]),
                             out_json_file=os.path.join(out_dir, "gmw_v3_chng_f{}_t{}_v312_country_stats.json".format(year, years[i+1])),
                             uid_lut_file="/scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json",
                             out_feather=os.path.join(out_dir, "gmw_v3_chng_f{}_t{}_v312_country_stats.feather".format(year, years[i+1])),
                             out_excel=os.path.join(out_dir, "gmw_v3_chng_f{}_t{}_v312_country_stats.xlsx".format(year, years[i+1])),
                             excel_sheet="chng_f{}_t{}_v312".format(year, years[i+1]),
                             out_csv=os.path.join(out_dir, "gmw_v3_chng_f{}_t{}_v312_country_stats.csv".format(year, years[i+1])))



