singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif python merge_tile_statistics.py \
--indir /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_sub_stats/tile_stats/2010 \
--outfile /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_sub_stats/national_stats/gmw_2010_country_sub_stats.json \
--lutfile /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut_sub.json \
--csv /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_sub_stats/national_stats/gmw_2010_country_sub_stats.csv

#--feather /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_sub_stats/national_stats/gmw_2010_country_sub_stats.feather \
#--excel /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_sub_stats/national_stats/gmw_2010_country_sub_stats.xlsx \
#--sheet sub2010 \



