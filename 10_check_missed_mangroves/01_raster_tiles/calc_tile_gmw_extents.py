from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.tools.utils
import rsgislib.imagecalc
import rsgislib.rastergis

logger = logging.getLogger(__name__)

class CalcTileGMWExtent(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='gen_calc_tile_extent_cmds.py', descript=None)

    def do_processing(self, **kwargs):
        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', self.params['img_tile'], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('cntrymsk', self.params['tile_roi_img'], 1))
        rsgislib.imagecalc.band_math(self.params['out_file'], '(gmw==1)&&(cntrymsk==0)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.pop_rat_img_stats(clumps_img=self.params['out_file'], add_clr_tab=True, calc_pyramids=True, ignore_zero=True)

    def required_fields(self, **kwargs):
        return ["img_tile", "tile_roi_img", "out_file"]

    def outputs_present(self, **kwargs):
        return os.path.exists(self.params['out_file']), dict()

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params['out_file']):
            os.remove(self.params['out_file'])

if __name__ == "__main__":
    CalcTileGMWExtent().std_run()


