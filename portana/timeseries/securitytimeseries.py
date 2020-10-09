from typing import Union, Tuple, Literal
import calendar

import numpy as np
import pandas as pd

from ..abstracts import timeseries


class SecurityTimeSeries(timeseries.AbstractSecurityTimeSeries):
    """Class for representation of securities time series

    Parameters
    -------
    dates: numpy.ndarray
        Numpy array containing dates,
        must be the same size as other parameters passed in
    prices: numpy.ndarray
        Numpy array containing prices,
        must be the same size as other parameters passed in
    tot_ret_idx: np.ndarray
        Numpy array containing total return index,
        must be the same size as other parameters passed in

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

    ToDo
    -------
    All the get_begins, get_ends, split_periods need to be refactored to improve code reuse!
    Right now they repeat themselves a lot, and I'm not in the mood to refactor today!
    """

    def __init__(self, dates: np.ndarray, prices: np.ndarray, tot_ret_idx: np.ndarray):
        self.dates = dates
        self.prices = prices
        self.tot_ret_idx = tot_ret_idx

    def __make_self(
        self, dates: np.ndarray, prices: np.ndarray, tot_ret_idx: np.ndarray
    ):
        return SecurityTimeSeries(dates, prices, tot_ret_idx)

    def __on_or_just_before(self, date: str) -> np.datetime64:
        date = np.datetime64(date)

        while date not in self.dates:
            if date < self.dates[0]:
                return None

            date -= 1

        return date

    def __on_or_just_after(self, date: str) -> np.datetime64:
        date = np.datetime64(date)

        while date not in self.dates:
            if date < self.dates[0]:
                return None

            date += 1

        return date

    def __getitem__(self, subscript: Union[str, list, slice]):
        if isinstance(subscript, slice):
            match = (self.dates >= np.datetime64(subscript.start)) & (
                self.dates <= np.datetime64(subscript.stop)
            )
            return self.__make_self(
                self.dates[match][:: subscript.step],
                self.prices[match][:: subscript.step],
                self.tot_ret_idx[match][:: subscript.step],
            )

        elif isinstance(subscript, str):
            match = self.dates == np.datetime64(subscript)

        elif isinstance(subscript, list):
            items = []
            for item in subscript:
                items.append(np.datetime64(item))

            match = np.isin(self.dates, items)

        return self.__make_self(
            self.dates[match], self.prices[match], self.tot_ret_idx[match]
        )

    def to_df(self) -> pd.DataFrame:
        """Returns a pandas DataFrame object representing data contained in this object


        Returns
        -------
        pandas.DataFrame
            DataFrame representation of this object
        """
        df = pd.DataFrame(
            data={"Price": self.prices, "Total Return Index": self.tot_ret_idx},
            index=self.dates,
        )
        return df

    def get_dates(self) -> np.ndarray:
        """Returns a numpy array of dates


        Returns
        -------
        numpy.ndarray
            Numpy array of dates contained in this object
        """
        return self.dates

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Returns a numpy array(s) containing data


        Returns
        -------
        numpy.ndarray
            Numpy array of data contained in this object (excluding dates)
        """
        return self.prices, self.tot_ret_idx

    def get_month_ends(self):
        """Returns timeseries containing every month-end within current Timeseries

        Returns
        -------
        SecurityTimeSeries
            SecurityTimeSeries object containing every month-end
        """
        start_year, start_month, _ = str(self.dates[0]).split("-")
        end_year, end_month, _ = str(self.dates[-1]).split("-")

        start_year, start_month = int(start_year), int(start_month)
        end_year, end_month = int(end_year), int(end_month)

        month_ends = []

        # get month-ends in start_year
        for month in range(start_month, 12 + 1):
            month_end_day = calendar.monthrange(start_year, month)[1]

            if month <= 9:
                date = f"{start_year}-0{month}-{month_end_day}"
            else:
                date = f"{start_year}-{month}-{month_end_day}"

            date = str(self.__on_or_just_before(date))
            month_ends.append(date)

        # get month-ends after start_year but before end_year
        for year in range(start_year + 1, end_year):
            for month in range(1, 12 + 1):
                month_end_day = calendar.monthrange(year, month)[1]

                if month <= 9:
                    date = f"{year}-0{month}-{month_end_day}"
                else:
                    date = f"{year}-{month}-{month_end_day}"

                date = str(self.__on_or_just_before(date))
                month_ends.append(date)

        # get month-ends in end_year
        for month in range(1, end_month + 1):
            month_end_day = calendar.monthrange(end_year, month)[1]

            if month <= 9:
                date = f"{end_year}-0{month}-{month_end_day}"
            else:
                date = f"{end_year}-{month}-{month_end_day}"

            date = str(self.__on_or_just_before(date))
            month_ends.append(date)

        return self[month_ends]

    def get_quarter_ends(self):
        """Returns timeseries containing every quarter-end within current Timeseries


        Returns
        -------
        SecurityTimeSeries
            TimeSeries object containing every quater-end
        """
        dates = self.get_month_ends().dates
        quarter_end_months = ["03", "06", "09", "12"]
        quarter_ends = []

        for idx, date in enumerate(dates):
            month = str(date).split("-")[1]
            if month in quarter_end_months:
                quarter_ends.append(dates[idx])

        return self[quarter_ends]

    def get_year_ends(self):
        """Returns timeseries containing every year-end within current Timeseries


        Returns
        -------
        SecurityTimeSeries
            TimeSeries object containing every year-end
        """
        dates = self.get_month_ends().dates
        year_end_month = ["12"]
        year_ends = []

        for idx, date in enumerate(dates):
            month = str(date).split("-")[1]
            if month in year_end_month:
                year_ends.append(dates[idx])

        return self[year_ends]

    def get_period_ends(self, freq: Literal["M", "Q", "Y"]):
        """Returns timeseries containing every period-end within current Timeseries


        Parameters
        -------
        freq: Literal["M", "Q", "Y"]
            "M" for month-end, "Q" for quarter-end, "Y" for year-end

        Returns
        -------
        SecurityTimeSeries
            TimeSeries object containing every year-end
        """
        if freq == "M":
            return self.get_month_ends()

        elif freq == "Q":
            return self.get_quarter_ends()

        elif freq == "Y":
            return self.get_year_ends()

        return None

    def get_month_starts(self):
        """Returns timeseries containing every month-start within current Timeseries

        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every month-start
        """
        start_year, start_month, _ = str(self.dates[0]).split("-")
        end_year, end_month, _ = str(self.dates[-1]).split("-")

        start_year, start_month = int(start_year), int(start_month)
        end_year, end_month = int(end_year), int(end_month)

        month_starts = []

        # get month-ends in start_year
        for month in range(start_month, 12 + 1):
            if month <= 9:
                date = f"{start_year}-0{month}-01"

            else:
                date = f"{start_year}-{month}-01"

            date = str(self.__on_or_just_after(date))
            month_starts.append(date)

        # get month-ends after start_year but before end_year
        for year in range(start_year + 1, end_year):
            for month in range(1, 12 + 1):
                if month <= 9:
                    date = f"{year}-0{month}-01"
                else:
                    date = f"{year}-{month}-01"

                date = str(self.__on_or_just_after(date))
                month_starts.append(date)

        # get month-ends in end_year
        for month in range(1, end_month + 1):
            if month <= 9:
                date = f"{end_year}-0{month}-01"
            else:
                date = f"{end_year}-{month}-01"

            date = str(self.__on_or_just_after(date))
            month_starts.append(date)

        return self[month_starts]

    def get_quarter_starts(self):
        """Returns timeseries containing every quarter-start within current Timeseries


        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every quater-start
        """
        dates = self.get_month_starts().dates
        quarter_start_months = ["01", "04", "07", "10"]
        quarter_starts = []

        for idx, date in enumerate(dates):
            month = str(date).split("-")[1]
            if month in quarter_start_months:
                quarter_starts.append(dates[idx])

        return self[quarter_starts]

    def get_year_starts(self):
        """Returns timeseries containing every year-start within current Timeseries


        Returns
        -------
        AbstractTimeSeries
            TimeSeries object containing every year-start
        """
        dates = self.get_month_starts().dates
        year_start_month = ["1"]
        year_starts = []

        for idx, date in enumerate(dates):
            month = str(date).split("-")[1]
            if month in year_start_month:
                year_starts.append(dates[idx])

        return self[year_starts]

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

        if freq == "M":
            return self.get_month_starts()

        elif freq == "Q":
            return self.get_quarter_starts()

        elif freq == "Y":
            return self.get_year_starts()

        return None

    def split_month(self) -> list:
        """Split series into each month


        Returns
        -------
        List[AbstractTimeSeries]
            List of TimeSeries object, with each element representing one month
        """

        months = []

        month_dates = self.get_month_starts().get_dates()

        month_indices = np.isin(self.dates, month_dates)
        month_indices = list(np.argwhere(month_indices == True).flatten())

        # Handle edge case where first month start in data happens to be the first row
        try:
            month_indices.remove(0)
        except ValueError:
            pass
        month_indices.insert(0, 0)

        # Handle edge case where last month start in data happens to be the last row
        if month_indices[-1] == len(self.dates) - 1:
            month_indices[-1] += 1
        else:
            month_indices.append(len(self.dates))

        for idx, i in enumerate(month_indices[:-1]):
            start_index = i
            end_index = month_indices[idx + 1]

            current_slice = self.__make_self(
                self.dates[start_index:end_index],
                self.prices[start_index:end_index],
                self.tot_ret_idx[start_index:end_index],
            )

            months.append(current_slice)

        return months

    def split_quarter(self) -> list:
        """Split series into each month


        Returns
        -------
        List[AbstractTimeSeries]
            List of TimeSeries object, with each element representing one quarter
        """
        quarters = []

        quarter_dates = self.get_quarter_starts().get_dates()

        quarter_indices = np.isin(self.dates, quarter_dates)
        quarter_indices = list(np.argwhere(quarter_indices == True).flatten())

        # Handle edge case where first month start in data happens to be the first row
        try:
            quarter_indices.remove(0)
        except ValueError:
            pass
        quarter_indices.insert(0, 0)

        # Handle edge case where last month start in data happens to be the last row
        if quarter_indices[-1] == len(self.dates) - 1:
            quarter_indices[-1] += 1
        else:
            quarter_indices.append(len(self.dates))

        for idx, i in enumerate(quarter_indices[:-1]):
            start_index = i
            end_index = quarter_indices[idx + 1]

            current_slice = self.__make_self(
                self.dates[start_index:end_index],
                self.prices[start_index:end_index],
                self.tot_ret_idx[start_index:end_index],
            )

            quarters.append(current_slice)

        return quarters

    def split_year(self) -> list:
        """Split series into each month


        Returns
        -------
        List[AbstractTimeSeries]
            List of TimeSeries object, with each element representing one year
        """
        years = []

        year_dates = self.get_year_starts().get_dates()

        year_indices = np.isin(self.dates, year_dates)
        year_indices = list(np.argwhere(year_indices == True).flatten())

        # Handle edge case where first month start in data happens to be the first row
        try:
            year_indices.remove(0)
        except ValueError:
            pass
        year_indices.insert(0, 0)

        # Handle edge case where last month start in data happens to be the last row
        if year_indices[-1] == len(self.dates) - 1:
            year_indices[-1] += 1
        else:
            year_indices.append(len(self.dates))

        for idx, i in enumerate(year_indices[:-1]):
            start_index = i
            end_index = year_indices[idx + 1]

            current_slice = self.__make_self(
                self.dates[start_index:end_index],
                self.prices[start_index:end_index],
                self.tot_ret_idx[start_index:end_index],
            )

            years.append(current_slice)

        return years
