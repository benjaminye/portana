from abc import ABC, abstractmethod
from typing import Tuple, Union

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
