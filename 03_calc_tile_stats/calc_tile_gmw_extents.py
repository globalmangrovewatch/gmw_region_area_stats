from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.vectorutils
import numpy


logger = logging.getLogger(__name__)

def calc_unq_val_pxl_areas(pix_area_img, uid_img, unq_val_area_lut):
    from rios import applier

    infiles = applier.FilenameAssociations()
    infiles.pix_area_img = pix_area_img
    infiles.uid_img = uid_img
    outfiles = applier.FilenameAssociations()
    otherargs = applier.OtherInputs()
    otherargs.unq_val_area_lut = unq_val_area_lut
    aControls = applier.ApplierControls()

    def _calcUnqValPxlArea(info, inputs, outputs, otherargs):
        unq_pix_vals = numpy.unique(inputs.uid_img[0])
        for val in unq_pix_vals:
            unq_val_area_lut[val] += numpy.sum(inputs.pix_area_img[inputs.uid_img[0] == val])

    applier.apply(_calcUnqValPxlArea, infiles, outfiles, otherargs, controls=aControls)

class CalcTileGMWExtent(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='gen_calc_tile_extent_cmds.py', descript=None)

    def do_processing(self, **kwargs):
        rsgis_utils = rsgislib.RSGISPyUtils()
        tile_base_name = rsgis_utils.get_file_basename(self.params['img_tile'], checkvalid=True)
        pix_area_img = os.path.join(self.params['tmp_dir'], "{}_pix_area.kea".format(tile_base_name))
        rsgislib.imagecalc.calcWSG84PixelArea(self.params['img_tile'], pix_area_img, scale=10000, gdalformat='KEA')

        uid_img = os.path.join(self.params['tmp_dir'], "{}_uid.kea".format(tile_base_name))
        rsgislib.vectorutils.rasteriseVecLyr(self.params['roi_vec'], self.params['roi_vec_lyr'],
                                             self.params['img_tile'], uid_img, gdalformat="KEA",
                                             burnVal=1, datatype=rsgislib.TYPE_16UINT,
                                             vecAtt=self.params['roi_vec_col'],
                                             vecExt=False, thematic=True, nodata=0)

        lut_vals = dict()
        for val in self.params['unq_vals']:
            lut_vals[val] = 0.0

        calc_unq_val_pxl_areas(pix_area_img, uid_img, lut_vals)

        rsgis_utils.writeDict2JSON(lut_vals, self.params['out_file'])

        #if os.path.exists(self.params['tmp_dir']):
        #    shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["img_tile", "unq_vals", "roi_vec", "roi_vec_lyr", "roi_vec_col", "out_file", "tmp_dir"]

    def outputs_present(self, **kwargs):
        return os.path.exists(self.params['out_file']), dict()

if __name__ == "__main__":
    CalcTileGMWExtent().std_run()


