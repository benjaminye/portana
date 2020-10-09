from typing import List, Dict, Tuple, Literal

import numpy as np

from ..abstracts.portfolio import AbstractPortfolio
from ..abstracts.data import AbstractSecurity
from ..timeseries.securitytimeseries import SecurityTimeSeries
from ..data.security import PortfolioSecurity
from ..analyzer.equity_analyzer import EquityAnalyzer


class Portfolio(AbstractPortfolio):
    """Class to create a portfolio of securities, track exposure, and generate
    a timeseries of portfolio NAVs


    Attributes
    -------
    # Need to write this


    ToDo
    -------
    - Get rebal trades
    - make rebal more flexible (instead of every period,
      user can set it to monthly, quarterly... etc)
    """

    def __init__(self):
        self.name: str = "Custom Portfolio"
        self.securities: List[AbstractSecurity] = []
        self.weights: list = []
        self.starting_nav = 0
        self.rebal: bool = True
        self.rebal_freq: str = "data"

        self._earliest_common_date: np.datetime64 = None
        self._latest_common_date: np.datetime64 = None
        self._date_series: np.ndarray = None
        self._weights_timeseries: np.ndarray = None

    def __update_earliest_common_date(self) -> None:
        start_dates = []
        for security in self.securities:
            start_date = security.get_timeseries().get_dates()[0]
            start_dates.append(start_date)

        self._earliest_common_date = max(start_dates)

    def __update_latest_common_date(self) -> None:
        end_dates = []
        for security in self.securities:
            start_date = security.get_timeseries().get_dates()[-1]
            end_dates.append(start_date)

        self._latest_common_date = min(end_dates)

    def __build_dates(self) -> None:
        start = self._earliest_common_date
        end = self._latest_common_date

        dates = self.securities[0].get_timeseries()[start:end].get_dates()

        self._date_series = dates

    def __get_individual_price_returns(self) -> np.ndarray:
        analyzer = EquityAnalyzer()
        for security in self.securities:
            analyzer.add_security(security)

        rets, _ = analyzer.get_returns("px")

        return rets.get_data()

    def __get_individual_total_returns(self) -> np.ndarray:
        analyzer = EquityAnalyzer()
        for security in self.securities:
            analyzer.add_security(security)

        rets, _ = analyzer.get_returns("tr")

        return rets.get_data()

    def __calculate_weights_timeseries(self):
        if self.rebal:
            if self.rebal_freq == "data":
                weights = np.array(self.weights, dtype=np.float64)
                weights = np.expand_dims(weights, 0)
                weights = np.repeat(weights, len(self._date_series) - 1, axis=0)
            else:
                rebal_dates = (
                    self.securities[0]
                    .timeseries.get_period_ends(self.rebal_freq)
                    .get_dates()
                )

                rebal_dates_indices = np.isin(self._date_series, rebal_dates)
                rebal_dates_indices = list(
                    np.argwhere(rebal_dates_indices == True).flatten()
                )

                # Handle edge case where first rebalance day is the first day in data
                try:
                    rebal_dates_indices.remove(0)
                except ValueError:
                    pass
                rebal_dates_indices.insert(0, 0)

                # Handle edge case where last rebalance day is the last day in data
                if rebal_dates_indices[-1] == len(self._date_series) - 1:
                    rebal_dates_indices[-1] += 1
                    rebal_end = True
                else:
                    rebal_dates_indices.append(len(self._date_series))
                    rebal_end = False

                weights = np.zeros((0, len(self.securities)), dtype=np.float64)

                for idx, i in enumerate(rebal_dates_indices[:-1]):
                    start_index = i
                    end_index = rebal_dates_indices[idx + 1]
                    length = end_index - start_index

                    period_weights = np.zeros(
                        (length, len(self.securities)), dtype=np.float64
                    )
                    period_weights[0] = self.weights

                    rets = self.__get_individual_price_returns()[
                        start_index : end_index - 1
                    ]
                    rets = rets + 1

                    period_weights[1:] = rets

                    period_weights = np.cumprod(period_weights, axis=0)
                    period_weights = period_weights / np.expand_dims(
                        period_weights.sum(axis=1), axis=1
                    )
                    weights = np.vstack((weights, period_weights))

                if rebal_end:
                    weights[-1] = self.weights

                weights = np.delete(weights, 0, 0)

        else:
            weights = np.zeros(
                (len(self._date_series), len(self.securities)), dtype=np.float64
            )
            weights[0] = self.weights

            rets = self.__get_individual_price_returns()
            rets = rets + 1

            weights[1:] = rets

            weights = np.cumprod(weights, axis=0)
            weights = weights / np.expand_dims(weights.sum(axis=1), axis=1)
            weights = np.delete(weights, 0, 0)

        self._weights_timeseries = weights

    def __get_port_price_returns(self) -> np.ndarray:
        rets = self.__get_individual_price_returns()
        weights = self._weights_timeseries.transpose()

        return np.dot(rets, weights)[:, 0]

    def __get_port_total_returns(self) -> np.ndarray:
        rets = self.__get_individual_total_returns()
        weights = self._weights_timeseries.transpose()

        return np.dot(rets, weights)[:, 0]

    def add_security(self, security: AbstractSecurity, weight: float):
        """Add a security to portfolio


        Parameters
        -------
        security: AbstractSecurity
            Security to be added
        weight: float
            The weight of the security in the portfolio


        Returns
        -------
        None
        """
        self.securities.append(security)
        self.weights.append(weight)

        self.__update_earliest_common_date()
        self.__update_latest_common_date()
        self.__build_dates()
        self.__calculate_weights_timeseries()

    def set_starting_nav(self, starting_nav: float):
        """Set the starting NAV of the portfolio


        Parameters
        -------
        starting_nav: float
            Starting NAV of the portfolio

        Returns
        -------
        None
        """
        self.starting_nav = starting_nav

    def set_rebal(
        self, is_enabled: bool, freq: Literal["data", "M", "Q", "Y"] = "data"
    ):
        """Set the rebal policy of portfolio


        Parameters
        -------
        is_enabled: bool
            True to rebal portfolio every period, False to turn off rebal
        freq: bool
            Rebal frequency. "data": same as data frequency; "M": Monthly; "Q": Quarterly;
            "Y": Yearly

        Returns
        -------
        None
        """
        self.rebal = is_enabled
        self.rebal_freq = freq
        self.__calculate_weights_timeseries()

    def securitize(self) -> PortfolioSecurity:
        """Get simulated historical NAV of the portfolio,
        and return them in an AbstractSecurity object.

        Returns
        -------
        AbstractSecurity
            Security object representing the portfolio
        """
        prices = np.zeros(len(self._date_series))
        tot_ret_idx = np.zeros(len(self._date_series))

        px_ret, tot_ret = (
            self.__get_port_price_returns(),
            self.__get_port_total_returns(),
        )
        px_ret, tot_ret = px_ret + 1, tot_ret + 1

        prices[0], tot_ret_idx[0] = self.starting_nav, self.starting_nav
        prices[1:], tot_ret_idx[1:] = px_ret, tot_ret

        prices, tot_ret_idx = (
            np.cumprod(prices, axis=0),
            np.cumprod(tot_ret_idx, axis=0),
        )

        timeseries = SecurityTimeSeries(self._date_series, prices, tot_ret_idx)

        return PortfolioSecurity(
            self.name, timeseries, self.get_fees(), self.get_exposures()
        )

    def get_exposures(self) -> Dict[str, Dict[str, float]]:
        """Get categorized exposure of the entire porfolio


        Returns
        -------
        dict
            Dictionary containing portfolio's exposure


        Example
        -------
        >>> Portfolio.get_exposures()
        {
            "geography": {
                "United States": 0.50,
                "Canada" : 0.50
            },
            "sector": {
                ...
            },
            ...
        }
        """
        exposures_table = {}

        for idx, security in enumerate(self.securities):
            exposures = security.get_exposures()
            for exposure in exposures:
                exposures_table.setdefault(exposure, {})
                exposures_table[exposure].setdefault(exposures[exposure], 0)
                exposures_table[exposure][exposures[exposure]] += self.weights[idx]

        return exposures_table

    def get_exposures_detailed(self) -> Dict[str, Dict[str, Tuple[str, float]]]:
        """Get categorized exposure of the entire porfolio,
        broken down by security


        Returns
        -------
        dict
            Dictionary containing portfolio's exposure


        Example
        -------
        >>> Portfolio.get_exposures_detailed()
        {
            "geography": {
                "Canada": [
                    ("Security 1", 0.15),
                    ("Security 2", 0.20)
                ]
                "United States": [
                    "Security 3": 0.65
                ]
            },
            ...
        }
        """
        exposures_table = {}

        for idx, security in enumerate(self.securities):
            exposures = security.get_exposures()
            for exposure in exposures:
                exposures_table.setdefault(exposure, {})
                exposures_table[exposure].setdefault(exposures[exposure], [])
                exposures_table[exposure][exposures[exposure]].append(
                    (security.get_isin(), self.weights[idx])
                )

        return exposures_table

    def get_fees(self) -> Dict[str, float]:
        """Get total fees incurred by portfolio


        Returns
        -------
        dict
            Dictionary containing portfolio's fee


        Example
        -------
        >>> Portfolio.get_fees()
        {
            "fees": 0.005
        }
        """
        port_fee = 0.0
        for idx, security in enumerate(self.securities):
            fee = security.get_description().get("fee")
            if fee is not None:
                port_fee += fee * self.weights[idx]

        return {"fees": port_fee}
