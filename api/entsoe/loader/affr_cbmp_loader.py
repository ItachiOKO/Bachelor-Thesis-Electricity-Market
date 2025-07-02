import pandas as pd
from .base_entsoe_loader import EntsoeBaseLoader
from ..parsers.affr_cbmp_parser import parse_affr_cbmp

class AffrCbmpLoader(EntsoeBaseLoader):
    """Lädt Daten  'Crossborder Marginal Prices (A84)"""
    
    def _set_document_specific_params(self):
        """Setzt die festen API-Parameter für dieses Dokument."""
        self.params.update({
            "documentType": "A84",
            "processType": "A67",
            "businessType": "A96",
            "Standard_MarketProduct": "A01",
            "controlArea_Domain": "10YDE-VE-------2",
        })

    def parse(self, xml_string: str) -> pd.DataFrame:
        """Delegiert das Parsen an die zuständige Parser-Funktion."""
        return parse_affr_cbmp(xml_string)