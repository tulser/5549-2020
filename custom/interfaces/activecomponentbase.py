__all__ = ["ActiveBase"]


class ActiveBase:
    __active = False

    @classmethod
    def startup(cls):
        pass

    @classmethod
    def getActive(cls):
        return cls.__active
