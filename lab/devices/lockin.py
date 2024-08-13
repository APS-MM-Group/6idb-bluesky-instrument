"""
Lock in
"""

__all__ = ['lockin810', 'lockin830']

from .srs_lockins import SRS810Device, SRS830Device
from ..framework import sd
from ..session_logs import logger
logger.info(__file__)


lockin810 = SRS810Device('6idlab:SRS810:2:', name='lockin810', labels=('detectors',))
sd.baseline.append(lockin810)

lockin830 = SRS830Device('6idlab:SR830:1:', name='lockin830', labels=('detectors',))
sd.baseline.append(lockin830)
