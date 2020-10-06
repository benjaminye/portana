from abc import ABC, abstractmethod

from .data import AbstractSecurity

"""
Abstract Class for portfolio
"""


class AbstractPortfolio(ABC):
    """Class to create a portfolio of securities, track exposure, and generate
    a timeseries of portfolio NAVs

    ToDo
    -------
    - Get rebal trades
    - make rebal more flexible (instead of every period,
      user can set it to monthly, quarterly... etc)
    """

    @abstractmethod
    def add_security(self, security: AbstractSecurity, weight: float) -> None:
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
        pass

    @abstractmethod
    def set_starting_nav(self, starting_nav: float) -> None:
        """Set the starting NAV of the portfolio


        Parameters
        -------
        starting_nav: float
            Starting NAV of the portfolio

        Returns
        -------
        None
        """
        pass

    @abstractmethod
    def set_rebal(self, is_enabled: bool) -> None:
        """Set the rebal policy of portfolio


        Parameters
        -------
        is_enabled: bool
            True to rebal portfolio every period, False to turn off rebal


        Returns
        -------
        None
        """
        pass

    @abstractmethod
    def securitize(self) -> AbstractSecurity:
        """Get simulated historical NAV of the portfolio,
        and return them in an AbstractSecurity object.

        Returns
        -------
        AbstractSecurity
            Security object representing the portfolio
        """
        pass

    @abstractmethod
    def get_exposures(self) -> dict:
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
        pass

    @abstractmethod
    def get_exposures_detailed(self) -> dict:
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
        pass

    @abstractmethod
    def get_fees(self) -> dict:
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
        pass
