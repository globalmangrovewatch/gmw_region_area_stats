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
    years = ['t2007', 't2008', 't2009', 't2010', 't2015', 't2016', 't2017', 't2018', 't2019', 't2020']
    year_info = dict()
    comb_df = None
    for year in years:
        year_info[year] = dict()
        for in_file in input_pd_files:
            if year in in_file:
                year_info[year]['year_file'] = in_file

        if 'year_file' in year_info[year]:
            cln_year = year.replace('t', '')
            yr_df = pandas.read_feather(year_info[year]['year_file'])
            yr_df = yr_df.rename(columns={'count_gain': '{}_count_gain'.format(cln_year), 'area_gain': '{}_area_gain'.format(cln_year)})
            yr_df = yr_df.rename(columns={'count_loss': '{}_count_loss'.format(cln_year), 'area_loss': '{}_area_loss'.format(cln_year)})

            yr_df = yr_df.drop(['uid'], axis=1)
            if cln_year == '2007':
                comb_df = yr_df
            else:
                comb_df = pandas.merge(left=comb_df, right=yr_df, how='outer', left_on='region', right_on='region')

    if comb_df is not None:
        cnty_lst = list()
        for region in comb_df['region']:
            if region in country_names_luts['gid']:
                cnty_lst.append(country_names_luts['gid'][region])
            else:
                cnty_lst.append('NA')
        comb_df['name'] = cnty_lst

        comb_df = comb_df[['region', 'name', '2007_count_gain', '2008_count_gain',
                           '2009_count_gain', '2010_count_gain', '2015_count_gain',
                           '2016_count_gain', '2017_count_gain', '2018_count_gain',
                           '2019_count_gain', '2020_count_gain', 
                           '2007_area_gain', '2008_area_gain', '2009_area_gain',
                           '2010_area_gain', '2015_area_gain', '2016_area_gain',
                           '2017_area_gain', '2018_area_gain', '2019_area_gain',
                           '2020_area_gain', '2007_count_loss', '2008_count_loss',
                           '2009_count_loss', '2010_count_loss', '2015_count_loss',
                           '2016_count_loss', '2017_count_loss', '2018_count_loss',
                           '2019_count_loss', '2020_count_loss', 
                           '2007_area_loss', '2008_area_loss', '2009_area_loss',
                           '2010_area_loss', '2015_area_loss', '2016_area_loss',
                           '2017_area_loss', '2018_area_loss', '2019_area_loss',
                           '2020_area_loss']]

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




out_dir = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/gmw_v3_chng_f1996_v312"

input_pd_files = glob.glob(os.path.join(out_dir, "gmw_v3_chng_f1996_t*_v312_country_stats.feather"))
country_names_lut_file = "../../gadm_lut.json"
out_feather=os.path.join(out_dir, "gmw_v312_chng_f1996_national_stats.feather")
out_excel=os.path.join(out_dir, "gmw_v312_chng_f1996_national_stats.xlsx")
excel_sheet="gmw_v312_chng_f1996"
out_csv=os.path.join(out_dir, "gmw_v312_chng_f1996_national_stats.csv")
merge_annual_stats(input_pd_files, country_names_lut_file, out_feather, out_excel, excel_sheet, out_csv)




out_dir = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/gmw_v3_annual_chng_v312"

input_pd_files = glob.glob(os.path.join(out_dir, "gmw_v3_chng_*_v312_country_stats.feather"))
country_names_lut_file = "../../gadm_lut.json"
out_feather=os.path.join(out_dir, "gmw_v312_annual_chngs_national_stats.feather")
out_excel=os.path.join(out_dir, "gmw_v312_annual_chngs_national_stats.xlsx")
excel_sheet="gmw_v312_annual_chngs"
out_csv=os.path.join(out_dir, "gmw_v312_annual_chngs_national_stats.csv")
merge_annual_stats(input_pd_files, country_names_lut_file, out_feather, out_excel, excel_sheet, out_csv)
