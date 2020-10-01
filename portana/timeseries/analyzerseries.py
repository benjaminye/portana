from typing import Union, List

import numpy as np
import pandas as pd

from ..abstracts import timeseries


class AnalyzerSeries(timeseries.AbstractTimeSeries):
    """Class for time series representation for ouputs from Anlyzer classes
    A concrete implementation of AbstractTimeSeries

    Methods
    -------
    to_df() -> pandas.DataFrame
        Returns a pandas DataFrame object representing outputs
    get_dates() -> numpy.ndarray
        Returns a numpy array of dates
    get_data() -> Union[numpy.ndarray, Tuple[numpy.ndarray]]
        Returns a numpy array of outputs (excluding dates)

    Notes
    -------
    This class supports indexing by date.

    User can pass in date(s) in following ways:
    TimeSeries[str] -> TimeSeries:
        returns TimeSeries object containing data on that date
    TimeSeries[List[str]] -> TimeSeries:
        returns TimeSeries object containing data on dates in list
    TimeSeries[begin:end:step] -> TimeSeries:
        returns TimeSeries object containing data on and between
        begin and end dates, with prescribed step size
    """

    def __init__(self, dates: np.ndarray, results: np.ndarray, col_names: List[str]):
        self.dates = dates
        self.results = results
        self.col_names = col_names

    def __make_self(self, dates: np.ndarray, results: np.ndarray, col_names: List[str]):
        return AnalyzerSeries(dates, results, col_names)

    def __getitem__(self, subscript: Union[str, list, slice]):
        if isinstance(subscript, slice):
            match = (self.dates >= np.datetime64(subscript.start)) & (
                self.dates <= np.datetime64(subscript.stop)
            )
            return self.__make_self(
                self.dates[match][:: subscript.step],
                self.results[match][:: subscript.step],
                self.col_names,
            )

        elif isinstance(subscript, str):
            match = self.dates == np.datetime64(subscript)

        elif isinstance(subscript, list):
            items = []
            for item in subscript:
                items.append(np.datetime64(item))

            match = np.isin(self.dates, items)

        return self.__make_self(self.dates[match], self.results[match], self.col_names)

    def to_df(self) -> pd.DataFrame:
        """Returns a pandas DataFrame object representing data contained in this object


        Returns
        -------
        pandas.DataFrame
            DataFrame representation of this object
        """
        df = pd.DataFrame(data=self.results, index=self.dates, columns=self.col_names)
        return df

    def get_dates(self) -> np.ndarray:
        """Returns a numpy array of dates


        Returns
        -------
        numpy.ndarray
            Numpy array of dates contained in this object
        """
        return self.dates

    def get_data(self) -> np.ndarray:
        """Returns a numpy array(s) containing data


        Returns
        -------
        numpy.ndarray
            Numpy array of data contained in this object (excluding dates)
        """
        return self.results
