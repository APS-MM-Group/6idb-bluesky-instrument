
'''
cryo motors  --cryostat carrier motors
'''

__all__ = ['cryo']

from ophyd import Component, MotorBundle, EpicsMotor
from ..framework import sd
from ..session_logs import logger
logger.info(__file__)


class Cryo(MotorBundle):
    x = Component(EpicsMotor, 'm34') #cryostat carrier x motor
    y = Component(EpicsMotor, 'm33') #cryostat carrier y motor
    z = Component(EpicsMotor, 'm35') #cryostat carrier z motor


cryo = Cryo('6idb1:', name='cryo')
sd.baseline.append(cryo)
