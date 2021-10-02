singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-beta-dev.sif python merge_tile_statistics.py

#\
#--indir /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/gmw_1996_v3_fnl \
#--outfile /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_v3_fnl_1996_country_stats.json \
#--lutfile /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json \
#--csv /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_v3_fnl_1996_country_stats.csv \
#--feather /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_v3_fnl_1996_country_stats.feather





