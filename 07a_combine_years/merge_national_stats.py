import glob
import pandas
import os

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



def merge_annual_stats(input_v20_file, input_v25_file, country_names_lut_file, out_feather=None, out_excel=None, excel_sheet=None, out_csv=None):
    country_names_luts = readJSON2Dict(country_names_lut_file)

    gmw_df = pandas.read_feather(input_v20_file)
    gmw_df = gmw_df.rename(columns={'count': 'gmw_v20_count', 'area': 'gmw_v20_area'})

    gmw_tmp_df = pandas.read_feather(input_v25_file)
    gmw_tmp_df = gmw_tmp_df.rename(columns={'count': 'gmw_v25_count', 'area': 'gmw_v25_area'})
    gmw_df = pandas.merge(left=gmw_df, right=gmw_tmp_df, left_on='region', right_on='region')

    if gmw_df is not None:
        cnty_lst = list()
        for region in gmw_df['region']:
            cnty_lst.append(country_names_luts['gid'][region])
        gmw_df['name'] = cnty_lst

        gmw_df = gmw_df[['region', 'name', 'gmw_v20_count', 'gmw_v25_count', 'gmw_v20_area', 'gmw_v25_area']]

        gmw_df = gmw_df.sort_values(by=['name']).reset_index()
        gmw_df = gmw_df.drop(['index'], axis=1)
        print(gmw_df)

        if out_feather is not None:
            gmw_df.to_feather(out_feather)
        if out_csv is not None:
            gmw_df.to_csv(out_csv)
        if out_excel is not None:
            if excel_sheet is None:
                excel_sheet = 'gmw_stats'
            gmw_df.to_excel(out_excel, sheet_name=excel_sheet)



out_dir = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/gmw_v20_v25_2010"
input_v20_file = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/gmw_v20_2010/gmw_v20_2010_country_stats.feather"
input_v25_file = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/gmw_v25_2010/gmw_v25_2010_country_stats.feather"
country_names_lut_file = "../gadm_lut.json"
out_feather=os.path.join(out_dir, "gmw_v20_v25_2010_national_stats.feather")
out_excel=os.path.join(out_dir, "gmw_v20_v25_2010_national_stats.xlsx")
excel_sheet="gmw_2010"
out_csv=os.path.join(out_dir, "gmw_v20_v25_2010_national_stats.csv")
merge_annual_stats(input_v20_file, input_v25_file, country_names_lut_file, out_feather, out_excel, excel_sheet, out_csv)
