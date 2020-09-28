from typing import List, Union, Literal, Tuple

import numpy as np

from ..abstracts import Data
from ..abstracts import Analyzer
from ..timeseries.analyzerseries import AnalyzerSeries


class EquityOutput(Analyzer.Output):
    def __init__(self):
        pass

    def __repr__(self):
        pass

    def get_period_stats(
        self,
        freq: Union[
            Literal["D"], Literal["W"], Literal["M"], Literal["Q"], Literal["Y"]
        ],
    ):
        pass

    def get_range_stats(self, date_range: Tuple[str, str]):
        pass


class EquityAnalyzer(Analyzer.Analyzer):
    def __init__(self):
        self.securities: List[Data.Security] = []
        self.index: Data.Security = None
        self._earliest_common_date: np.datetime64 = None

    def __update_earliest_common_date(self) -> None:
        start_dates = []
        for security in self.securities:
            start_date = security.timeseries.dates[0]
            start_dates.append(start_date)

        index_start_date = self.index.timeseries.dates[0]
        start_dates.append(index_start_date)

        self._earliest_common_date = max(start_dates)

    def add_security(self, security: Data.Security) -> None:
        self.securities.append(security)
        self.__update_earliest_common_date()

    def set_index(self, index: Data.Security) -> None:
        self.index = index
        self.__update_earliest_common_date()

    def get_returns(self) -> Data.TimeSeries:
        pass

    def get_return_by_date_range(self) -> Data.TimeSeries:
        pass

    def get_excess_returns(self) -> Data.TimeSeries:
        pass

    def get_excess_return_by_date_range(self) -> Data.TimeSeries:
        pass

    def get_betas(self, freq) -> Data.TimeSeries:
        pass

    def get_betas_by_date_range(self) -> Data.TimeSeries:
        pass

    def get_volatilities(self) -> Data.TimeSeries:
        pass

    def get_volatility_by_date_range(self) -> Data.TimeSeries:
        pass

    def get_sharpes(self) -> Data.TimeSeries:
        pass

    def get_sharpe_by_date_range(self) -> Data.TimeSeries:
        pass

    def analyze(self) -> Analyzer.Output:
        pass
