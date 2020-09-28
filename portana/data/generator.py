from typing import List, Tuple
import string
import random

import numpy as np


class Generator:
    # TODO: Maybe seperate into SubGenerators for different AssetClass; having them inherit this class
    def __init__(self):
        self.seed: int = None
        self.max_drift: float = None
        self.max_vol: float = None
        self.max_distribution: float = None
        self.date_range: Tuple[str, str] = None
        self.initial_price_range: Tuple[int, int] = None

        self.days_delta: int = None
        self.drift: float = None
        self.vol: float = None
        self.distribution: float = None
        self.initial_price: float = None

    def set_seed(self, seed: int) -> None:
        self.seed = seed

        random.seed(a=self.seed)
        self.drift = random.uniform(0, self.max_drift)

        random.seed(a=self.seed)
        self.vol = random.uniform(0, self.max_vol)

        random.seed(a=self.seed)
        self.distribution = random.uniform(0, self.max_distribution)

        random.seed(a=self.seed)
        self.initial_price = random.uniform(
            self.initial_price_range[0], self.initial_price_range[1]
        )

    def set_max_drift(self, max_drift: float) -> None:
        self.max_drift = max_drift

    def set_max_vol(self, max_vol: float) -> None:
        self.max_vol = max_vol

    def set_max_distribution(self, max_distribution: float) -> None:
        self.max_distribution = max_distribution

    def set_date_range(self, date_range: Tuple[str, str]) -> None:
        self.date_range = date_range

        days_delta = (
            np.datetime64(self.date_range[1]) - np.datetime64(self.date_range[0]) + 1
        )
        self.days_delta = days_delta.astype("timedelta64[D]") // np.timedelta64(1, "D")

    def set_initial_price_range(self, price_range: Tuple[int, int]) -> None:
        self.initial_price_range = price_range

    def generate_dates(self) -> np.ndarray:

        dates = np.array(self.date_range[0], dtype=np.datetime64)
        dates = dates + np.arange(self.days_delta)

        return dates

    def generate_prices(self) -> np.ndarray:
        prices = (
            np.random.default_rng(self.seed).normal(
                self.drift, self.vol, self.days_delta
            )
            + 1
        )

        prices[0] = self.initial_price
        prices = np.cumprod(prices)

        return prices

    def generate_tot_ret_idx(self) -> np.ndarray:
        tot_ret_idx = (
            np.random.default_rng(self.seed).normal(
                self.drift, self.vol, self.days_delta
            )
            + 1
            + self.distribution
        )
        tot_ret_idx[0] = 100
        tot_ret_idx = np.cumprod(tot_ret_idx)

        return tot_ret_idx

    def generate_name(self) -> str:
        return f"Simulated Security {self.seed}"

    def generate_ticker(self) -> str:
        random.seed(a=self.seed)
        length = random.choice(range(1, 5))
        letters = string.ascii_uppercase

        ticker = ""
        for i in range(length):
            random.seed(a=self.seed + i)
            ticker += random.choice(letters)

        return ticker

    def generate_fee(self) -> float:
        random.seed(a=self.seed)
        fee = random.uniform(0, 0.02)

        return round(fee, 3)

    def generate_sector(self) -> str:
        sectors = ["Technology", "Industrials", "Financials"]
        return self.__random_choice(sectors)

    def generate_geography(self) -> str:
        geographies = ["United States", "Canada"]
        return self.__random_choice(geographies)

    def generate_strategy(self) -> str:
        strategies = ["Growth", "Income", "Value", "Balanced"]
        return self.__random_choice(strategies)

    def generate_risk(self) -> str:
        risks = ["High", "Medium", "Low"]
        return self.__random_choice(risks)

    def __random_choice(self, choices: list) -> str:
        random.seed(a=self.seed)
        return random.choice(choices)
