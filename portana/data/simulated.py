from typing import List, Tuple, Literal, Dict, Union

import pandas as pd

from . import generator
from ..abstracts import data
from ..timeseries.securitytimeseries import SecurityTimeSeries
from .security import Equity, EquityFund, Security


class SimConnection(data.AbstractConnection):
    """Simulated connection to a database.
    A concrete implementation of AbstractConnection class.
    """

    def __init__(self):
        self._asset_type: data.AbstractAssetType = None

    def set_asset_type(self, asset_type: data.AbstractAssetType):
        """Sets the connection to retrieve a security in particular asset class


        Parameters
        -------
        asset_type: AbstractAssetType
            AssetType class which contains methods necessary to
            retrieve simulated data unique to each asset class
        """
        self._asset_type = asset_type

    def get_security(
        self, isin: str, date_range: Tuple[str, str]
    ) -> data.AbstractSecurity:
        """Returns a simulated Security by ISIN and date range


        Parameters
        -------
        isin: str
        date_range: Tuple[str, str]

        Returns
        -------
        Security
            A Security object containing all data relavent to requested security
        """
        timeseries = self._asset_type.get_timeseries(date_range, int(isin))
        description = self._asset_type.get_description(int(isin))
        exposures = self._asset_type.get_exposures(int(isin))

        # ToDo: Try to find a good pattern to replace the following...
        if self._asset_type.__class__ == SimEquityAssetType:
            return Equity(isin, timeseries, description, exposures)
        elif self._asset_type.__class__ == SimEquityFundAssetType:
            return EquityFund(isin, timeseries, description, exposures)


class SimQuery(data.AbstractQuery):
    """Class for sending queries to a simulated database


    Note
    -------
    Currently, the simulated database is consisted of 5000 rows of simulated securities.
    The equity database has these fields "isin", "name", "ticker",
    "sector", "geography", "5y_sharpe".

    The equity funds database has "isin", "name", "fee",
    "geography", "strategy", "risk", "5y_sharpe".

    The database is stored as a csv files under portana/data/simulated_db.
    The query is implemented through pandas.DataFrame's query method.


    Parameters
    -------
    asset_type: str
        Either "equity" or "equityfunds", this determines which database to find data from
    fields: dict
        A dictionary containing fields to query. Example: {"geography": "Canada"}
    sort_by: str
        Field by which to sort the result, default None
    limit: int
        Number of results to return, default None (all results)
    offset: int
        The offset of the results (e.g. offset of 1 will return results from the second row),
        default None (no offset)
    """

    def __init__(
        self,
        asset_type: str,
        fields: dict,
        sort_by: str = None,
        limit: int = None,
        offset: int = 0,
    ):
        self.asset_type = asset_type
        self.fields = fields
        self.sort_by = sort_by
        self.limit = limit
        self.offset = offset

    def _get_sim_equity(self) -> pd.DataFrame:
        df = pd.read_csv("./portana/data/simulated_db/equities.csv", index_col=0)

        return df

    def _get_sim_equity_fund(self) -> pd.DataFrame:
        df = pd.read_csv("./portana/data/simulated_db/equity_funds.csv", index_col=0)

        return df

    def build_query(self):
        """Generate query string to send to database server

        Returns
        -------
        str
            Query string to send to the server
        """
        query_str = ""

        for key, item in self.fields.items():
            query_str += f"{key} == '{item}' and "

        return query_str[:-5]

    def send_query(self) -> Dict[str, Dict[str, Union[str, float]]]:
        """Sends query and returns data

        Returns
        -------
        dict
            Result of the query

        Example
        -------
        >>> q = SimQuery("equity", {"geography": "Canada"}, "5y_sharpe", 2, 0)
        >>> q.send_query()
        {'16366': {'name': 'Simulated Security 16366',
        'ticker': 'W',
        'sector': 'Industrials',
        'geography': 'Canada',
        '5y_sharpe': 221.8231716},
        '19527': {'name': 'Simulated Security 19527',
        'ticker': 'FP',
        'sector': 'Industrials',
        'geography': 'Canada',
        '5y_sharpe': 170.7695025}}
        """
        if self.asset_type.lower() == "equity":
            db = self._get_sim_equity()

        if self.asset_type.lower() == "equityfund":
            db = self._get_sim_equity_fund()

        query_str = self.build_query()

        result = db.query(query_str)

        if self.sort_by:
            result = result.sort_values(self.sort_by, ascending=False)

        if self.limit:
            result = result[self.offset : self.offset + self.limit]

        result_dict = result.to_dict("index")
        result_dict = {str(key): value for key, value in result_dict.items()}

        return result_dict


