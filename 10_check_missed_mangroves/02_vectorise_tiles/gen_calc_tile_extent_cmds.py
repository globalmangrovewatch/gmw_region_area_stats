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
            out_file = os.path.join(kwargs['out_path'], f"{tile_base_name}.txt")
            out_vec_file = os.path.join(kwargs['out_path'], f"{tile_base_name}.gpkg")
            out_vec_lyr = f"{tile_base_name}"
            if not os.path.exists(out_file):
                c_dict = dict()
                c_dict['img_tile'] = img_tile
                c_dict['out_vec_file'] = out_vec_file
                c_dict['out_vec_lyr'] = out_vec_lyr
                c_dict['out_file'] = out_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Country Statistics
        for year in ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']:
            print(year)
            self.gen_command_info(img_tiles=f'/home/pete/Documents/gmw_v3_regional_stats/data/tests/tile_rasters/gmw_{year}_v3/*.kea',
                                  out_path=f'/home/pete/Documents/gmw_v3_regional_stats/data/tests/tile_vectors/gmw_{year}_v3')

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
