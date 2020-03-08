from wpilib import SpeedControllerGroup
from ctre import TalonSRX
from math import fabs
from threading import Thread, RLock
import numpy

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

        if len(args) is 1:
            self.__srcact = self.__single
        else:
            self.__srcact = self.__multi

        self.__src = args

        self.__srclen = len(args)

        self.__calcact = self.__stdcalc

        self._Pfac = p
        self._Ifac = i
        self._Dfac = d
        self._FFfac = f

        self.__integralsum = 0
        self.__pasterr = 0
        self.__setpoint = setpoint
        self.__threshold = 0.1
        self.__intcounter = 1
        self.__preverr = numpy.zeros(10)
        self.enabled = False
        self.active = False
        self.__achieved = False
        self.__noContinue = False

        self.waitThresh = 20

        self.mutex = RLock()

        return

    def setSetpoint(self, setpoint: float = 0):
        with self.mutex:
            self.__setpoint = setpoint
        return

    def setMode(self, mode: int):
        if mode is 0:
            with self.mutex:
                self.__calcact = self.__stdcalc
        else:
            with self.mutex:
                self.__calcact = self.__rangedcalc

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

    @property
    def achieved(self):
        return self.__achieved

    def __single(self):
        return self.__src[0].getSelectedSensorVelocity() * 10

    def __multi(self):
        currval = 0
        for talon in self.__src:
            currval += talon.getSelectedSensorVelocity() * 10
        return self.__setpoint - currval / self.__srclen

    def __stdcalc(self, err):
        self.__controller.set(err * self._Pfac + self.__integralsum * self._Ifac + (
                err - self.__preverr[0]) * self._Dfac + self._FFfac)

        self.__integralsum += err
        self.__preverr[0] = err

    def __rangedcalc(self, err):
        self.__intcounter = (self.__intcounter + 1) % self.__preverr.size

        self.__controller.set(err * self._Pfac + self.__integralsum * self._Ifac + (
                err - self.__preverr[self.__intcounter]) * self._Dfac + self._FFfac)

        self.__integralsum += err
        self.__integralsum -= self.__preverr[(self.__intcounter + 1) % self.__preverr.size]
        self.__preverr[self.__intcounter] = err

    def go(self, threshold: float = 0.1):
        self.__threshold = threshold
        self.active = True
        self.enabled = True
        self.reset()
        if not self.is_alive():
            self.start()
        return

    def run(self):
        counter = 0
        while self.active:
            if self.enabled:
                with self.mutex:
                    error = self.__srcact()
                    self.__calcact(error)

                    condit = fabs(error) > self.__threshold
                    counter = (counter + 1) if not condit else 0
                if not condit and counter > self.waitThresh:
                    self.__achieved = True
                    if self.__noContinue:
                        break
        return

    def pause(self):
        self.enabled = False
        return

    def stop(self):
        self.active = False
        self.enabled = False
        self.reset()
        return

    def reset(self):
        with self.mutex:
            self.__intcounter = 0
            for val in range(0, self.__preverr.size):
                self.__preverr[val] = 0
            self.__integralsum = 0
            self.__pasterr = 0
            self.__achieved = False
        return