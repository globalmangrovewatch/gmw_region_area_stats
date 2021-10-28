from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import numpy
import osgeo.gdal as gdal

logger = logging.getLogger(__name__)

def calc_unq_val_pxl_areas(pix_area_img, uid_img, gmw_img, unq_val_area_lut):
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

    img_gmw_ds = gdal.Open(gmw_img)
    if img_gmw_ds is None:
        raise Exception("Could not open the GMW input image: '{}'".format(gmw_img))
    img_gmw_band = img_gmw_ds.GetRasterBand(1)
    if img_gmw_band is None:
        raise Exception("Failed to read the GMW image band: '{}'".format(gmw_img))
    gmw_arr = img_gmw_band.ReadAsArray()
    img_gmw_ds = None
    
    unq_pix_vals = numpy.unique(uid_arr)

    for unq_val in unq_pix_vals:
        if unq_val != 0:
            msk_1 = numpy.zeros_like(uid_arr, dtype=bool)
            msk_1[(uid_arr == unq_val) & (uid_arr > 0) & (gmw_arr == 1)] = True

            msk_2 = numpy.zeros_like(uid_arr, dtype=bool)
            msk_2[(uid_arr == unq_val) & (uid_arr > 0) & (gmw_arr == 2)] = True

            unq_val_area_lut[unq_val]['count'] = [numpy.sum(msk_1), numpy.sum(msk_2)]
            unq_val_area_lut[unq_val]['area'] = [numpy.sum(pxl_area_arr[msk_1]), numpy.sum(pxl_area_arr[msk_2])]


class CalcTileGMWExtent(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='gen_calc_tile_extent_cmds.py', descript=None)

    def do_processing(self, **kwargs):
        rsgis_utils = rsgislib.RSGISPyUtils()
        unq_vals = rsgis_utils.readJSON2Dict(self.params['unq_vals_file'])
        lut_vals = dict()
        for val in unq_vals:
            lut_vals[val] = dict()
            lut_vals[val]['count'] = [0, 0]
            lut_vals[val]['area'] = [0.0, 0.0]

        calc_unq_val_pxl_areas(self.params['tile_pxa_img'], self.params['tile_roi_img'], self.params['img_tile'], lut_vals)

        for val in unq_vals:
            lut_vals[val]['count'][0] = int(lut_vals[val]['count'])
            lut_vals[val]['area'][0] = float(lut_vals[val]['area'])
            lut_vals[val]['count'][1] = int(lut_vals[val]['count'])
            lut_vals[val]['area'][1] = float(lut_vals[val]['area'])

        rsgis_utils = rsgislib.RSGISPyUtils()
        rsgis_utils.writeDict2JSON(lut_vals, self.params['out_file'])

    def required_fields(self, **kwargs):
        return ["img_tile", "unq_vals_file", "tile_pxa_img", "tile_roi_img", "out_file",]

    def outputs_present(self, **kwargs):
        return os.path.exists(self.params['out_file']), dict()

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params['out_file']):
            os.remove(self.params['out_file'])

if __name__ == "__main__":
    CalcTileGMWExtent().std_run()


