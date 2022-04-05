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



def merge_annual_stats(input_pd_files, country_names_lut_file, out_feather=None, out_excel=None, excel_sheet=None, out_csv=None):
    country_names_luts = readJSON2Dict(country_names_lut_file)
    years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
    year_info = dict()
    comb_df = None
    for year in years:
        year_info[year] = dict()
        for in_file in input_pd_files:
            if year in in_file:
                year_info[year]['year_file'] = in_file

        if 'year_file' in year_info[year]:
            yr_df = pandas.read_feather(year_info[year]['year_file'])
            yr_df = yr_df.rename(columns={'count': '{}_count'.format(year), 'area': '{}_area'.format(year)})
            yr_df = yr_df.drop(['uid'], axis=1)
            if year == '1996':
                comb_df = yr_df
            else:
                comb_df = pandas.merge(left=comb_df, right=yr_df, left_on='region', right_on='region')

    if comb_df is not None:
        cnty_lst = list()
        for region in comb_df['region']:
            cnty_lst.append(country_names_luts['gid'][region])
        comb_df['name'] = cnty_lst

        comb_df = comb_df[['region', 'name', '1996_count', '2007_count', '2008_count', '2009_count', '2010_count',
                           '2015_count', '2016_count', '2017_count', '2018_count', '2019_count', '2020_count',
                           '1996_area', '2007_area', '2008_area', '2009_area', '2010_area', '2015_area', '2016_area',
                           '2017_area', '2018_area', '2019_area', '2020_area']]

        comb_df = comb_df.sort_values(by=['name']).reset_index()
        comb_df = comb_df.drop(['index'], axis=1)
        print(comb_df)

        if out_feather is not None:
            comb_df.to_feather(out_feather)
        if out_csv is not None:
            comb_df.to_csv(out_csv)
        if out_excel is not None:
            if excel_sheet is None:
                excel_sheet = 'gmw_stats'
            comb_df.to_excel(out_excel, sheet_name=excel_sheet)


version = "v313"
for lyr in ['mjr']:#, 'min', 'max']:
    out_dir = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/gmw_v3_fnl_{}_{}".format(lyr, version)

    input_pd_files = glob.glob(os.path.join(out_dir, "gmw_v3_fnl_{}_*_{}_country_stats.feather".format(lyr, version)))
    country_names_lut_file = "../gadm_lut.json"
    out_feather=os.path.join(out_dir, "gmw_{}_{}_national_stats.feather".format(lyr, version))
    out_excel=os.path.join(out_dir, "gmw_{}_{}_national_stats.xlsx".format(lyr, version))
    excel_sheet="gmw_{}_{}".format(lyr, version)
    out_csv=os.path.join(out_dir, "gmw_{}_{}_national_stats.csv".format(lyr, version))
    merge_annual_stats(input_pd_files, country_names_lut_file, out_feather, out_excel, excel_sheet, out_csv)
