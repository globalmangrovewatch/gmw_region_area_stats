import glob
import pandas
import os
import rsgislib.tools.utils

def merge_annual_stats(input_pd_files, country_names_lut_file, out_feather=None, out_excel=None, excel_sheet=None, out_csv=None):
    country_names_luts = rsgislib.tools.utils.read_json_to_dict(country_names_lut_file)
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



out_dir = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/gmw_v3_stats"

input_pd_files = glob.glob(os.path.join(out_dir, "gmw_v3_*_country_stats.feather"))
country_names_lut_file = "../un_boundaries_lut.json"
out_feather=os.path.join(out_dir, f"gmw_v3_country_stats.feather")
out_excel=os.path.join(out_dir, f"gmw_v3_country_stats.xlsx")
excel_sheet="gmw_v3_stats"
out_csv=os.path.join(out_dir, "gmw_v3_national_stats.csv")
merge_annual_stats(input_pd_files, country_names_lut_file, out_feather, out_excel, excel_sheet, out_csv)