class SimEquityAssetType(data.AbstractAssetType):
    """Class to return simulated data for an equity security.
    A concrete implementation of AbstractAssetType.
    """

    def __init__(self):
        self.generator = generator.Generator()
        self.generator.set_max_drift(0.001)
        self.generator.set_max_vol(0.05)
        self.generator.set_max_distribution(0.005)
        self.generator.set_initial_price_range((1, 1000))

    def get_timeseries(
        self, date_range: Tuple[str, str], seed: int
    ) -> SecurityTimeSeries:
        """Returns a Timeseries object containing time series data


        Returns
        -------
        SimTimeSeries
            Pricing and total returns data for an equity security
        """

        self.generator.set_seed(seed)
        self.generator.set_date_range(date_range)

        dates = self.generator.generate_dates()
        prices = self.generator.generate_prices()
        tot_ret_idx = self.generator.generate_tot_ret_idx()

        return SecurityTimeSeries(dates, prices, tot_ret_idx)

    def get_description(self, seed: int) -> dict:
        """Get dict of descriptive fields for an equity security


        Returns
        -------
        dict
            dict containing each descriptive field for an equity security


        Example
        -------
        >>> AssetType.get_description()
        {"name": "Apple, Inc.", ...}
        """
        self.generator.set_seed(seed)

        description = {}
        description["name"] = self.generator.generate_name()
        description["ticker"] = self.generator.generate_ticker()

        return description

    def get_exposures(self, seed: int) -> dict:
        """Get dict of exposure-related fields for an equity security


        Returns
        -------
        dict
            dict containing each exposure field for an equity security


        Example
        -------
        >>> AssetType.get_exposures()
        {"geography": "Canada", ...}
        """
        self.generator.set_seed(seed)

        exposures = {}
        exposures["sector"] = self.generator.generate_sector()
        exposures["geography"] = self.generator.generate_geography()

        return exposures


class SimEquityFundAssetType(data.AbstractAssetType):
    """Class to return simulated data for an equity fund.
    A concrete implementation of AbstractAssetType."""

    def __init__(self):
        self.generator = generator.Generator()
        self.generator.set_max_drift(0.00025)
        self.generator.set_max_vol(0.02)
        self.generator.set_max_distribution(0.002)
        self.generator.set_initial_price_range((50, 100))

    def get_timeseries(
        self, date_range: Tuple[str, str], seed: int
    ) -> SecurityTimeSeries:
        """Returns a Timeseries object containing time series data


        Returns
        -------
        TimeSeries
            Pricing and total returns data for an equity fund
        """
        self.generator.set_seed(seed)
        self.generator.set_date_range(date_range)

        dates = self.generator.generate_dates()
        prices = self.generator.generate_prices()
        tot_ret_idx = self.generator.generate_tot_ret_idx()

        return SecurityTimeSeries(dates, prices, tot_ret_idx)

    def get_description(self, seed: int) -> dict:
        """Get dict of descriptive fields for an equity security


        Returns
        -------
        dict
            dict containing each descriptive field for an equity security


        Example
        -------
        >>> AssetType.get_description()
        {"fee": "0.015", ...}
        """
        self.generator.set_seed(seed)

        description = {}
        description["name"] = self.generator.generate_name()
        description["fee"] = self.generator.generate_fee()

        return description

    def get_exposures(self, seed: int) -> dict:
        """Get dict of exposure-related fields for an equity fund


        Returns
        -------
        dict
            dict containing each exposure field for an equity fund


        Example
        -------
        >>> AssetType.get_exposures()
        {"geography": "Canada", ...}
        """
        self.generator.set_seed(seed)

        exposures = {}
        exposures["geography"] = self.generator.generate_geography()
        exposures["strategy"] = self.generator.generate_strategy()
        exposures["risk"] = self.generator.generate_risk()

        return exposures
