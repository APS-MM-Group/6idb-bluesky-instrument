
'''
analy motors  --polarization analyzer motors
'''

__all__ = ['analy']

from ophyd import Component, MotorBundle, EpicsMotor
from ..framework import sd
from ..session_logs import logger
logger.info(__file__)


class Analy(MotorBundle):
    th = Component(EpicsMotor, 'm21') #polarization analyzer theta motor
    tth = Component(EpicsMotor, 'm22') #polarization analyzer 2theta motor
    chi = Component(EpicsMotor, 'm23') #polarization analyzer chi motor


analy = Analy('6idb1:', name='analy')
sd.baseline.append(analy)