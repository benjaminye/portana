from typing import Literal

from ..abstracts.data import AbstractQuery
from ..abstracts.optimizer import AbstractOptimizer
from ..abstracts.portfolio import AbstractPortfolio
from ..portfolio.portfolio import Portfolio


class PortfolioOptimizer(AbstractOptimizer):
    def __init__(self):
        self.optimizer: AbstractOptimizer = None
        self.portfolio: AbstractPortfolio = None

    def set_optimizer(self, optimizer: AbstractOptimizer, query_engine: AbstractQuery):
        self.optimizer = optimizer
        self.optimizer.set_query_engine(query_engine)

    def set_portfolio(self, portfolio: AbstractPortfolio):
        self.portfolio = portfolio

    def suggest(
        self,
        optimize_by: Literal["5y_sharpe"],
        lim: int,
        offset: int,
    ):
        securities = self.portfolio.get_securities()

        res = {}
        for security in securities:
            res.update(self.optimizer.suggest(security, optimize_by, lim, offset))

        return res
