from abc import ABC, abstractmethod
from numpy import ndarray


class TimeSeries(ABC):
    def __init__(self, dates:ndarray, prices:ndarray):
        self.dates = dates
        self.prices = prices
        super().__init__()


class Descriptives(ABC):
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        super().__init__()


class Connection(ABC):
    @abstractmethod
    def get_prices(self, start_date:str, end_date:str) -> TimeSeries:
        pass

    @abstractmethod
    def get_desc(self) -> Descriptives:
        pass

