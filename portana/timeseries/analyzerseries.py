from typing import Union

import numpy as np
import pandas as pd

from ..abstracts import Data


class AnalyzerSeries(Data.TimeSeries):
    def __init__(self, dates: np.ndarray, results: np.ndarray, col_names: List[str]):
        self.dates = dates
        self.results = results
        self.col_names = col_names

    def __make_self(self, dates: np.ndarray, prices: np.ndarray, col_names: List[str]):
        return AnalyzerSeries(dates, results, col_names)

    def __getitem__(self, subscript: Union[str, list, slice]):
        if isinstance(subscript, slice):
            match = (self.dates >= np.datetime64(subscript.start)) & (
                self.dates < np.datetime64(subscript.stop)
            )
            return self.__make_self(
                self.dates[match][:: subscript.step],
                self.results[match][:: subscript.step],
            )

        elif isinstance(subscript, str):
            match = self.dates == np.datetime64(subscript)

        elif isinstance(subscript, list):
            items = []
            for item in subscript:
                items.append(np.datetime64(item))

            match = np.isin(self.dates, items)

        return self.__make_self(
            self.dates[match], self.results[match], self.col_names[match]
        )

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame(data=self.results, index=self.dates, columns=self.col_names)
        return df
