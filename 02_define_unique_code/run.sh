#python add_unqid_code.py --vecfile /Users/pete/Dropbox/University/Research/Data/World/GADM_EEZ_WMWC/GADM_EEZ_WCMC.gpkg --veclyr National --unqcol gid_0 --unqidcol unqid --outvecfile GADM_EEZ_WCMC_UnqID.gpkg --outveclyr National --format GPKG --lut lut.json

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
python add_unqid_code.py --vecfile /scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC.gpkg --veclyr National \
--unqcol gid_0 --unqidcol unqid --outvecfile /scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg \
--outveclyr National --format GPKG --lut /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut.json

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
python add_unqid_code.py --vecfile /scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_subset.gpkg --veclyr National \
--unqcol gid_0 --unqidcol unqid --outvecfile /scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_subset_UnqID.gpkg \
--outveclyr National --format GPKG --lut /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_lut_sub.json

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
python add_unqid_code.py --vecfile /scratch/a.pfb/gmw_calc_region_area_stats/data/wdpa_july2020_regions_ramsar.gpkg --veclyr polys \
--unqcol NAME --unqidcol unqid --outvecfile /scratch/a.pfb/gmw_calc_region_area_stats/data/wdpa_july2020_regions_ramsar_UnqID.gpkg \
--outveclyr polys --format GPKG --lut /scratch/a.pfb/gmw_calc_region_area_stats/data/unq_id_wdpa_lut.json


