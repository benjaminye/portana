import string
import random
from typing import List, Tuple

import numpy as np

from ..abstracts import Data


class SimConnection(Data.Connection):
    def __init__(self):
        self._description_type = None

    def __get_dates(self, date_range: Tuple[str, str]) -> np.ndarray:
        days_delta = np.datetime64(date_range[1]) - np.datetime64(date_range[0])
        days_delta = days_delta.astype("timedelta64[D]") // np.timedelta64(1, "D")

        dates = np.array(date_range[0], dtype=np.datetime64)
        dates = dates + np.arange(days_delta)

        return dates, days_delta

    def __get_price(self, days_delta: int, seed: int) -> np.ndarray:
        prices = np.random.default_rng(seed).normal(0, 0.1, days_delta) + 1
        prices[0] = 100
        prices = np.cumprod(prices)

        return prices

    def __get_timeseries(
        self, date_range: Tuple[str, str], seed: int
    ) -> Data.TimeSeries:
        dates, days_delta = self.__get_dates(date_range)
        prices = self.__get_price(days_delta, seed)

        return SimTimeSeries(dates, prices)

    def __get_description(self, seed: int) -> Data.Description:
        return self._description_type.get_description(seed)

    def set_description_type(self, desc_type: Data.Description):
        self._description_type = desc_type

    def get_security(self, isin: str, date_range: Tuple[str, str]) -> Data.Security:

        timeseries = self.__get_timeseries(date_range, int(isin))
        description = self.__get_description(int(isin))

        return Equity(isin, timeseries, description)

    def query_single_security(self) -> List[Data.Security]:
        pass

    def query_fund(self) -> List[Data.Security]:
        pass


class SimTimeSeries(Data.TimeSeries):
    def get_date(self, date: str) -> Data.TimeSeries:
        pass

    def get_dates(self, dates: List[str]) -> Data.TimeSeries:
        pass

    def get_date_range(self, date_range: Tuple[str, str]):
        pass


class EquityDescription(Data.Description):
    def __generate_ticker(self, seed: int) -> str:
        random.seed(a=seed)
        length = random.choice(range(1, 5))
        letters = string.ascii_uppercase

        result = ""
        for i in range(length):
            random.seed(a=seed + i)
            result += random.choice(letters)

        return result

    def __generate_sector(self, seed: int) -> str:
        sectors = ["Technology", "Industrials", "Financials"]
        random.seed(a=seed)
        return random.choice(sectors)

    def __generate_geography(self, seed: int) -> str:
        geographies = ["United States", "Canada"]
        random.seed(a=seed)
        return random.choice(geographies)

    def get_description(self, seed: int) -> dict:
        description = {}
        description["ticker"] = self.__generate_ticker(seed)
        description["sector"] = self.__generate_sector(seed)
        description["geography"] = self.__generate_geography(seed)

        return description


class EquityFundDescription(Data.Description):
    pass


class FixedIncomeFundDescription(Data.Description):
    pass


class MixedFundDescription(Data.Description):
    pass


class Equity(Data.Security):
    pass


class FixedIncome(Data.Security):
    pass
