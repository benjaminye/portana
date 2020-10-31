from abc import ABC, abstractmethod


class AbstractOptimizer(ABC):
    """Class to ingest a portfolio or security and outputs alternative(s)"""

    @abstractmethod
    def suggest(self) -> dict:
        """Outputs a dictionary of suggested replacements."""
        pass
