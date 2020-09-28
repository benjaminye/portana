from abc import ABC, abstractmethod
from typing import Dict, Tuple, Union, Literal

from numpy import ndarray


class Output(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def get_period_stats(
        self,
        freq: Union[
            Literal["D"], Literal["W"], Literal["M"], Literal["Q"], Literal["Y"]
        ],
    ):
        pass

    @abstractmethod
    def get_range_stats(self, date_range: Tuple[str, str]):
        pass


class Analyzer(ABC):
    @abstractmethod
    def add_security(self):
        pass

    @abstractmethod
    def set_index(self):
        pass

    @abstractmethod
    def analyze(self) -> Output:
        pass
