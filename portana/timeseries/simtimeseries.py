from typing import Union, Tuple

import numpy as np
import pandas as pd

from ..abstracts import Data


class SimTimeSeries(Data.TimeSeries):
    def __init__(self, dates: np.ndarray, prices: np.ndarray, tot_ret_idx: np.ndarray):
        self.dates = dates
        self.prices = prices
        self.tot_ret_idx = tot_ret_idx

    def __make_self(
        self, dates: np.ndarray, prices: np.ndarray, tot_ret_idx: np.ndarray
    ):
        return SimTimeSeries(dates, prices, tot_ret_idx)

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
        df = pd.DataFrame(
            data={"Price": self.prices, "Total Return Index": self.tot_ret_idx},
            index=self.dates,
        )
        return df

    def get_dates(self) -> np.ndarray:
        return self.dates

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.prices, self.tot_ret_idx
