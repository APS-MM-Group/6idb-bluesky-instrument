"""
SRS 810 and 830 Lock-ins
"""

from ophyd import Component, Device, EpicsSignal, EpicsSignalRO


class SRS830Device(Device):

    # Time constant
    time_multiplier = Component(EpicsSignal, 'TC1', kind='omitted', string=True)
    time_decade = Component(EpicsSignal, 'TC2', kind='omitted', string=True)
    time_unit = Component(EpicsSignal, 'TC3', kind='omitted', string=True)
    time_filter_readback = Component(EpicsSignalRO, 'LPFilter_rbv', kind='config')
    time_filter_setpoint = Component(EpicsSignal, 'LPFilter', kind='config', string=True)

    time_constant = Component(EpicsSignalRO, 'TC.SVAL', kind='config')

    # Gain
    gain_multiplier = Component(EpicsSignal, 'Sens1', kind='omitted', string=True)
    gain_decade = Component(EpicsSignal, 'Sens2', kind='omitted', string=True)
    gain_unit = Component(EpicsSignal, 'Sens3', kind='omitted', string=True)
    gain = Component(EpicsSignalRO, 'Sens.SVAL', kind='config')

    # Reserve
    reserve_readback = Component(EpicsSignalRO, 'Reserve_rbv', kind='config')
    reserve_setpoint = Component(EpicsSignal, 'ResvCh', kind='config', string=True)

    # Notch filter
    notch_readback = Component(EpicsSignalRO, 'NotchFilter_rbv', kind='config')
    notch_setpoint = Component(EpicsSignal, 'NotchFilter', kind='config', string=True)
    
    # AUX output voltage
    aux_out1 = Component(EpicsSignal, 'AuxOutCh1_rbv', write_pv='AuxOutCh1', kind='config')
    aux_out2 = Component(EpicsSignal, 'AuxOutCh2_rbv', write_pv='AuxOutCh2', kind='config')
    aux_out3 = Component(EpicsSignal, 'AuxOutCh3_rbv', write_pv='AuxOutCh3', kind='config')
    aux_out4 = Component(EpicsSignal, 'AuxOutCh4_rbv', write_pv='AuxOutCh4', kind='config')

    # Reference
    frequency = Component(EpicsSignal, 'Freq.VAL', write_pv='SetFreq', kind='config')
    phase = Component(EpicsSignal, 'Phas.VAL', write_pv='SetPhas', kind='config')
    amplitude = Component(EpicsSignal, 'Ampl.VAL', write_pv='SetAmpl', kind='config')

    # Outputs
    x = Component(EpicsSignalRO, 'X.VAL', kind='hinted')
    y = Component(EpicsSignalRO, 'Y.VAL', kind='normal')
    r = Component(EpicsSignalRO, 'R.VAL', kind='normal')
    q = Component(EpicsSignalRO, 'TH.VAL', kind='normal')
    adc1 = Component(EpicsSignalRO, 'ADC1.VAL', kind='normal')
    adc2 = Component(EpicsSignalRO, 'ADC2.VAL', kind='normal')
    adc3 = Component(EpicsSignalRO, 'ADC3.VAL', kind='normal')
    adc4 = Component(EpicsSignalRO, 'ADC4.VAL', kind='normal')

    # Auto buttons
    auto_phase = Component(EpicsSignal, 'AutoPhas.PROC', kind='omitted')
    auto_gain = Component(EpicsSignal, 'AutoGain.PROC', kind='omitted')
    auto_reserve = Component(EpicsSignal, 'AutoResv.PROC', kind='omitted')

    # Scan
    read_button =  Component(EpicsSignal, 'read.PROC', kind='omitted')
    read_scan = Component(EpicsSignal, 'read.SCAN', kind='config', string=True)
    read_parameters = Component(EpicsSignal, 'SlowRead', kind='config', string=True)


class SRS810Device(Device):

    # Time constant
    time_multiplier = Component(EpicsSignal, 'TC1', kind='omitted', string=True)
    time_decade = Component(EpicsSignal, 'TC2', kind='omitted', string=True)
    time_unit = Component(EpicsSignal, 'TC3', kind='omitted', string=True)
    time_filter = Component(EpicsSignal, 'FiltCh', kind='config', string=True)
    time_constant = Component(EpicsSignalRO, 'TC.SVAL', kind='config')
    time_read = Component(EpicsSignal, 'ReadTC.PROC', kind='omitted')

    # Gain
    gain_multiplier = Component(EpicsSignal, 'Sens1', kind='omitted', string=True)
    gain_decade = Component(EpicsSignal, 'Sens2', kind='omitted', string=True)
    gain_unit = Component(EpicsSignal, 'Sens3', kind='omitted', string=True)
    gain = Component(EpicsSignalRO, 'Sens.SVAL', kind='config')
    gain_read = Component(EpicsSignal, 'ReadSens.PROC', kind='omitted')

    # Reserve
    reserve = Component(EpicsSignal, 'ResvCh', kind='config', string=True)

    # Reference
    frequency = Component(EpicsSignalRO, 'Freq.VAL', kind='config')
    phase = Component(EpicsSignal, 'Phas.VAL', write_pv='SetPhas', kind='config')

    # outputs
    x = Component(EpicsSignalRO, 'X.VAL', kind='hinted')
    y = Component(EpicsSignalRO, 'Y.VAL', kind='normal')
    r = Component(EpicsSignalRO, 'R.VAL', kind='normal')
    q = Component(EpicsSignalRO, 'Th.VAL', kind='normal')
    read_button =  Component(EpicsSignal, 'ReadX.PROC', kind='omitted')
    read_scan = Component(EpicsSignal, 'ReadX.SCAN', kind='config', string=True)

    # Auto buttons
    auto_phase = Component(EpicsSignal, 'AutoPhas.PROC', kind='omitted')
    auto_gain = Component(EpicsSignal, 'AutoGain.PROC', kind='omitted')
    auto_reserve = Component(EpicsSignal, 'AutoResv.PROC', kind='omitted')