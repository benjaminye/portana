from abc import ABC, abstractmethod
from typing import Tuple, Union, Literal

from numpy import ndarray
from pandas import DataFrame


class AbstractTimeSeries(ABC):
    """Abstract class for time series representation used in this package


    Note
    -------
    This class supports indexing by date. User can pass in date(s) in following ways:


        TimeSeries[str] -> AbstractTimeSeries:
            Returns TimeSeries object containing data on that date
        TimeSeries[List[str]] -> AbstractTimeSeries:
            Returns TimeSeries object containing data on dates in list
        TimeSeries[begin:end:step] -> AbstractTimeSeries:
            Returns TimeSeries object containing data on and between
            begin and end dates, with prescribed step size
    """

    def __repr__(self):
        return str(self.to_df())

    @abstractmethod
    def __getitem__(self, key):
        """Method to support indexing"""
        pass

    @abstractmethod
    def to_df(self) -> DataFrame:
        """Returns a pandas DataFrame object representing data contained in this object


        Returns
        -------
        pandas.DataFrame
            DataFrame representation of this object
        """
        pass

    @abstractmethod
    def get_dates(self) -> ndarray:
        """Returns a numpy array of dates


        Returns
        -------
        numpy.ndarray
            Numpy array of dates contained in this object
        """
        pass

    @abstractmethod
    def get_data(self) -> Union[ndarray, Tuple[ndarray]]:
        """Returns a numpy array(s) containing data


        Returns
        -------
        numpy.ndarray
            Numpy array of data contained in this object (excluding dates)
        """
        pass


class AbstractSecurityTimeSeries(AbstractTimeSeries):
    @abstractmethod
    def get_month_ends(self):
        """Returns timeseries containing every month-end within current Timeseries

        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every month-end
        """
        pass

    @abstractmethod
    def get_quarter_ends(self):
        """Returns timeseries containing every quarter-end within current Timeseries


        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every quater-end
        """
        pass

    @abstractmethod
    def get_year_ends(self):
        """Returns timeseries containing every year-end within current Timeseries


        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every year-end
        """
        pass

    @abstractmethod
    def get_period_ends(self, freq: Literal["M", "Q", "Y"]):
        """Returns timeseries containing every period-end within current Timeseries


        Parameters
        -------
        freq: Literal["M", "Q", "Y"]
            "M" for month-end, "Q" for quarter-end, "Y" for year-end

        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every year-end
        """
        pass

    @abstractmethod
    def get_month_starts(self):
        """Returns timeseries containing every month-start within current Timeseries

        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every month-start
        """
        pass

    @abstractmethod
    def get_quarter_starts(self):
        """Returns timeseries containing every quarter-start within current Timeseries


        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every quater-start
        """
        pass

    @abstractmethod
    def get_year_starts(self):
        """Returns timeseries containing every year-start within current Timeseries


        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every year-start
        """
        pass

    @abstractmethod
    def get_period_starts(self, freq: Literal["M", "Q", "Y"]):
        """Returns timeseries containing every period-starts within current Timeseries


        Parameters
        -------
        freq: Literal["M", "Q", "Y"]
            "M" for month-start, "Q" for quarter-start, "Y" for year-start

        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every period-starts
        """
        pass

    @abstractmethod
    def split_month(self) -> list:
        """Split series into each month


        Returns
        -------
        List[AbstractTimeSeries]
            List of TimeSeries object, with each element representing one month
        """
        pass

    @abstractmethod
    def split_quarter(self) -> list:
        """Split series into each month


        Returns
        -------
        List[AbstractTimeSeries]
            List of TimeSeries object, with each element representing one quarter
        """
        pass

    @abstractmethod
    def split_year(self) -> list:
        """Split series into each month


        Returns
        -------
        List[AbstractTimeSeries]
            List of TimeSeries object, with each element representing one year
        """
        pass
