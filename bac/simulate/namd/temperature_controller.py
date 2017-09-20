from enum import Enum

from bac.utils.decorators import *


class TemperatureController:

    def __init__(self, **kwargs):
        self.langevin: LangevinDynamics = None
        self.coupling: TemperatureCoupling = None
        self.rescale: VelocityRescaling = None
        self.reassign: VelocityReassignment = None
        self.lowe_andersen: LoweAndersenDynamics = None


class LangevinDynamics:
    def __init__(self, **kwargs):
        self.temperature = kwargs.get('temperature')
        self.damping = kwargs.get('damping')
        self.applies_to_hydrogen = kwargs.get('hydrogen')
        self.file = kwargs.get('file')
        self.column = kwargs.get('column')

    @boolean(default=True)
    def applies_to_hydrogen(self): pass

    @positive_decimal
    def temperature(self): pass

    @positive_decimal
    def damping(self): pass

    @file(default=lambda self: self.run.coordinates)
    def file(self): pass

    @column
    def column(self): pass


class TemperatureCoupling:
    def __init__(self, **kwargs):
        self.temperature = kwargs.get('temperature')
        self.file = kwargs.get('file')
        self.column = kwargs.get('column')

    @positive_decimal
    def temperature(self): pass

    @file
    def file(self): pass

    @column
    def column(self): pass


class VelocityRescaling:
    def __init__(self, **kwargs):
        self.temperature = kwargs.get('temperature')
        self.frequency = kwargs.get('frequency')

    @positive_decimal
    def temperature(self): pass

    @positive_integer
    def frequency(self): pass

    def __bool__(self):
        return self.frequency is not None


class VelocityReassignment:
    def __init__(self, **kwargs):
        self.temperature = kwargs.get('temperature')
        self.frequency = kwargs.get('frequency')
        self.increment = kwargs.get('increment')
        self.hold_at = kwargs.get('hold_at')

    @positive_decimal(default=lambda self: self.simulation.temperature)
    def temperature(self): pass

    @positive_integer
    def frequency(self): pass

    @decimal(default=0)
    def increment(self): pass

    @positive_decimal
    def hold_at(self): pass

    def __bool__(self):
        return self.frequency is not None


class LoweAndersenDynamics:
    def __init__(self, **kwargs):
        self.temperature = kwargs.get('temperature')
        self.cutoff = kwargs.get('cutoff')
        self.rate = kwargs.get('rate')

    @positive_decimal
    def temperature(self): pass

    @positive_decimal(default=2.7)
    def cutoff(self): pass

    @positive_decimal(default=50)
    def rate(self): pass
