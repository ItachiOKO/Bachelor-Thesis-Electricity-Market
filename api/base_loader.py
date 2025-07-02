from abc import ABC, abstractmethod

class BaseLoader(ABC):
    """Ganz allgemeine, abstrakte Basisklasse für jeden Daten-Loader."""

    @abstractmethod
    def load(self, **kwargs):
        """
        Lädt Daten. Die Parameter sind für jede API unterschiedlich,
        daher werden flexible Keyword-Argumente verwendet.
        """
        pass