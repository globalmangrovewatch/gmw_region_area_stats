from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

import logging
import os
import glob
import geopandas

import rsgislib.tools.utils
import rsgislib.tools.filetools

logger = logging.getLogger(__name__)

class GenTileExtentCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_path']):
            os.mkdir(kwargs['out_path'])

        img_tiles = glob.glob(kwargs['img_tiles'])
        for img_tile in img_tiles:
            tile_base_name = rsgislib.tools.filetools.get_file_basename(img_tile, check_valid=False)
            out_file = os.path.join(kwargs['out_path'], f"{tile_base_name}_missed_mng.kea")
            if not os.path.exists(out_file):
                tile_generic_base_name = tile_base_name.replace(kwargs['tile_name_rm'], '')
                tile_roi_img = os.path.join(kwargs['roi_img_path'], "{}_roi_{}.kea".format(tile_generic_base_name, kwargs['roi_name']))
                if not os.path.exists(tile_roi_img):
                    raise Exception("Could not file ROI image file: {}".format(tile_roi_img))

                c_dict = dict()
                c_dict['img_tile'] = img_tile
                c_dict['tile_roi_img'] = tile_roi_img
                c_dict['out_file'] = out_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Country Statistics
        for year in ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']:
            print(year)
            self.gen_command_info(img_tiles=f'/home/pete/Documents/gmw_v3_regional_stats/data/gmw_v3_extent/gmw_v3_{year}/*.tif',
                                  tile_name_rm=f'_{year}_v3',
                                  roi_name='countries_sub',
                                  roi_img_path='/home/pete/Documents/gmw_v3_regional_stats/data/un_country_rois',
                                  out_path=f'/home/pete/Documents/gmw_v3_regional_stats/data/tests/tile_rasters/gmw_{year}_v3')



        self.pop_params_db()
        self.create_shell_exe(
            run_script="run_exe_analysis.sh",
            cmds_sh_file="cmds_lst.sh",
            n_cores=50,
            db_info_file="pbpt_db_conn_info.json",
        )


if __name__ == "__main__":
    py_script = os.path.abspath("calc_tile_gmw_extents.py")
    script_cmd = "python {}".format(py_script)

    process_tools_mod = 'calc_tile_gmw_extents'
    process_tools_cls = 'CalcTileGMWExtent'

    create_tools = GenTileExtentCmds(
        cmd=script_cmd,
        db_conn_file="/home/pete/.pbpt_db_conn.txt",
        lock_file_path="./gmw_lock_file.txt",
        process_tools_mod=process_tools_mod,
        process_tools_cls=process_tools_cls,
    )

    create_tools.parse_cmds()
