""" intake functions """
# importing packages
from ctre import *

__all__ = ["Intake"]

INTAKESCALING = 0.50

class Intake:

    __intakeMotor = WPI_VictorSPX(9)

    @classmethod
    def takeIn(cls):
        # taking in the ball at set scaling
        cls.__intakeMotor.set(INTAKESCALING)
        return

    @classmethod
    def eject(cls):
        # ejecting ball at set scaling
        cls.__intakeMotor.set(-INTAKESCALING)
        return
