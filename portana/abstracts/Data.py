from abc import ABC, abstractmethod
from typing import List, Tuple

from numpy import ndarray
import pandas as pd


class TimeSeries(ABC):
    def __init__(self, dates: ndarray, prices: ndarray):
        self.dates = dates
        self.prices = prices
        super().__init__()

    def __repr__(self):
        df = pd.DataFrame(data=self.prices, index=self.dates, columns=["Price"])
        return df.__str__()

    def __str__(self):
        df = pd.DataFrame(data=self.prices, index=self.dates, columns=["Price"])
        return df.__str__()

    @abstractmethod
    def get_date(self, date: str):
        pass

    @abstractmethod
    def get_dates(self, dates: List[str]):
        pass

    @abstractmethod
    def get_date_range(self, date_range: Tuple[str, str]):
        pass


class Description(ABC):
    @abstractmethod
    def get_description(self) -> dict:
        pass


class Security(ABC):
    def __init__(self, isin: str, timeseries: TimeSeries, description: dict):
        self.isin = isin
        self.timeseries = timeseries
        self.description = description
        super().__init__()

    def __repr__(self):
        output = ""
        output += f"ISIN:   {self.isin} \n"
        output += "----------------------------------------- \n"
        for key in self.description:
            output += f"{key.capitalize()}:  {self.description[key]} \n"

        output += "----------------------------------------- \n"
        output += str(self.timeseries)

        return output

        # print(self.timeseries)


class Connection(ABC):
    @abstractmethod
    def get_security(self, isin: str, date_range: Tuple[str, str]) -> Security:
        pass

    @abstractmethod
    def query_single_security(self) -> List[Security]:
        pass

    @abstractmethod
    def query_fund(self) -> List[Security]:
        pass