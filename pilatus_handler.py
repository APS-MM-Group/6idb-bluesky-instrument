"""
Handler for the Pilatus detector HDF5 files.
"""

from area_detector_handlers.handlers import AreaDetectorHDF5SingleHandler
from dask.array import from_array


class PilatusHDF5Handler(AreaDetectorHDF5SingleHandler):
    specs = (
        {"AD_HDF5_Pilatus_6idb"} | AreaDetectorHDF5SingleHandler.specs
    )

    def __call__(self, point_number):
        return from_array(super().__call__(point_number))
