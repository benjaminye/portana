from ..abstracts import data
from ..timeseries.securitytimeseries import SecurityTimeSeries


class Security(data.AbstractSecurity):
    """Class containing information pertaining to a security.
    A concrete implementation of AbstractSecurity.

    Parameters
    -------
    isin: str
        Security's ISIN (unique identifier)
    timeseries: SimTimeSeries
        Security's time series data
    description: dict
        Security's descriptive data
    exposures: dict
        Security's exposure data


    Attributes
    -------
    isin: str
        Security's ISIN (unique identifier)
    timeseries: SimTimeSeries
        Security's time series data
    description: dict
        Security's descriptive data
    exposures: dict
        Security's exposure data
    """

    def __init__(
        self,
        isin: str,
        timeseries: SecurityTimeSeries,
        description: dict,
        exposures: dict,
    ):
        self.isin: str = isin
        self.timeseries: SecurityTimeSeries = timeseries
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
        SimTimeSeries
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
    """Class to represent an equity security.
    Child of Security class.
    """

    pass


class EquityFund(Security):
    """Class to represent an equity fund.
    Child of Security class.
    """

    pass


class PortfolioSecurity(Security):
    """Class to represent a portfolio.
    Child of Security class.
    """

    pass
