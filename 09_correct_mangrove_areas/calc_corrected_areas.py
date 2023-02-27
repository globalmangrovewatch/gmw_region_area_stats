import pandas

extent_file = "00_base_stats/gmw_v3_m49_un1_stats.feather"
chngs_file = "00_base_stats/gmw_v3_chng_f1996_m49_un1_stats.feather"

extent_stats_df = pandas.read_feather(extent_file)
chng_stats_df = pandas.read_feather(chngs_file)

# Find and remove the extent count columns
cols = extent_stats_df.columns
cols_rm = list()
cols_area = list()
for col in cols:
    if "count" in col:
        cols_rm.append(col)
    elif ("area" in col):
        cols_area.append(col)
print(cols_rm)
print(cols_area)
extent_stats_df = extent_stats_df.drop(columns=cols_rm)


# Find and remove the change count columns
cols = chng_stats_df.columns
cols_rm = list()
cols_area = list()
for col in cols:
    if "count" in col:
        cols_rm.append(col)
    elif ("area" in col):
        cols_area.append(col)
print(cols_rm)
print(cols_area)
chng_stats_df = chng_stats_df.drop(columns=cols_rm)
chng_stats_df = chng_stats_df.drop(columns=["index"])

# Calculate the global totals and print for info
extent_totals_df = extent_stats_df.drop(columns=["m49_un1"]).sum(axis=0)
print(extent_totals_df/100)

# Create seperate gain and loss dataframes
chng_totals_df = chng_stats_df.drop(columns=["m49_un1"]).sum(axis=0)

gain_cols = ["2007_area_gain", "2008_area_gain", "2009_area_gain", "2010_area_gain", "2015_area_gain", "2016_area_gain", "2017_area_gain", "2018_area_gain", "2019_area_gain", "2020_area_gain"]
loss_cols = ["2007_area_loss", "2008_area_loss", "2009_area_loss", "2010_area_loss", "2015_area_loss", "2016_area_loss", "2017_area_loss", "2018_area_loss", "2019_area_loss", "2020_area_loss"]

chng_loss_totals_df = chng_totals_df.drop(gain_cols)
chng_gain_totals_df = chng_totals_df.drop(loss_cols)

chng_loss_stats_df = chng_stats_df.drop(columns=gain_cols)
chng_gain_stats_df = chng_stats_df.drop(columns=loss_cols)


# Print global loss totals
print(chng_loss_totals_df/100)
# Print global gain totals
print(chng_gain_totals_df/100)


# Mangrove area correction factor
mng_om = (100-85.63061873343034)/100
mng_com = (100 - 89.28977298408603)/100
print(f"mng_om = {mng_om}")
print(f"mng_com = {mng_com}")

# Mangrove loss correction factor
loss_om = (100-73.77949765590216)/100
loss_com = (100-51.42118863049095)/100
print(f"loss_om = {loss_om}")
print(f"loss_com = {loss_com}")

# Mangrove gain correction factor
gain_om = (100-69.97109826589596)/100
gain_com = (100-50.0)/100
print(f"gain_om = {gain_om}")
print(f"gain_com = {gain_com}")

# Apply correction factor to 1996 which is the base for change.
extent_stats_corr_df = extent_stats_df.copy()
# Don't change the 1996 value - leave as mapped.
#extent_stats_corr_df["1996_area"] = extent_stats_df["1996_area"] + (extent_stats_df * mng_om) - (extent_stats_df * mng_com)

# Apply gain correction factor 
chng_gain_corr_stats_df = chng_gain_stats_df.copy()
chng_gain_corr_stats_df[gain_cols] = chng_gain_corr_stats_df[gain_cols] + (chng_gain_corr_stats_df[gain_cols] * gain_om) - (chng_gain_corr_stats_df[gain_cols] * gain_com)

# Apply loss correction factor 
chng_loss_corr_stats_df = chng_loss_stats_df.copy()
chng_loss_corr_stats_df[loss_cols] = chng_loss_corr_stats_df[loss_cols] + (chng_loss_corr_stats_df[loss_cols] * loss_om) - (chng_loss_corr_stats_df[loss_cols] * loss_com)


# Export corrected gain and loss files
chng_gain_corr_stats_df.to_csv("gmw_v3_chng_gain_corrected_m49_un1.csv")
chng_loss_corr_stats_df.to_csv("gmw_v3_chng_loss_corrected_m49_un1.csv")

chng_gain_corr_stats_df.to_feather("gmw_v3_chng_gain_corrected_m49_un1.feather")
chng_loss_corr_stats_df.to_feather("gmw_v3_chng_loss_corrected_m49_un1.feather")

chng_gain_corr_stats_df.to_excel("gmw_v3_chng_gain_corrected_m49_un1.xlsx")
chng_loss_corr_stats_df.to_excel("gmw_v3_chng_loss_corrected_m49_un1.xlsx")



# Define region as the index so all countries are correctly matched.
chng_gain_corr_stats_df = chng_gain_corr_stats_df.set_index("m49_un1")
chng_loss_corr_stats_df = chng_loss_corr_stats_df.set_index("m49_un1")
extent_stats_corr_df = extent_stats_corr_df.set_index("m49_un1")

# Calculate the corrected values per year based on change and 1996 area
gmw_chng_years = [2007, 2008, 2009, 2010, 2015, 2016, 2017, 2018, 2019, 2020]
for chng_year in gmw_chng_years: 
    extent_stats_corr_df[f"{chng_year}_area"] = extent_stats_corr_df["1996_area"] - chng_loss_corr_stats_df[f"{chng_year}_area_loss"] + chng_gain_corr_stats_df[f"{chng_year}_area_gain"]

# Find the regions which have NaN outputs as there were no gain or loss values (i.e., no change!)
no_chng_rgns_df = extent_stats_corr_df[extent_stats_corr_df.isna().any(axis=1)]

# Set no change regions to have the same mangrove area in all years.
for i, row in no_chng_rgns_df.iterrows():
    for chng_year in gmw_chng_years: 
        extent_stats_corr_df.at[i, f"{chng_year}_area"] = extent_stats_corr_df.loc[[i]]["1996_area"]

# Export Corrected Country Areas
extent_stats_corr_df = extent_stats_corr_df.reset_index()
extent_stats_corr_df.to_csv("gmw_v3_m49_un1_areas_corrected.csv")
extent_stats_corr_df.to_feather("gmw_v3_m49_un1_areas_corrected.feather")
extent_stats_corr_df.to_excel("gmw_v3_m49_un1_areas_corrected.xlsx")
