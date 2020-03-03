from wpilib import SpeedControllerGroup
from ctre import TalonSRX
from math import fabs
from threading import Thread, RLock

__all__ = ["PIDManager"]


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

        self.waitThresh = 20

        self.mutex = RLock()

        return

    def setSetpoint(self, setpoint: float = 0):
        with self.mutex:
            self.__setpoint = setpoint
        return

    def setPIDF(self, P: float = 0, I: float = 0, D: float = 0, F: float = 0):
        with self.mutex:
            self._Pfac = P
            self._Ifac = I
            self._Dfac = D
            self._FFfac = F
        return

    def setTolerance(self, threshold: int):
        self.waitThresh = threshold
        return

    def go(self, threshold: float = 0.1):
        self.__threshold = threshold
        self.active = True
        self.enabled = True
        if not self.is_alive():
            self.start()
        return

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
                    if not condit or counter > self.waitThresh: break

                    self.__integralsum += error
                    self.__pasterr = error
        return

    def pause(self):
        self.enabled = False
        return

    def stop(self):
        self.active = False
        self.reset()
        return

    def reset(self):
        with self.mutex:
            self.__integralsum = 0
            self.__pasterr = 0
        return