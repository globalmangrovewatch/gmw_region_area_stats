from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imagecalc
import rsgislib.vectorutils

logger = logging.getLogger(__name__)

class CalcPixelArea(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='calc_pixel_area.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imagecalc.calcWSG84PixelArea(self.params['img_tile'], self.params['tile_pxa_img'],
                                              scale=10000, gdalformat='KEA')

    def required_fields(self, **kwargs):
        return ["img_tile", "tile_pxa_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['tile_pxa_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params['tile_pxa_img']):
            os.remove(self.params['tile_pxa_img'])

if __name__ == "__main__":
    CalcPixelArea().std_run()


