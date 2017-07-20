from enum import Enum

from bac.utils.decorators import advanced_property, decimal, boolean, positive_integer


class ConstraintType(Enum):
    none = 'none'
    h_bonds = 'h-bonds'
    all_bonds = 'all-bonds'
    h_angles = 'h-angles'
    all_angles = 'all-angles'


class ConstraintAlgorithmType(Enum):
    lincs = 'LINCS'
    shake = 'SHAKE'


class ConstraintController:

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.algorithm = kwargs.get('algorithm')
        self.continuation = kwargs.get('continuation')

        self.shake_tolerance = kwargs.get('shake_tolerance')

        self.lincs_order = kwargs.get('lincs_order')
        self.lincs_iterations = kwargs.get('lincs_iterations')
        self.lincs_warn_after_angle = kwargs.get('lincs_warn_after_angle')

        self.morse = kwargs.get('morse')

    @advanced_property(type=ConstraintType, default=ConstraintType.none)
    def type(self): pass

    @advanced_property(type=ConstraintAlgorithmType, default=ConstraintAlgorithmType.lincs)
    def algorithm(self): pass

    @boolean(default=False)
    def continuation(self): pass

    @decimal(default=0.0001)
    def shake_tolerance(self): pass

    @positive_integer(default=4)
    def lincs_order(self): pass

    @positive_integer(default=1)
    def lincs_iterations(self): pass

    @decimal(default=30)
    def lincs_warn_after_angle(self): pass

    @boolean(default=False)
    def morse(self): pass






