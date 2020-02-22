""" shooter functions """
# importing packages
from robot import Vision
from robot.shared import *
from math import fabs, sqrt, pow
from ctre import *
from wpilib import SpeedControllerGroup
from threading import Thread #,RLock

__all__ = ["Shooter"]

WAITCONST = 8


class Shooter:

    __encoderTop: WPI_TalonSRX = None
    __encoderBot: WPI_TalonSRX = None
    __motors: SpeedControllerGroup = None

    @classmethod
    def __init__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__encoderTop = WPI_TalonSRX(5)
        cls.__encoderBot = WPI_TalonSRX(7)
        cls.__motors = SpeedControllerGroup(cls.__encoderTop, WPI_VictorSPX(6), cls.__encoderBot, WPI_VictorSPX(8))

    @classmethod
    def shootAuto(cls, force=False):
        dist = Vision.getDistance()
        if dist < (TARGETHEIGHT-TARGETMARGINS) and not force:
            # Recommended to setup networktables feedback under this conditional.
            return

        cls.__encoderTop.setSelectedSensorPosition(0)
        cls.__encoderBot.setSelectedSensorPosition(0)

        # automatically shoot balls given distance
        pid = PIDManager(cls.__motors,
                         sqrt(-9.81 * pow(dist, 2) / (TARGETHEIGHT - SHOOTERHEIGHT + TARGETHEIGHTBIAS - dist)) * 1283.2661368899589,
                         0.01, 0.01, 0, 0, cls.__encoderTop, cls.__encoderBot)
        pid.go(0.05)
        return


class PIDManager(Thread):

    def __init__(self, ctrlr: SpeedControllerGroup, setpoint: float = 0, p: float = 0, i: float = 0, d: float = 0, f: float = 0, *args: TalonSRX):
        super().__init__(name="ShooterPID", daemon=True)
        if ctrlr is None:
            raise ValueError
        if not isinstance(ctrlr, SpeedControllerGroup):
            raise TypeError

        for talon in args:
            if not isinstance(talon, TalonSRX):
                raise TypeError

        self.__src = tuple(args)

        self.__controller = ctrlr

        self._Pfac = p
        self._Ifac = i
        self._Dfac = d
        self._FFfac = f

        self.__integralsum = 0
        self.__pasterr = 0
        self.__setpoint = setpoint
        self.__threshold = 0.1
        self.enabled = False
        self.active = False

        # self.mutex = threading.RLock()

        return

    def go(self, threshold: float = 0.1):
        self.__threshold = threshold
        self.active = True
        self.enabled = True
        if not self.isAlive():
            self.start()

    def run(self):
        counter = 0
        while self.active:
            if self.enabled:
                currval = 0
                for talon in self.__src:
                    currval += talon.getSelectedSensorVelocity()
                error = self.__setpoint - currval/self.__src.__len__()

                self.__controller.set(error * self._Pfac + self.__integralsum * self._Ifac + (error - self.__pasterr) * self._Dfac + self._FFfac)

                condit = fabs(error) > self.__threshold
                counter = (counter + 1) if not condit else 0
                if not condit or counter > WAITCONST: break

                self.__integralsum += error
                self.__pasterr = error
        return

    def pause(self):
        self.enabled = False

    def stop(self):
        self.active = False
        self.reset()

    def reset(self, newsetpoint: float = None):
        if newsetpoint is None:
            self.__setpoint = 0

        self.__integralsum = 0
        self.__pasterr = 0
        return
