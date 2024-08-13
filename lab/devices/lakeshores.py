"""
Lakeshore temperature controllers
"""

__all__ = ['lakeshore340', ]

from apstools.devices import LakeShore340Device
from apstools.devices.lakeshore_controllers import LS340_LoopBase, LS340_LoopControl
from apstools.devices.positioner_soft_done import timed_pause
from ophyd import FormattedComponent, Component, EpicsSignalRO, EpicsSignal
from ..framework import sd
from ..session_logs import logger
logger.info(__file__)


class MyLoopBase(LS340_LoopBase):
    def _setup_move(self, position):
        super()._setup_move(position)
        self.cb_setpoint(value=0)

    def stop(self, *, success=False):
        """
        Hold the current readback when stop() is called and not :meth:`inposition`.
        """
        if not self.inposition:
            # self.setpoint.put(self.position)
            timed_pause()
            self.cb_readback()  # re-evaluate soft done Signal
            
    def pause(self):
        pass

class MyLoopControl(MyLoopBase):
    readback = Component(EpicsSignalRO, "Control", kind="normal")
    sensor = Component(EpicsSignal, "Ctl_sel", kind="config")


class MyLakeshore(LakeShore340Device):

    control = FormattedComponent(MyLoopControl, "{prefix}", loop_number=1)
    
# Lakeshore 340 - Low temperature
#lakeshore340 = LakeShore340Device(
#    '6idlab:LS340:TC1:', name="lakeshore340", labels=("lakeshore",)
#)

lakeshore340 = MyLakeshore(
    '6idlab:LS340:TC1:', name="lakeshore340", labels=("lakeshore",)
)
lakeshore340.control.readback.kind = "hinted"
sd.baseline.append(lakeshore340)
