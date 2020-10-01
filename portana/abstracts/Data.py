from abc import ABC, abstractmethod
from typing import List, Tuple

from .timeseries import AbstractTimeSeries


""" Defines abstract classes used for data interfaces and representation
"""


class AbstractAssetType(ABC):
    """Abstract class to return different data depending on each asset class


    Methods
    -------
    get_description() -> dict
        dict of descriptive fields for specific asset class
        Example: {"name": "Apple, Inc"}
    get_exposures() -> dict
        dict of exposure fields for specific asset class
        Example: {"currency": "USD"}
    get_timeseries() -> TimeSeries
        generates a TimeSeries of security's prices within that asset class
    """

    @abstractmethod
    def get_timeseries(self) -> AbstractTimeSeries:
        """Returns a Timeseries object containing time series data


        Returns
        -------
        TimeSeries
            Pricing data for a security under this asset class
        """
        pass

    @abstractmethod
    def get_description(self) -> dict:
        """Get dict of descriptive fields for specific asset class


        Returns
        -------
        dict
            dict containing each descriptive field for prescribed asset class


        Example
        -------
        >>> AssetType.get_description()
        {"name": "Apple, Inc."}
        """
        pass

    @abstractmethod
    def get_exposures(self) -> dict:
        """Get dict of exposure-related fields for specific asset class


        Returns
        -------
        dict
            dict containing each exposure field for prescribed asset class


        Example
        -------
        >>> AssetType.get_exposures()
        {"currency": "USD"}
        """
        pass


# Not Implemented
# ------------------------------------------
# class FrequencyConverter(ABC):
#     @abstractmethod
#     def get_daily(self) -> TimeSeries:
#         pass

#     @abstractmethod
#     def get_weekly(self) -> TimeSeries:
#         pass

#     @abstractmethod
#     def get_monthly(self) -> TimeSeries:
#         pass

#     @abstractmethod
#     def get_quarterly(self) -> TimeSeries:
#         pass

#     @abstractmethod
#     def get_yearly(self) -> TimeSeries:
#         pass

#     @abstractmethod
#     def get_freq(
#         self,
#         freq: Union[
#             Literal["D"], Literal["W"], Literal["M"], Literal["Q"], Literal["Y"]
#         ],
#     ) -> TimeSeries:
#         pass


class AbstractSecurity(ABC):
    """Class containing information pertaining to a security


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

    @abstractmethod
    def get_isin(self):
        """Getter for attribute Security.isin

        Returns
        -------
        str
            Security's ISIN (unique identifier)
        """
        pass

    @abstractmethod
    def get_timeseries(self):
        """Getter for attribute Security.timeseries

        Returns
        -------
        TimeSeries
            Security's time series data
        """
        pass

    @abstractmethod
    def get_description(self):
        """Getter for attribute Security.description

        Returns
        -------
        dict
            Security's description fields
        """
        pass

    @abstractmethod
    def get_exposures(self):
        """Getter for attribute Security.exposures

        Returns
        -------
        dict
            Security's exposure fields
        """
        pass


class AbstractConnection(ABC):
    """Abstract class for database connections

    ...

    Methods
    -------
    get_security(isin:str, date_range: Tuple[str, str]) -> Security
        Retrieve security and data from database by isin and date_range
    """

    @abstractmethod
    def get_security(self, isin: str, date_range: Tuple[str, str]) -> AbstractSecurity:
        """Retrieve security and data from database by isin and date_range

        Parameters
        -------
        isin: str
            Security's ISIN (unique identifier)
        date_range: Tuple[str, str]
            Date range by which to retrive data from
            Example: ["2001-01-01", "2004-01-01"]

        Returns
        -------
        Security
            Class containing information of the security
        """
        pass

    # Not Implemented
    @abstractmethod
    def query(self) -> List[AbstractSecurity]:
        pass


# Not Implemented
# ----------------------
# class Query(ABC):
# pass
