from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imagecalc
import rsgislib.vectorutils.createrasters

logger = logging.getLogger(__name__)

class RasteriseStatsROIs(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='rasterise_roi.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.vectorutils.createrasters.rasterise_vec_lyr(self.params['roi_vec'], self.params['roi_vec_lyr'],
                                                             self.params['img_tile'], self.params['tile_roi_img'],
                                                             gdalformat = 'KEA', burn_val = 1,
                                                             datatype = rsgislib.TYPE_32UINT, att_column = self.params['roi_vec_col'],
                                                             use_vec_extent = False, thematic = True, no_data_val = 0)

    def required_fields(self, **kwargs):
        return ["img_tile", "roi_vec", "roi_vec_lyr", "roi_vec_col", "tile_roi_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['tile_roi_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params['tile_roi_img']):
            os.remove(self.params['tile_roi_img'])

if __name__ == "__main__":
    RasteriseStatsROIs().std_run()
