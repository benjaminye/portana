from abc import ABC, abstractmethod

from .data import AbstractSecurity

""" Abstract classes for analyzing a Security
"""

# from typing import Dict, Tuple, Union, Literal

# from numpy import ndarray

# Not Implemented
# --------------------------
# class Output(ABC):
#     @abstractmethod
#     def __repr__(self):
#         pass

#     @abstractmethod
#     def get_period_stats(
#         self,
#         freq: Union[
#             Literal["D"], Literal["W"], Literal["M"], Literal["Q"], Literal["Y"]
#         ],
#     ):
#         pass

#     @abstractmethod
#     def get_range_stats(self, date_range: Tuple[str, str]):
#         pass


class AbstractAnalyzer(ABC):
    """Abstract class to analyze a Security


    Methods
    -------
    add_security(security: Security)
        Add a Security to analyze
    set_comp_index(comp_index: Security)
        Add a benchmark; used to calculate beta
    """

    @abstractmethod
    def add_security(self, security: AbstractSecurity):
        """Add a Security to analyze


        Parameters
        -------
        security: Security
            Security object to analyze
        """
        pass

    @abstractmethod
    def set_comp_index(self, comp_index: AbstractSecurity):
        """Add a benchmark to analyze agains
        Also used for calculations such as beta

        Parameters
        -------
        security: Security
            Security object containing the benchmark
        """
        pass

    @abstractmethod
    def analyze(self):
        pass
