from typing import List, Union, Literal, Tuple, Dict

import numpy as np

from ..abstracts import Data
from ..abstracts import Analyzer
from ..timeseries.analyzerseries import AnalyzerSeries


class EquityOutput(Analyzer.Output):
    """
    Wrapper for outputs from Equity Analyzer
    """

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
        self.comp_index: Data.Security = None
        self._earliest_common_date: np.datetime64 = None
        self._latest_common_date: np.datetime64 = None
        self._date_series: np.ndarray = None
        self._price_series: np.ndarray = None
        self._tot_ret_idx_series: np.ndarray = None
        self._col_names: List[str] = []

    def __update_earliest_common_date(self) -> None:
        start_dates = []
        for security in self.securities:
            start_date = security.get_timeseries().get_dates()[0]
            start_dates.append(start_date)

        index_start_date = self.comp_index.get_timeseries().get_dates()[0]
        start_dates.append(index_start_date)

        self._earliest_common_date = max(start_dates)

    def __update_latest_common_date(self) -> None:
        end_dates = []
        for security in self.securities:
            start_date = security.get_timeseries().get_dates()[-1]
            end_dates.append(start_date)

        index_end_date = self.comp_index.get_timeseries().get_dates()[-1]
        end_dates.append(index_end_date)

        self._latest_common_date = min(end_dates)

    def __build_dates(self) -> None:
        start = self._earliest_common_date
        end = self._latest_common_date

        dates = self.securities[0].get_timeseries()[start:end].get_dates()

        self._date_series = dates

    def __build_series(self) -> None:
        start = self._earliest_common_date
        end = self._latest_common_date

        dates = self._date_series

        prices = np.ndarray((len(dates), len(self.securities)))
        tot_ret_idx = np.ndarray((len(dates), len(self.securities)))

        for index, security in enumerate(self.securities):
            prices[:, index], tot_ret_idx[:, index] = security.get_timeseries()[
                start:end
            ].get_data()

        self._price_series = AnalyzerSeries(dates, prices, self._col_names)
        self._tot_ret_idx_series = AnalyzerSeries(dates, tot_ret_idx, self._col_names)

    def __build_col_names(self) -> None:
        col_names = []
        for security in self.securities:
            col_names.append(security.isin)

        self._col_names = col_names

    def __get_series(
        self, mode: Union[Literal["px"], Literal["tr"]]
    ) -> Tuple[np.ndarray, np.ndarray]:
        start = self._earliest_common_date
        end = self._latest_common_date

        if mode == "px":
            series = self._price_series.get_data().copy()
            index, _ = self.comp_index.get_timeseries()[start:end].get_data()
            index = index.copy()

        elif mode == "tr":
            series = self._tot_ret_idx_series.get_data().copy()
            _, index = self.comp_index.get_timeseries()[start:end].get_data()
            index = index.copy()

        return series, index

    def add_security(self, security: Data.Security) -> None:
        # Todo: Check frequency... if added security timeseries if of lower freq, convert all to lower freq
        self.securities.append(security)

        if self.comp_index is None:
            self.set_comp_index(security)

        # Todo: Add an update routine function to wrap all these
        self.__build_col_names()
        self.__update_earliest_common_date()
        self.__update_latest_common_date()
        self.__build_dates()
        self.__build_series()

    def set_comp_index(self, comp_index: Data.Security) -> None:
        # Todo: Check frequency... if added security timeseries if of lower freq, convert all to lower freq
        self.comp_index = comp_index
        self.__update_earliest_common_date()
        self.__update_latest_common_date()
        self.__build_dates()
        self.__build_series()

    def get_rebased_index(
        self, mode: Union[Literal["px"], Literal["tr"]], initial_val: float
    ) -> Tuple[Data.TimeSeries, Data.TimeSeries]:

        series, index = self.__get_series(mode)
        series[0], index[0] = float(initial_val), float(initial_val)
        series_ret, index_ret = self.get_returns(mode)
        series[1:], index[1:] = (
            series_ret.get_data() + 1,
            index_ret.get_data() + 1,
        )
        series, index = np.cumprod(series, axis=0), np.cumprod(index, axis=0)

        series_securities = AnalyzerSeries(self._date_series, series, self._col_names)
        series_index = AnalyzerSeries(self._date_series, index, [self.comp_index.isin])

        return series_securities, series_index

    def get_returns(
        self, mode: Union[Literal["px"], Literal["tr"]]
    ) -> Tuple[Data.TimeSeries, Data.TimeSeries]:

        dates = self._date_series[1:]

        series, index = self.__get_series(mode)

        results_securities = np.diff(series, axis=0) / series[:-1]
        results_index = np.diff(index, axis=0) / index[:-1]

        series_securities = AnalyzerSeries(dates, results_securities, self._col_names)
        series_index = AnalyzerSeries(dates, results_index, [self.comp_index.isin])

        return series_securities, series_index

    def get_betas(
        self, mode: Union[Literal["px"], Literal["tr"]]
    ) -> Tuple[Data.TimeSeries, Data.TimeSeries]:
        dates = self._date_series[[-1]]

        securities_ret, index_ret = self.get_returns(mode)
        securities_ret, index_ret = securities_ret.get_data(), index_ret.get_data()

        betas = (
            np.cov(securities_ret, y=index_ret, rowvar=False)
            / np.var(index_ret, ddof=1)
        )[-1]

        results_securities = np.expand_dims(betas[0:-1], axis=0)
        results_index = betas[[-1]]

        series_securities = AnalyzerSeries(dates, results_securities, self._col_names)
        series_index = AnalyzerSeries(dates, results_index, [self.comp_index.isin])

        return series_securities, series_index

    def get_volatilities(
        self, mode: Union[Literal["px"], Literal["tr"]], adj_factor: int
    ) -> Tuple[Data.TimeSeries, Data.TimeSeries]:
        dates = self._date_series[[-1]]

        securities_ret, index_ret = self.get_returns(mode)
        securities_ret, index_ret = securities_ret.get_data(), index_ret.get_data()

        securities_var, index_var = (
            np.var(securities_ret, axis=0, keepdims=True, ddof=1),
            np.var(index_ret, axis=0, keepdims=True, ddof=1),
        )

        securities_vol, index_vol = (
            np.sqrt(securities_var) * np.sqrt(adj_factor),
            np.sqrt(index_var) * np.sqrt(adj_factor),
        )

        series_securities = AnalyzerSeries(dates, securities_vol, self._col_names)
        series_index = AnalyzerSeries(dates, index_vol, [self.comp_index.isin])

        return series_securities, series_index

    def get_sharpes(
        self, mode: Union[Literal["px"], Literal["tr"]], adj_factor: int, rfr: float
    ) -> Tuple[Data.TimeSeries, Data.TimeSeries]:
        dates = self._date_series[[-1]]

        securities_ret, index_ret = self.get_returns(mode)
        securities_ret, index_ret = (
            securities_ret.get_data() + 1,
            index_ret.get_data() + 1,
        )

        securities_cumu_ret, index_cumu_ret = (
            np.cumprod(securities_ret, axis=0) - 1,
            np.cumprod(index_ret, axis=0) - 1,
        )

        securities_per_ret, index_per_ret = (
            securities_cumu_ret[[-1]],
            index_cumu_ret[[-1]],
        )

        securities_vol, index_vol = self.get_volatilities(mode, adj_factor)
        securities_vol, index_vol = securities_vol.get_data(), index_vol.get_data()

        securities_sharpe, index_sharpe = (
            (securities_per_ret - rfr) / securities_vol,
            (index_per_ret - rfr) / index_vol,
        )

        series_securities = AnalyzerSeries(dates, securities_sharpe, self._col_names)
        series_index = AnalyzerSeries(dates, index_sharpe, [self.comp_index.isin])

        return series_securities, series_index

    def analyze(self) -> Analyzer.Output:
        pass
