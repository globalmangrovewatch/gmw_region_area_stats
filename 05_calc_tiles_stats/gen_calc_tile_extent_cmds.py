from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import rsgislib
import logging
import os
import glob
import geopandas

logger = logging.getLogger(__name__)

class GenTileExtentCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        base_gpdf = geopandas.read_file(kwargs['roi_vec'], layer=kwargs['roi_vec_lyr'])
        unq_vals = base_gpdf[kwargs['roi_vec_col']].unique().tolist() 
        base_gpdf = None

        rsgis_utils = rsgislib.RSGISPyUtils()
        img_tiles = glob.glob(kwargs['img_tiles'])
        for img_tile in img_tiles:
            tile_base_name = rsgis_utils.get_file_basename(img_tile, checkvalid=False)
            out_file = os.path.join(kwargs['out_path'], "{}_stats.json".format(tile_base_name))
            if not os.path.exists(out_file):
                tile_generic_base_name = tile_base_name.replace(kwargs['tile_name_rm'], '')
                tile_roi_img = os.path.join(kwargs['roi_img_path'], "{}_roi.kea".format(tile_generic_base_name))
                if not os.path.exists(tile_roi_img):
                    raise Exception("Could not file ROI image file: {}".format(tile_roi_img))
                tile_pxa_img = os.path.join(kwargs['pxa_img_path'], "{}_pxa.kea".format(tile_generic_base_name))
                if not os.path.exists(tile_pxa_img):
                    raise Exception("Could not file Pixel Area image file: {}".format(tile_pxa_img))

                c_dict = dict()
                c_dict['img_tile'] = img_tile
                c_dict['unq_vals'] = unq_vals
                c_dict['tile_pxa_img'] = tile_pxa_img
                c_dict['tile_roi_img'] = tile_roi_img
                c_dict['out_file'] = out_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Country Statistics
        """
        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw1996v2.0/*.tif',
                              tile_name_rm='_gmw1996v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg',
                              roi_vec_lyr='National',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/1996')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2007v2.0/*.tif',
                              tile_name_rm='_gmw2007v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg',
                              roi_vec_lyr='National',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2007')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2008v2.0/*.tif',
                              tile_name_rm='_gmw2008v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg',
                              roi_vec_lyr='National',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2008')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2009v2.0/*.tif',
                              tile_name_rm='_gmw2009v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg',
                              roi_vec_lyr='National',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2009')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2010v2.0/*.tif',
                              tile_name_rm='_gmw2010v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg',
                              roi_vec_lyr='National',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2010')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2015v2.0/*.tif',
                              tile_name_rm='_gmw2015v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg',
                              roi_vec_lyr='National',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2015')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2016v2.0/*.tif',
                              tile_name_rm='_gmw2016v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/GADM_EEZ_WCMC_UnqID.gpkg',
                              roi_vec_lyr='National',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/country_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/country_stats/tile_stats/2016')
        """

        # WDPA Statistics
        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw1996v2.0/*.tif',
                              tile_name_rm='_gmw1996v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/wdpa_july2020_regions_ramsar_UnqID.gpkg',
                              roi_vec_lyr='polys',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/wdpa_ramsar_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/wdpa_ramsar_stats/tile_stats/1996')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2007v2.0/*.tif',
                              tile_name_rm='_gmw2007v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/wdpa_july2020_regions_ramsar_UnqID.gpkg',
                              roi_vec_lyr='polys',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/wdpa_ramsar_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/wdpa_ramsar_stats/tile_stats/2007')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2008v2.0/*.tif',
                              tile_name_rm='_gmw2008v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/wdpa_july2020_regions_ramsar_UnqID.gpkg',
                              roi_vec_lyr='polys',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/wdpa_ramsar_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/wdpa_ramsar_stats/tile_stats/2008')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2009v2.0/*.tif',
                              tile_name_rm='_gmw2009v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/wdpa_july2020_regions_ramsar_UnqID.gpkg',
                              roi_vec_lyr='polys',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/wdpa_ramsar_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/wdpa_ramsar_stats/tile_stats/2009')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2010v2.0/*.tif',
                              tile_name_rm='_gmw2010v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/wdpa_july2020_regions_ramsar_UnqID.gpkg',
                              roi_vec_lyr='polys',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/wdpa_ramsar_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/wdpa_ramsar_stats/tile_stats/2010')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2015v2.0/*.tif',
                              tile_name_rm='_gmw2015v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/wdpa_july2020_regions_ramsar_UnqID.gpkg',
                              roi_vec_lyr='polys',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/wdpa_ramsar_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/wdpa_ramsar_stats/tile_stats/2015')

        self.gen_command_info(img_tiles='/scratch/a.pfb/gmw_calc_region_area_stats/data/gmw_tiles_v2/gmw2016v2.0/*.tif',
                              tile_name_rm='_gmw2016v2.0',
                              roi_vec='/scratch/a.pfb/gmw_calc_region_area_stats/data/wdpa_july2020_regions_ramsar_UnqID.gpkg',
                              roi_vec_lyr='polys',
                              roi_vec_col='unqid',
                              pxa_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/pixel_area_tiles',
                              roi_img_path='/scratch/a.pfb/gmw_calc_region_area_stats/data/roi_tiles/wdpa_ramsar_roi_tiles',
                              out_path='/scratch/a.pfb/gmw_calc_region_area_stats/stats/wdpa_ramsar_stats/tile_stats/2016')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_tiles_stats", 8224, '/scratch/a.pfb/gmw_calc_region_area_stats/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

    def run_check_outputs(self):
        process_tools_mod = 'calc_tile_gmw_extents'
        process_tools_cls = 'CalcTileGMWExtent'
        time_sample_str = self.generate_readable_timestamp_str()
        out_err_file = 'processing_errs_{}.txt'.format(time_sample_str)
        out_non_comp_file = 'non_complete_errs_{}.txt'.format(time_sample_str)
        self.check_job_outputs(process_tools_mod, process_tools_cls, out_err_file, out_non_comp_file)


if __name__ == "__main__":
    py_script = os.path.abspath("calc_tile_gmw_extents.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    create_tools = GenTileExtentCmds(cmd=script_cmd, sqlite_db_file="gmw_tile_stats.db")
    create_tools.parse_cmds()
