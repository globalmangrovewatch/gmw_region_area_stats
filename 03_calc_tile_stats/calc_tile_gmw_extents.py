from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.vectorutils
import numpy
import osgeo.gdal as gdal

logger = logging.getLogger(__name__)

def calc_unq_val_pxl_areas(pix_area_img, uid_img, unq_val_area_lut):
    img_uid_ds = gdal.Open(uid_img)
    if img_uid_ds is None:
        raise Exception("Could not open the UID input image.")
    img_uid_band = img_uid_ds.GetRasterBand(1)
    if img_uid_band is None:
        raise Exception("Failed to read the UID image band.")
    uid_arr = img_uid_band.ReadAsArray()
    img_uid_ds = None

    img_pixarea_ds = gdal.Open(pix_area_img)
    if img_pixarea_ds is None:
        raise Exception("Could not open the pixel area input image.")
    img_pixarea_band = img_pixarea_ds.GetRasterBand(1)
    if img_pixarea_band is None:
        raise Exception("Failed to read the pixel area image band.")
    pxl_area_arr = img_pixarea_band.ReadAsArray()
    img_pixarea_ds = None

    unq_pix_vals = numpy.unique(uid_arr)

    for unq_val in unq_pix_vals:
        if unq_val != 0:
            msk = numpy.zeros_like(uid_arr, dtype=bool)
            msk[numpy.logical_and(uid_arr == unq_val, uid_arr > 0)] = True

            unq_val_area_lut[unq_val] = dict()
            unq_val_area_lut[unq_val]['count'] = numpy.sum(msk)
            unq_val_area_lut[unq_val]['area'] = numpy.sum(pxl_area_arr[msk])


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
            lut_vals[val] = dict()
            lut_vals[val]['count'] = 0
            lut_vals[val]['area'] = 0.0

        calc_unq_val_pxl_areas(pix_area_img, uid_img, lut_vals)

        for val in self.params['unq_vals']:
            lut_vals[val]['count'] = int(lut_vals[val]['count'])
            lut_vals[val]['area'] = float(lut_vals[val]['area'])

        rsgis_utils.writeDict2JSON(lut_vals, self.params['out_file'])

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["img_tile", "unq_vals", "roi_vec", "roi_vec_lyr", "roi_vec_col", "out_file", "tmp_dir"]

    def outputs_present(self, **kwargs):
        return os.path.exists(self.params['out_file']), dict()

if __name__ == "__main__":
    CalcTileGMWExtent().std_run()


