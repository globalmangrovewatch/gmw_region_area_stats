from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import rsgislib.tools.filetools
import logging
import os
import glob

logger = logging.getLogger(__name__)

class GenTileExtentCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_roi_path']):
            os.mkdir(kwargs['out_roi_path'])
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
        self.gen_command_info(img_tiles='/home/pete/Documents/gmw_v3_regional_stats/data/gmw_v3_extent/gmw_v3_2020/*.tif',
                              tile_name_rm='_2020_v3',
                              roi_name='countries_sub',
                              roi_vec='/home/pete/Documents/gmw_v3_regional_stats/data/UNBoundaries_wEEZ_unq.gpkg',
                              roi_vec_lyr='UNBoundaries_wEEZ_unq',
                              roi_vec_col='cntry_uid',
                              out_roi_path='/home/pete/Documents/gmw_v3_regional_stats/data/un_country_rois')

        self.pop_params_db()

        self.create_shell_exe(
            run_script="run_exe_analysis.sh",
            cmds_sh_file="cmds_lst.sh",
            n_cores=50,
            db_info_file="pbpt_db_conn_info.json",
        )

if __name__ == "__main__":
    py_script = os.path.abspath("rasterise_roi.py")
    script_cmd = "python {}".format(py_script)

    process_tools_mod = 'rasterise_roi'
    process_tools_cls = 'RasteriseStatsROIs'

    create_tools = GenTileExtentCmds(
        cmd=script_cmd,
        db_conn_file="/home/pete/.pbpt_db_conn.txt",
        lock_file_path="./gmw_lock_file.txt",
        process_tools_mod=process_tools_mod,
        process_tools_cls=process_tools_cls,
    )

    create_tools.parse_cmds()
