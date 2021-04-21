singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif python merge_tile_statistics.py \
--indir /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2010_v3 \
--outfile /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_v3_2010_country_stats.json \
--lutfile /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json \
--csv /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_v3_2010_country_stats.csv \
--feather /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_v3_2010_country_stats.feather

#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
#/scratch/a.pfb/sw_imgs/au-eoed-dev.sif python merge_tile_statistics.py \
#--indir /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/1996 \
#--outfile /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_1996_country_stats.json \
#--lutfile /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json \
#--csv /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_1996_country_stats.csv \
#--feather /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_1996_country_stats.feather
#
#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
#/scratch/a.pfb/sw_imgs/au-eoed-dev.sif python merge_tile_statistics.py \
#--indir /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2007 \
#--outfile /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2007_country_stats.json \
#--lutfile /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json \
#--csv /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2007_country_stats.csv \
#--feather /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2007_country_stats.feather
#
#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
#/scratch/a.pfb/sw_imgs/au-eoed-dev.sif python merge_tile_statistics.py \
#--indir /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2008 \
#--outfile /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2008_country_stats.json \
#--lutfile /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json \
#--csv /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2008_country_stats.csv \
#--feather /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2008_country_stats.feather
#
#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
#/scratch/a.pfb/sw_imgs/au-eoed-dev.sif python merge_tile_statistics.py \
#--indir /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2009 \
#--outfile /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2009_country_stats.json \
#--lutfile /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json \
#--csv /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2009_country_stats.csv \
#--feather /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2009_country_stats.feather
#
#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
#/scratch/a.pfb/sw_imgs/au-eoed-dev.sif python merge_tile_statistics.py \
#--indir /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2010 \
#--outfile /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2010_country_stats.json \
#--lutfile /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json \
#--csv /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2010_country_stats.csv \
#--feather /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2010_country_stats.feather
#
#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
#/scratch/a.pfb/sw_imgs/au-eoed-dev.sif python merge_tile_statistics.py \
#--indir /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2015 \
#--outfile /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2015_country_stats.json \
#--lutfile /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json \
#--csv /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2015_country_stats.csv \
#--feather /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2015_country_stats.feather
#
#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
#/scratch/a.pfb/sw_imgs/au-eoed-dev.sif python merge_tile_statistics.py \
#--indir /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2016 \
#--outfile /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2016_country_stats.json \
#--lutfile /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json \
#--csv /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2016_country_stats.csv \
#--feather /scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/national_stats/gmw_2016_country_stats.feather




