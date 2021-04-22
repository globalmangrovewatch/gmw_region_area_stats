import glob
import rsgislib
import pandas

def merge_annual_stats(input_pd_file, country_names_lut_file, out_feather=None, out_excel=None, excel_sheet=None, out_csv=None):
    rsgis_utils = rsgislib.RSGISPyUtils()
    country_names_luts = rsgis_utils.readJSON2Dict(country_names_lut_file)

    data_df = pandas.read_feather(input_pd_file)

    if data_df is not None:
        cnty_lst = list()
        for region in data_df['region']:
            cnty_lst.append(country_names_luts['gid'][region])
        data_df['name'] = cnty_lst

        data_df = data_df[['region', 'name', 'count', 'area']]

        data_df = data_df.sort_values(by=['name']).reset_index()
        data_df = data_df.drop(['index'], axis=1)
        print(data_df)

        if out_feather is not None:
            data_df.to_feather(out_feather)
        if out_csv is not None:
            data_df.to_csv(out_csv)
        if out_excel is not None:
            if excel_sheet is None:
                excel_sheet = 'gmw_stats'
            data_df.to_excel(out_excel, sheet_name=excel_sheet)


input_pd_files = "/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_v3_2010_country_stats.feather"
country_names_lut_file = "/scratch/a.pfb/gmw_calc_region_area_stats/scripts/gadm_lut.json"
out_feather="/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats_fnl/national_stats_gmw_v3_2010.feather"
out_excel="/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats_fnl/national_stats_gmw_v3_2010.xlsx"
excel_sheet='gmw_v3_2010'
out_csv="/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats_fnl/national_stats_gmw_v3_2010.csv"
merge_annual_stats(input_pd_files, country_names_lut_file, out_feather, out_excel, excel_sheet, out_csv)
