import numpy as np

from ..abstracts import Data


class SimConnection(Data.Connection):
    def get_prices(self, start_date: str, end_date: str) -> Data.TimeSeries:
        days_delta = np.datetime64(end_date) - np.datetime64(start_date)
        days_delta = days_delta.astype(
            'timedelta64[D]') // np.timedelta64(1, 'D')

        dates = np.array(start_date, dtype=np.datetime64)
        dates = dates + np.arange(days_delta)

        prices = np.random.default_rng().normal(0, 0.1, days_delta) + 1
        prices[0] = 100
        prices = np.cumprod(prices)

        return SimTimeSeries(dates, prices)

    def get_desc(self) -> Data.Descriptives:
        pass


class SimTimeSeries(Data.TimeSeries):
    pass


class SimDescriptives(Data.Descriptives):
    pass
