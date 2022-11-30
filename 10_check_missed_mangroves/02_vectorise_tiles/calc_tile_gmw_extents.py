from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import pathlib

import rsgislib
import rsgislib.tools.utils
import rsgislib.vectorutils.createvectors
import rsgislib.imagecalc

logger = logging.getLogger(__name__)

class CalcTileGMWExtent(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='gen_calc_tile_extent_cmds.py', descript=None)

    def do_processing(self, **kwargs):
        pxl_counts = rsgislib.imagecalc.count_pxls_of_val(self.params['img_tile'], vals=[1], img_band=1)
        if pxl_counts[0] > 0:
            rsgislib.vectorutils.createvectors.polygonise_raster_to_vec_lyr(self.params['out_vec_file'], self.params['out_vec_lyr'], out_format="GPKG", input_img=self.params['img_tile'], img_band = 1, mask_img = self.params['img_tile'], mask_band = 1, replace_file = True, replace_lyr = True, pxl_val_fieldname = 'PXLVAL', use_8_conn = False)
        pathlib.Path(self.params['out_file']).touch()

    def required_fields(self, **kwargs):
        return ["img_tile", "out_vec_file", "out_vec_lyr", "out_file"]

    def outputs_present(self, **kwargs):
        return os.path.exists(self.params['out_file']), dict()

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params['out_file']):
            os.remove(self.params['out_file'])

if __name__ == "__main__":
    CalcTileGMWExtent().std_run()


