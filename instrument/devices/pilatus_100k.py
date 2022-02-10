from ophyd import (
    ADComponent,
    ImagePlugin,
    PilatusDetector,
    SingleTrigger
)
from ophyd.areadetector.plugins import (
    HDF5Plugin_V34 as HDF5Plugin,
    OverlayPlugin_V34 as OverlayPlugin,
    ROIPlugin_V34 as ROIPlugin,
    StatsPlugin_V34 as StatsPlugin
)
from ophyd.areadetector.filestore_mixins import (
    FileStoreHDF5SingleIterativeWrite
)
from os.path import join

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
        write_path_template=join(PILATUS_FILES_ROOT, TEST_IMAGE_DIR),
        read_path_template=join(BLUESKY_FILES_ROOT, TEST_IMAGE_DIR),
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
        """
        Set the default Pilatus configuration.
        """
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

    def plot_roi(self, values=[1, 2, 3, 4, 5]):
        """
        Select ROI stats to be plotted during scan.

        Parameters
        ----------
        values: int or iterable, optional
            ROI index or list of ROI indexes to be plotted. Defaults to plot
            all ROIs.
        """
        if isinstance(values, (int, float)):
            values = [int(values)]

        for name in self.component_names:
            if "stats" in name:
                kind = "hinted" if int(name[-1]) in values else "normal"
                attr = getattr(self, name)
                attr.total.kind = kind


pilatus100k = MyPilatusDetector("s6_pilatus:", name="pilatus100k")
pilatus100k.hdf1.stage_sigs["auto_save"] = 1
pilatus100k.plot_roi()
pilatus100k.default_settings()
