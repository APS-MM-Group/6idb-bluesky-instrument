
'''
opty2 motors
'''

__all__ = ['opty2']

from ophyd import Component, MotorBundle, EpicsMotor
from ..framework import sd
from ..session_logs import logger
logger.info(__file__)


class Opty2(MotorBundle):
    hu = Component(EpicsMotor, 'm14') #upstream horizonal motor
    hd = Component(EpicsMotor, 'm15') #downstream horizonal motor
    v1 = Component(EpicsMotor, 'm11') #upstream inboard vertical motor
    v2 = Component(EpicsMotor, 'm12') #upstream outboard vertical motor
    v3 = Component(EpicsMotor, 'm13') #downstream vertical motor


opty2 = Opty2('6idb1:', name='opty2')
sd.baseline.append(opty2)