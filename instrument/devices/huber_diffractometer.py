__all__ = "fourc psic".split()

from ..session_logs import logger

logger.info(__file__)

import gi
gi.require_version('Hkl', '5.0')

from hkl.geometries import E4CV
from ophyd import EpicsMotor, PseudoSingle
from ophyd import Component as Cpt

class FourCircle(E4CV):
    """
    Our 4-circle.  Eulerian.  Vertical scattering orientation.
    """
    # the reciprocal axes are called "pseudo" in hklpy
    h = Cpt(PseudoSingle, '')
    k = Cpt(PseudoSingle, '')
    l = Cpt(PseudoSingle, '')

    # the motor axes are called "real" in hklpy
    omega = Cpt(EpicsMotor, "6idb1:m17")
    chi = Cpt(EpicsMotor, "6idb1:m19")
    phi = Cpt(EpicsMotor, "6idb1:m20")
    tth = Cpt(EpicsMotor, "6idb1:m18")


fourc = FourCircle("", name="fourc")


from hkl.geometries import E6C

class SixCircle(E6C):
    """
#    Our 6-circle.  Eulerian.  
    """
    # the reciprocal axes are called "pseudo" in hklpy
    h = Cpt(PseudoSingle, '')
    k = Cpt(PseudoSingle, '', kind="hinted")
    l = Cpt(PseudoSingle, '', kind="hinted")

    # the motor axes are called "real" in hklpy
    mu = Cpt(EpicsMotor, "6idb1:m28")
    omega = Cpt(EpicsMotor, "6idb1:m17")
    chi = Cpt(EpicsMotor, "6idb1:m19")
    phi = Cpt(EpicsMotor, "6idb1:m20")
    gamma = Cpt(EpicsMotor, "6idb1:m29")
    delta = Cpt(EpicsMotor, "6idb1:m18")


psic = SixCircle("", name="psic")

from hkl.user import select_diffractometer
select_diffractometer(psic)

# Make sure all motors are not hinted!
# for item in "h k l".split():
#     getattr(fourc, item).readback.kind = "normal"
    # getattr(psic, item).readback.kind = "normal"

# for item in "omega chi phi tth".split():
#     getattr(fourc, item).user_readback.kind = "normal"

# for item in "omega mu chi phi gamma delta".split():
    # getattr(psic, item).user_readback.kind = "normal"
