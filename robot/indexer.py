""" indexer functions """
# importing packages
from custom import SpeedControllerGroup_M
from ctre import *

__all__ = ["Indexer"]

class Indexer:

    __indexer = SpeedControllerGroup_M(WPI_VictorSPX(10), WPI_VictorSPX(11), WPI_VictorSPX(12), WPI_VictorSPX(13), WPI_VictorSPX(14))

    @classmethod
    def forward(cls):
        cls.__indexer.set(1.0)
        return

    @classmethod
    def stop(cls):
        cls.__indexer.stopMotor()
        return

    @classmethod
    def reverse(cls):
        cls.__indexer.set(-1)
        return
