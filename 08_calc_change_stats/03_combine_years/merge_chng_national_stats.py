import glob
import pandas
import os
import rsgislib.tools.utils

def merge_annual_stats(input_pd_files, out_feather=None, out_excel=None, excel_sheet=None, out_csv=None):
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
        comb_df = comb_df[['region', '2007_count_gain', '2008_count_gain',
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

        comb_df = comb_df.sort_values(by=['region']).reset_index()
        comb_df = comb_df.drop(['index'], axis=1)

        col_count_names = ['2007_count_gain', '2008_count_gain', '2009_count_gain',
                           '2010_count_gain', '2015_count_gain', '2016_count_gain',
                           '2017_count_gain', '2018_count_gain', '2019_count_gain',
                           '2020_count_gain', '2007_count_loss', '2008_count_loss',
                           '2009_count_loss', '2010_count_loss', '2015_count_loss',
                           '2016_count_loss', '2017_count_loss', '2018_count_loss',
                           '2019_count_loss', '2020_count_loss']
        comb_df['CountSum'] = comb_df[col_count_names].sum(axis=1)
        comb_df = comb_df.drop(comb_df[comb_df['CountSum']==0].index)
        comb_df = comb_df.drop(columns=['CountSum'])
        comb_df = comb_df.drop(columns=col_count_names)
        comb_df = comb_df.sort_values(by=['region']).reset_index()
        comb_df = comb_df.rename(columns={'region': 'gmw_fid_uid'})

        print(comb_df)

        if out_feather is not None:
            comb_df.to_feather(out_feather)
        if out_csv is not None:
            comb_df.to_csv(out_csv)
        if out_excel is not None:
            if excel_sheet is None:
                excel_sheet = 'gmw_stats'
            comb_df.to_excel(out_excel, sheet_name=excel_sheet)



in_dir = "/home/pete/Documents/gmw_v3_regional_stats/data/stats/country_chng_stats/gmw_v3_chng_f1996"
out_dir = "/home/pete/Documents/gmw_v3_regional_stats/data/stats/country_chng_stats/"

input_pd_files = glob.glob(os.path.join(in_dir, f"gmw_v3_chng_f1996_t*_gmw_fid_uid_stats.feather"))
#country_names_lut_file = "../../un_boundaries_lut.json"
out_feather=os.path.join(out_dir, "gmw_v3_chng_f1996_gmw_fid_uid_stats.feather")
out_excel=os.path.join(out_dir, "gmw_v3_chng_f1996_gmw_fid_uid_stats.xlsx")
excel_sheet="gmw_v3_chng_f1996"
out_csv=os.path.join(out_dir, "gmw_v3_chng_f1996_gmw_fid_uid_stats.csv")
merge_annual_stats(input_pd_files, out_feather, out_excel, excel_sheet, out_csv)

