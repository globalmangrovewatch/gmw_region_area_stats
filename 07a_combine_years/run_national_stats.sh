singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-beta-dev.sif python merge_national_stats.py
