""" shooter functions """
# importing packages
from robot import *
from math import fabs, sqrt, pow
from ctre import *
from wpilib import SpeedControllerGroup
from threading import Thread, RLock

__all__ = ["Shooter"]

WAITCONST = 8
SHOOTERHEIGHT = 0.5461  # ground to shooter


class PIDManager(Thread):

    def __init__(self, ctrlr: [SpeedControllerGroup], setpoint: float = 0, p: float = 0, i: float = 0, d: float = 0,
                 f: float = 0, *args: TalonSRX):
        super().__init__(name="ShooterPID", daemon=True)
        if ctrlr is None:
            raise ValueError
        if not isinstance(ctrlr, SpeedControllerGroup):
            raise TypeError

        if args is None:
            raise ValueError
        for talon in args:
            if not isinstance(talon, TalonSRX):
                raise TypeError

        self.__controller = ctrlr

        self.__src = tuple(args)

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

        self.mutex = RLock()

        return

    def setSetpoint(self, setpoint: float = 0):
        with self.mutex:
            self.__setpoint = setpoint

    def setPIDF(self, P: float = 0, I: float = 0, D: float = 0, F: float = 0):
        with self.mutex:
            self._Pfac = P
            self._Ifac = I
            self._Dfac = D
            self._FFfac = F

    def go(self, threshold: float = 0.1):
        self.__threshold = threshold
        self.active = True
        self.enabled = True
        if not self.is_alive():
            self.start()

    def run(self):
        counter = 0
        while self.active:
            if self.enabled:
                with self.mutex:
                    currval = 0
                    for talon in self.__src:
                        currval += talon.getSelectedSensorVelocity()*10
                    error = self.__setpoint - currval / self.__src.__len__()

                    self.__controller.set(error * self._Pfac + self.__integralsum * self._Ifac + (
                                error - self.__pasterr) * self._Dfac + self._FFfac)

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

    def reset(self):
        with self.mutex:
            self.__integralsum = 0
            self.__pasterr = 0
        return

class Shooter:

    __encoderTop: WPI_TalonSRX = None
    __encoderBot: WPI_TalonSRX = None
    __motorsUp: SpeedControllerGroup = None
    __motorsDown: SpeedControllerGroup = None
    __pidUp: PIDManager = None
    __pidDown: PIDManager = None

    presets = ()  # please fill in

    @classmethod
    def __init__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__encoderTop = WPI_TalonSRX(5)
        cls.__encoderBot = WPI_TalonSRX(7)
        cls.__motorsUp = SpeedControllerGroup(cls.__encoderTop, WPI_VictorSPX(6))
        cls.__motorsDown = SpeedControllerGroup(cls.__encoderBot, WPI_VictorSPX(8))
        cls.__pidUp = PIDManager(cls.__motorsUp, 0, 0.1, 0.005, 0, 0, cls.__encoderTop, cls.__encoderBot)
        cls.__pidDown = PIDManager(cls.__motorsDown, 0, 0.1, 0.005, 0, 0, cls.__encoderTop, cls.__encoderBot)

    @classmethod
    def stopAll(cls):
        cls.__motorsUp.set(0)
        cls.__motorsDown.set(0)

    @classmethod
    def shootBoth(cls, rpm: float):
        cls.shootDifferent(rpm, rpm)

    @classmethod
    def shootDesired(cls, rpm: float, whichmotor: int):  # 0: both, 1: up, 2: down
        if whichmotor == 0:
            cls.shootDifferent(rpm, rpm)
        if whichmotor == 1:
            cls.__pidUp.pause()
            cls.__pidUp.setSetpoint(rpm)
            cls.__pidUp.reset()
            cls.__pidUp.go(0.05)
        if whichmotor == 2:
            cls.__pidDown.pause()
            cls.__pidDown.setSetpoint(rpm)
            cls.__pidUp.reset()
            cls.__pidDown.go(0.05)

    @classmethod
    def shootDifferent(cls, rpmUp: float, rpmDown: float):
        cls.__pidUp.pause()
        cls.__pidDown.pause()
        cls.__pidUp.setSetpoint(rpmUp)
        cls.__pidDown.setSetpoint(rpmDown)
        cls.__pidUp.reset()
        cls.__pidDown.reset()
        cls.__pidUp.go(0.05)
        cls.__pidDown.go(0.05)

    @classmethod
    def shootPreset(cls, setting: int):
        cls.shootDifferent(cls.presets[setting][0], cls.presets[setting][1])

    @classmethod
    def shootAuto(cls, force=False):
        dist = Vision.getTargetDistance()
        if dist < (TARGETHEIGHT-TARGETMARGINS) and not force:
            # Recommended to setup networktables feedback under this conditional.
            return

        cls.__encoderTop.setSelectedSensorPosition(0)
        cls.__encoderBot.setSelectedSensorPosition(0)

        target = sqrt(-9.81 * pow(dist, 2) / (TARGETHEIGHT - SHOOTERHEIGHT + TARGETHEIGHTBIAS - dist)) * 12832.661368899589

        # automatically shoot balls given distance
        cls.shootBoth(target)
        return
