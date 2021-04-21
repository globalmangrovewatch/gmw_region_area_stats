from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import rsgislib
import logging
import os
import glob
import geopandas

logger = logging.getLogger(__name__)

class GenTilePixAreaCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        rsgis_utils = rsgislib.RSGISPyUtils()
        img_tiles = glob.glob(kwargs['img_tiles'])
        for img_tile in img_tiles:
            tile_base_name = rsgis_utils.get_file_basename(img_tile, checkvalid=False)
            tile_base_name = tile_base_name.replace(kwargs['tile_name_rm'], '')
            out_pxa_file = os.path.join(kwargs['out_pxa_path'], "{}_pxa.kea".format(tile_base_name))
            if not os.path.exists(out_pxa_file):
                c_dict = dict()
                c_dict['img_tile'] = img_tile
                c_dict['tile_pxa_img'] = out_pxa_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_qa/*.kea',
                              tile_name_rm='_tile_gmw_v3_init_qad',
                              out_pxa_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles')
        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_tiles_pxa", 8224, '/scratch/a.pfb/gmw_calc_region_area_stats/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("calc_pixel_area.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'calc_pixel_area'
    process_tools_cls = 'CalcPixelArea'

    create_tools = GenTilePixAreaCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_stats_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
