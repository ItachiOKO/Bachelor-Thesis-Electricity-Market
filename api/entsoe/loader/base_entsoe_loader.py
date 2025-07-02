from abc import abstractmethod
from ...base_loader import BaseLoader
from ..client import EntsoeApiClient

class EntsoeBaseLoader(BaseLoader):
    """
    Eine spezifische Basisklasse für alle ENTSO-E Loader.
    Bündelt gemeinsame Logik wie Client und Parameter-Struktur.
    """
    def __init__(self, api_key: str):
        self.client = EntsoeApiClient()
        self.params = {"securityToken": api_key}
        self._set_document_specific_params()

    def load(self, period_start: str, period_end: str):
        self.params.update({"periodStart": period_start, "periodEnd": period_end})
        xml_data = self.client.fetch_xml(self.params)
        return self.parse(xml_data)

    @abstractmethod
    def _set_document_specific_params(self):
        """Erzwingt das Setzen von dokumentspezifischen API-Parametern."""
        pass

    @abstractmethod
    def parse(self, xml_string: str):
        """Erzwingt die Implementierung eines Parsers."""
        pass