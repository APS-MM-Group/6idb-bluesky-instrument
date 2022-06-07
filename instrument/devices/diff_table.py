'''
diff motors  --diffractormeter table motors
'''

__all__ = ['diff']

from ophyd import Component, MotorBundle, EpicsMotor
from ..framework import sd
from ..session_logs import logger
logger.info(__file__)


class Diff(MotorBundle):
    x = Component(EpicsMotor, 'm30') #diffractormeter table x motor
    y1 = Component(EpicsMotor, 'm25') #diffractormeter table y1 motor
    y2 = Component(EpicsMotor, 'm26') #cdiffractormeter table y2 motor


diff = Diff('6idb1:', name='diff')
sd.baseline.append(diff)