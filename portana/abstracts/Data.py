from abc import ABC, abstractmethod
from typing import List, Tuple

from numpy import ndarray
import pandas as pd


class TimeSeries(ABC):
    def __init__(self, dates: ndarray, prices: ndarray, tot_ret_idx: ndarray):
        self.dates = dates
        self.prices = prices
        self.tot_ret_idx = tot_ret_idx
        super().__init__()

    def __repr__(self):
        return str(self.to_df())

    def to_df(self):
        df = pd.DataFrame(
            data={"Price": self.prices, "Total Return Index": self.tot_ret_idx},
            index=self.dates,
            columns=["Price", "Total Return Index"],
        )
        return df

    @abstractmethod
    def __getitem__(self, key):
        pass


class AssetType(ABC):
    @abstractmethod
    def get_description(self) -> dict:
        pass

    @abstractmethod
    def get_exposures(self) -> dict:
        pass

    @abstractmethod
    def get_timeseries(self) -> TimeSeries:
        pass


class Security(ABC):
    def __init__(
        self, isin: str, timeseries: TimeSeries, description: dict, exposures: dict
    ):
        self.isin = isin
        self.timeseries = timeseries
        self.description = description
        self.exposures = exposures
        super().__init__()

    def __repr__(self):
        output = ""
        output += f"ISIN:   {self.isin} \n"
        output += "----------------------------------------- \n"
        for key in self.description:
            output += f"{key.capitalize()}:  {self.description[key]} \n"

        output += "----------------------------------------- \n"
        for key in self.exposures:
            output += f"{key.capitalize()}:  {self.exposures[key]} \n"

        output += "----------------------------------------- \n"
        output += str(self.timeseries)

        return output


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