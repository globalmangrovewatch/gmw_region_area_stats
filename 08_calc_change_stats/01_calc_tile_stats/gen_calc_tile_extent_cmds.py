from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import rsgislib
import rsgislib.tools.utils
import rsgislib.tools.filetools
import logging
import os
import glob
import geopandas
import datetime

logger = logging.getLogger(__name__)

class GenTileExtentCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_path']):
            os.mkdir(kwargs['out_path'])

        if not os.path.exists(kwargs['unq_vals_file']):
            base_gpdf = geopandas.read_file(kwargs['roi_vec'], layer=kwargs['roi_vec_lyr'])
            unq_vals = base_gpdf[kwargs['roi_vec_col']].unique().tolist()
            base_gpdf = None
            rsgislib.tools.utils.write_dict_to_json(unq_vals, kwargs['unq_vals_file'])

        img_tiles = glob.glob(kwargs['img_tiles'])
        for img_tile in img_tiles:
            tile_base_name = rsgislib.tools.filetools.get_file_basename(img_tile, check_valid=False)
            out_file = os.path.join(kwargs['out_path'], "{}_stats.json".format(tile_base_name))

            if os.path.exists(out_file):
                mod_time_stamp = os.path.getmtime(img_tile)
                mod_time = datetime.datetime.fromtimestamp(mod_time_stamp)
                if mod_time > datetime.datetime(2021, 10, 29, hour=8):
                    print("Removing: {}".format(out_file))
                    os.remove(out_file)

            if not os.path.exists(out_file):
                tile_generic_base_name = tile_base_name.replace(kwargs['tile_name_rm'], '')
                tile_roi_img = os.path.join(kwargs['roi_img_path'], "{}_roi_{}.kea".format(tile_generic_base_name, kwargs['roi_name']))
                if not os.path.exists(tile_roi_img):
                    raise Exception("Could not file ROI image file: {}".format(tile_roi_img))
                tile_pxa_img = os.path.join(kwargs['pxa_img_path'], "{}_pxa.kea".format(tile_generic_base_name))
                if not os.path.exists(tile_pxa_img):
                    raise Exception("Could not file Pixel Area image file: {}".format(tile_pxa_img))

                c_dict = dict()
                c_dict['img_tile'] = img_tile
                c_dict['unq_vals_file'] = kwargs['unq_vals_file']
                c_dict['tile_pxa_img'] = tile_pxa_img
                c_dict['tile_roi_img'] = tile_roi_img
                c_dict['out_file'] = out_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Country Statistics
        for year in ['2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']:
            self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t{}_v314_kea/*.kea'.format(year),
                                  tile_name_rm='_chng_f1996_t{}_v314'.format(year),
                                  roi_name='countries',
                                  roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg',
                                  roi_vec_lyr='National',
                                  roi_vec_col='unqid',
                                  pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                                  roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_roi_tiles',
                                  unq_vals_file='/scratch/a.pfb/gmw_calc_region_area_stats/tmp/country_roi_tiles_{}_v3_mjr_unqvals.json'.format(year),
                                  out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/chng_f1996/gmw_v3_f1996_t{}_v314'.format(year))

        years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
        for i, year in enumerate(years):
            if year != '2020':
                self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f{}_t{}_v314_kea/*.kea'.format(year, years[i+1]),
                                      tile_name_rm='_chng_f{}_t{}_v314'.format(year, years[i+1]),
                                      roi_name='countries',
                                      roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg',
                                      roi_vec_lyr='National',
                                      roi_vec_col='unqid',
                                      pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                                      roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_roi_tiles',
                                      unq_vals_file='/scratch/a.pfb/gmw_calc_region_area_stats/tmp/country_roi_tiles_{}_v3_min_unqvals.json'.format(year),
                                      out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/annual_chngs/gmw_v3_f{}_t{}_v314'.format(year, years[i+1]))


        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_tiles_stats", 8224, '/scratch/a.pfb/gmw_calc_region_area_stats/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("calc_tile_gmw_extents.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'calc_tile_gmw_extents'
    process_tools_cls = 'CalcTileGMWExtent'

    create_tools = GenTileExtentCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_stats_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
