from ophyd import ADComponent
from ophyd import ImagePlugin
from ophyd import PilatusDetector
from ophyd import SingleTrigger
from ophyd.areadetector.plugins import HDF5Plugin_V34 as HDF5Plugin
from ophyd.areadetector.plugins import OverlayPlugin_V34 as OverlayPlugin
from ophyd.areadetector.plugins import ROIPlugin_V34 as ROIPlugin
from ophyd.areadetector.plugins import StatsPlugin_V34 as StatsPlugin
from ophyd.areadetector.filestore_mixins import (
    FileStoreHDF5SingleIterativeWrite
)
import os

PILATUS_FILES_ROOT = "/home/det/6IDB"
BLUESKY_FILES_ROOT = "/home/beams/USER6IDB/Data"
TEST_IMAGE_DIR = "pilatus100k/%Y/%m/%d/"


class MyHDF5Plugin(FileStoreHDF5SingleIterativeWrite, HDF5Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filestore_spec = 'AD_HDF5_Pilatus_6idb'
        

class MyPilatusDetector(SingleTrigger, PilatusDetector):
    """Pilatus detector"""

    _default_configuration_attrs = (
        'roi1', 'roi2', 'roi3', 'roi4', 'cam'
    )
    _default_read_attrs = (
        'hdf1', 'stats1', 'stats2', 'stats3', 'stats4', 'stats5'
    )

    image = ADComponent(ImagePlugin, "image1:")
    hdf1 = ADComponent(
        MyHDF5Plugin,
        "HDF1:",
        write_path_template=os.path.join(PILATUS_FILES_ROOT, TEST_IMAGE_DIR),
        read_path_template=os.path.join(BLUESKY_FILES_ROOT, TEST_IMAGE_DIR),
    )
    over1 = ADComponent(OverlayPlugin, 'Over1:')
    roi1 = ADComponent(ROIPlugin, 'ROI1:')
    roi2 = ADComponent(ROIPlugin, 'ROI2:')
    roi3 = ADComponent(ROIPlugin, 'ROI3:')
    roi4 = ADComponent(ROIPlugin, 'ROI4:')
    stats1 = ADComponent(StatsPlugin, 'Stats1:')
    stats2 = ADComponent(StatsPlugin, 'Stats2:')
    stats3 = ADComponent(StatsPlugin, 'Stats3:')
    stats4 = ADComponent(StatsPlugin, 'Stats4:')
    stats5 = ADComponent(StatsPlugin, 'Stats5:')

    def default_settings(self):
        # Enter all the important default settings here.
        self.cam.image_mode.put("Single")
        self.cam.num_images.put(1)
        self.cam.acquire_time.put(1)
        self.cam.trigger_mode.put("Internal")
        self.hdf1.create_directory.put(-5)
        self.hdf1.file_write_mode.put("Single")
        self.hdf1.lazy_open.put(1)
        self.hdf1.compression.put("blosc")
        self.hdf1.file_template.put("%s%s_%5.5d.h5")
        self.hdf1.auto_save.put(0)

    # Example of roi config.
    def plot_roi1(self):
        self.stats1.total.kind = "hinted"  # Is this signal correct?
        self.stats2.total.kind = "normal"
        self.stats3.total.kind = "normal"
        self.stats4.total.kind = "normal"

    def plot_roi2(self):
        self.stats1.total.kind = "normal"  # Is this signal correct?
        self.stats2.total.kind = "hinted"
        self.stats3.total.kind = "normal"
        self.stats4.total.kind = "normal"

    def plot_roi3(self):
        self.stats3.total.kind = "hinted"  # Is this signal correct?
        self.stats2.total.kind = "normal"
        self.stats1.total.kind = "normal"
        self.stats4.total.kind = "normal"

    def plot_roi4(self):
        self.stats4.total.kind = "hinted"  # Is this signal correct?
        self.stats2.total.kind = "normal"
        self.stats3.total.kind = "normal"
        self.stats1.total.kind = "normal"

    def plot_all(self):
        for i in range(1, 5):
            getattr(self, f"stats{i}").total.kind = "hinted"

pilatus100k = MyPilatusDetector("s6_pilatus:", name="pilatus100k")
pilatus100k.hdf1.stage_sigs["auto_save"] = 1
pilatus100k.cam.stage_sigs["trigger_mode"] = 0
pilatus100k.plot_roi1()
