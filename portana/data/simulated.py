import string
import random
from typing import List, Tuple, Union

import numpy as np

from . import generator
from ..abstracts import Data
from ..timeseries import simtimeseries


class SimConnection(Data.Connection):
    def __init__(self):
        self._asset_type: Data.AssetType = None

    def set_asset_type(self, asset_type: Data.AssetType):
        self._asset_type = asset_type

    def get_security(self, isin: str, date_range: Tuple[str, str]) -> Data.Security:
        timeseries = self._asset_type.get_timeseries(date_range, int(isin))
        description = self._asset_type.get_description(int(isin))
        exposures = self._asset_type.get_exposures(int(isin))

        # ToDo: Try to find a good pattern to replace the following...
        if self._asset_type.__class__ == EquityAssetType:
            return Equity(isin, timeseries, description, exposures)
        elif self._asset_type.__class__ == EquityFundAssetType:
            return EquityFund(isin, timeseries, description, exposures)

    def query_single_security(self) -> List[Data.Security]:
        pass

    def query_fund(self) -> List[Data.Security]:
        pass


class SimTimeSeries(Data.TimeSeries):
    def __make_self(
        self, dates: np.ndarray, prices: np.ndarray, tot_ret_idx: np.ndarray
    ):
        return SimTimeSeries(dates, prices, tot_ret_idx)

    def __getitem__(self, subscript: Union[str, list, slice]):
        if isinstance(subscript, slice):
            match = (self.dates >= np.datetime64(subscript.start)) & (
                self.dates < np.datetime64(subscript.stop)
            )
            return self.__make_self(
                self.dates[match][:: subscript.step],
                self.prices[match][:: subscript.step],
                self.tot_ret_idx[match][:: subscript.step],
            )

        elif isinstance(subscript, str):
            match = self.dates == np.datetime64(subscript)

        elif isinstance(subscript, list):
            items = []
            for item in subscript:
                items.append(np.datetime64(item))

            match = np.isin(self.dates, items)

        return self.__make_self(
            self.dates[match], self.prices[match], self.tot_ret_idx[match]
        )


class EquityAssetType(Data.AssetType):
    def __init__(self):
        self.generator = generator.Generator()
        self.generator.set_max_drift(0.001)
        self.generator.set_max_vol(0.05)
        self.generator.set_max_distribution(0.005)
        self.generator.set_initial_price_range((1, 1000))

    def get_timeseries(self, date_range: Tuple[str, str], seed: int) -> Data.TimeSeries:
        self.generator.set_seed(seed)
        self.generator.set_date_range(date_range)

        dates = self.generator.generate_dates()
        prices = self.generator.generate_prices()
        tot_ret_idx = self.generator.generate_tot_ret_idx()

        return simtimeseries.SimTimeSeries(dates, prices, tot_ret_idx)

    def get_description(self, seed: int) -> dict:
        self.generator.set_seed(seed)

        description = {}
        description["name"] = self.generator.generate_name()
        description["ticker"] = self.generator.generate_ticker()

        return description

    def get_exposures(self, seed: int) -> dict:
        self.generator.set_seed(seed)

        exposures = {}
        exposures["sector"] = self.generator.generate_sector()
        exposures["geography"] = self.generator.generate_geography()

        return exposures


class EquityFundAssetType(Data.AssetType):
    def __init__(self):
        self.generator = generator.Generator()
        self.generator.set_max_drift(0.00025)
        self.generator.set_max_vol(0.02)
        self.generator.set_max_distribution(0.002)
        self.generator.set_initial_price_range((50, 100))

    def get_timeseries(self, date_range: Tuple[str, str], seed: int) -> Data.TimeSeries:
        self.generator.set_seed(seed)
        self.generator.set_date_range(date_range)

        dates = self.generator.generate_dates()
        prices = self.generator.generate_prices()
        tot_ret_idx = self.generator.generate_tot_ret_idx()

        return simtimeseries.SimTimeSeries(dates, prices, tot_ret_idx)

    def get_description(self, seed: int) -> dict:
        self.generator.set_seed(seed)

        description = {}
        description["name"] = self.generator.generate_name()
        description["fee"] = self.generator.generate_fee()

        return description

    def get_exposures(self, seed: int) -> dict:
        self.generator.set_seed(seed)

        exposures = {}
        exposures["geography"] = self.generator.generate_geography()
        exposures["strategy"] = self.generator.generate_strategy()
        exposures["risk"] = self.generator.generate_risk()

        return exposures


class Equity(Data.Security):
    pass


class EquityFund(Data.Security):
    pass