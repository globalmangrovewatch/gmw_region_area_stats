from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import numpy
import osgeo.gdal as gdal

logger = logging.getLogger(__name__)

def calc_unq_val_pxl_areas(pix_area_img, uid_img, unq_val_area_lut):
    img_uid_ds = gdal.Open(uid_img)
    if img_uid_ds is None:
        raise Exception("Could not open the UID input image: '{}'".format(uid_img))
    img_uid_band = img_uid_ds.GetRasterBand(1)
    if img_uid_band is None:
        raise Exception("Failed to read the UID image band: '{}'".format(uid_img))
    uid_arr = img_uid_band.ReadAsArray()
    img_uid_ds = None

    img_pixarea_ds = gdal.Open(pix_area_img)
    if img_pixarea_ds is None:
        raise Exception("Could not open the pixel area input image: '{}'".format(pix_area_img))
    img_pixarea_band = img_pixarea_ds.GetRasterBand(1)
    if img_pixarea_band is None:
        raise Exception("Failed to read the pixel area image band: '{}'".format(pix_area_img))
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
        unq_vals = rsgis_utils.readJSON2Dict(self.params['unq_vals_file'])
        
        lut_vals = dict()
        for val in unq_vals:
            lut_vals[val] = dict()
            lut_vals[val]['count'] = 0
            lut_vals[val]['area'] = 0.0

        calc_unq_val_pxl_areas(self.params['tile_pxa_img'], self.params['tile_roi_img'], lut_vals)

        for val in unq_vals:
            lut_vals[val]['count'] = int(lut_vals[val]['count'])
            lut_vals[val]['area'] = float(lut_vals[val]['area'])

        rsgis_utils = rsgislib.RSGISPyUtils()
        rsgis_utils.writeDict2JSON(lut_vals, self.params['out_file'])


    def required_fields(self, **kwargs):
        return ["img_tile", "unq_vals_file", "tile_pxa_img", "tile_roi_img", "out_file",]

    def outputs_present(self, **kwargs):
        return os.path.exists(self.params['out_file']), dict()

if __name__ == "__main__":
    CalcTileGMWExtent().std_run()


