from typing import Literal, Dict, List

from ..abstracts.optimizer import AbstractOptimizer
from ..abstracts.data import AbstractQuery
from ..abstracts.data import AbstractSecurity


class SecurityReplacementOptimizer(AbstractOptimizer):
    def __init__(self):
        self.query_engine = None

    def set_query_engine(self, engine: AbstractQuery):
        self.query_engine = engine

    def suggest(
        self,
        security: AbstractSecurity,
        optimize_by: Literal["5y_sharpe"],
        lim: int,
        offset: int,
    ) -> Dict[str, List[str]]:
        asset_type = type(security).__name__
        exposures = security.get_exposures()

        query = self.query_engine(asset_type, exposures, optimize_by, lim, offset)
        res = query.send_query()

        return {security.get_isin(): list(res.keys())}
