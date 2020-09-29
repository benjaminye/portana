from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Literal

from numpy import ndarray
from pandas import DataFrame


class TimeSeries(ABC):
    def __repr__(self):
        return str(self.to_df())

    @abstractmethod
    def __getitem__(self, key):
        # should return another instance of the same object
        pass

    @abstractmethod
    def to_df(self) -> DataFrame:
        pass

    @abstractmethod
    def get_dates(self) -> ndarray:
        pass

    @abstractmethod
    def get_data(self) -> Union[ndarray, Tuple[ndarray]]:
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


class FrequencyConverter(ABC):
    @abstractmethod
    def get_daily(self) -> TimeSeries:
        pass

    @abstractmethod
    def get_weekly(self) -> TimeSeries:
        pass

    @abstractmethod
    def get_monthly(self) -> TimeSeries:
        pass

    @abstractmethod
    def get_quarterly(self) -> TimeSeries:
        pass

    @abstractmethod
    def get_yearly(self) -> TimeSeries:
        pass

    @abstractmethod
    def get_freq(
        self,
        freq: Union[
            Literal["D"], Literal["W"], Literal["M"], Literal["Q"], Literal["Y"]
        ],
    ) -> TimeSeries:
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

    def get_isin(self):
        return self.isin

    def get_timeseries(self):
        return self.timeseries

    def get_description(self):
        return self.description

    def get_exposures(self):
        return self.exposures


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


class Query(ABC):
    pass