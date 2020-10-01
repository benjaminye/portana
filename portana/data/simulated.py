from typing import List, Tuple

from . import generator
from ..abstracts import data
from ..timeseries import simtimeseries


class SimConnection(data.AbstractConnection):
    """Simulated connection to a database
    A concrete implementation of AbstractConnection class


    Methods
    -------
    set_asset_type(asset_type: AssetType)
        Sets the connection to retrieve a security in particular asset class
    get_security(isin: str, date_range: Tuple[str, str])
        Returns a simulated Security by ISIN and date range
    """

    def __init__(self):
        self._asset_type: data.AbstractAssetType = None

    def set_asset_type(self, asset_type: data.AbstractAssetType):
        """Sets the connection to retrieve a security in particular asset class


        Parameters
        -------
        asset_type: AssetType
            An AssetType class which contains methods necessary to
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

    def query(self) -> List[data.AbstractSecurity]:
        pass


class SimEquityAssetType(data.AbstractAssetType):
    """Class to return simulated data for an equity security


    Methods
    -------
    get_description() -> dict
        dict of descriptive fields for an equity security
        Example: {"name": "Apple, Inc", ...}
    get_exposures() -> dict
        dict of exposure fields for an equity security
        Example: {"geography": "Canada", ...}
    get_timeseries() -> TimeSeries
        generates a TimeSeries of equity security's prices and total returns
    """

    def __init__(self):
        self.generator = generator.Generator()
        self.generator.set_max_drift(0.001)
        self.generator.set_max_vol(0.05)
        self.generator.set_max_distribution(0.005)
        self.generator.set_initial_price_range((1, 1000))

    def get_timeseries(
        self, date_range: Tuple[str, str], seed: int
    ) -> data.AbstractTimeSeries:
        """Returns a Timeseries object containing time series data


        Returns
        -------
        TimeSeries
            Pricing and total returns data for an equity security
        """

        self.generator.set_seed(seed)
        self.generator.set_date_range(date_range)

        dates = self.generator.generate_dates()
        prices = self.generator.generate_prices()
        tot_ret_idx = self.generator.generate_tot_ret_idx()

        return simtimeseries.SimTimeSeries(dates, prices, tot_ret_idx)

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
    """Class to return simulated data for an equity fund
    A concrete implementation of AbstractAssetType


    Methods
    -------
    get_description() -> dict
        dict of descriptive fields for an equity fund
        Example: {"fee": "0.015", ...}

    get_exposures() -> dict
        dict of exposure fields for an equity fund
        Example: {"Geography": "United States", ...}

    get_timeseries() -> TimeSeries
        generates a TimeSeries of equity fund's prices and total returns
    """

    def __init__(self):
        self.generator = generator.Generator()
        self.generator.set_max_drift(0.00025)
        self.generator.set_max_vol(0.02)
        self.generator.set_max_distribution(0.002)
        self.generator.set_initial_price_range((50, 100))

    def get_timeseries(
        self, date_range: Tuple[str, str], seed: int
    ) -> data.AbstractTimeSeries:
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

        return simtimeseries.SimTimeSeries(dates, prices, tot_ret_idx)

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


class Security(data.AbstractSecurity):
    """Class containing information pertaining to a security
    A concrete implementation of AbstractSecurity

    Parameters
    -------
    isin: str
        Security's ISIN (unique identifier)
    timeseries: TimeSeries
        Security's time series data
    description: dict
        Security's descriptive data
    exposures: dict
        Security's exposure data


    Attributes
    -------
    isin: str
        Security's ISIN (unique identifier)
    timeseries: TimeSeries
        Security's time series data
    description: dict
        Security's descriptive data
    exposures: dict
        Security's exposure data


    Methods
    -------
    get_isin() -> str
        getter for attribute Security.isin
    get_timeseries() -> TimeSeries
        getter for attribute Security.timeseries
    get_description() -> dict
        getter for attribute Security.description
    get_exposures() -> dict
        getter for attribute Security.exposures
    """

    def __init__(
        self,
        isin: str,
        timeseries: data.AbstractTimeSeries,
        description: dict,
        exposures: dict,
    ):
        self.isin: str = isin
        self.timeseries: data.AbstractTimeSeries = timeseries
        self.description: dict = description
        self.exposures: dict = exposures
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
        """Getter for attribute Security.isin

        Returns
        -------
        str
            Security's ISIN (unique identifier)
        """
        return self.isin

    def get_timeseries(self):
        """Getter for attribute Security.timeseries

        Returns
        -------
        TimeSeries
            Security's time series data
        """
        return self.timeseries

    def get_description(self):
        """Getter for attribute Security.description

        Returns
        -------
        dict
            Security's description fields
        """
        return self.description

    def get_exposures(self):
        """Getter for attribute Security.exposures

        Returns
        -------
        dict
            Security's exposure fields
        """
        return self.exposures


class Equity(Security):
    """Class to represent an equity security
    Child of Security class
    """

    pass


class EquityFund(Security):
    """Class to represent an equity fund
    Child of Security class
    """

    pass
