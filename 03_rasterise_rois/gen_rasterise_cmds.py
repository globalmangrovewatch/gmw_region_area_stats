from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import rsgislib.tools.filetools
import logging
import os
import glob

logger = logging.getLogger(__name__)

class GenTileExtentCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):

        img_tiles = glob.glob(kwargs['img_tiles'])
        for img_tile in img_tiles:
            tile_base_name = rsgislib.tools.filetools.get_file_basename(img_tile)
            tile_base_name = tile_base_name.replace(kwargs['tile_name_rm'], '')
            out_roi_file = os.path.join(kwargs['out_roi_path'], "{}_roi_{}.kea".format(tile_base_name, kwargs['roi_name']))
            if not os.path.exists(out_roi_file):
                c_dict = dict()
                c_dict['img_tile'] = img_tile
                c_dict['roi_vec'] = kwargs['roi_vec']
                c_dict['roi_vec_lyr'] = kwargs['roi_vec_lyr']
                c_dict['roi_vec_col'] = kwargs['roi_vec_col']
                c_dict['tile_roi_img'] = out_roi_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        """"""
        """
        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_qa/*.kea',
                              tile_name_rm='_tile_gmw_v3_init_qad',
                              roi_name='countries_sub',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_subset_UnqID.gpkg',
                              roi_vec_lyr='National',
                              roi_vec_col='unqid',
                              out_roi_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_sub_roi_tiles')
        """
        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw1996v2.0/*.tif',
                              tile_name_rm='_gmw1996v2.0',
                              roi_name='countries',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg',
                              roi_vec_lyr='National',
                              roi_vec_col='unqid',
                              out_roi_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_roi_tiles_v2_tiles')
        """
        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_qa/*.kea',
                              tile_name_rm='_tile_gmw_v3_init_qad',
                              roi_name='ramsar',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/wdpa_july2020_regions_ramsar_UnqID.gpkg',
                              roi_vec_lyr='polys',
                              roi_vec_col='unqid',
                              out_roi_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/wdpa_ramsar_roi_tiles')
        """

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_tiles_stats", 8224, '/scratch/a.pfb/gmw_calc_region_area_stats/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')


if __name__ == "__main__":
    py_script = os.path.abspath("rasterise_roi.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'rasterise_roi'
    process_tools_cls = 'RasteriseStatsROIs'

    create_tools = GenTileExtentCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_stats_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
