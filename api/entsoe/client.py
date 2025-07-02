import requests

class EntsoeApiClient:
    """Ein effizienter Client für die ENTSO-E API, der eine Session nutzt."""
    API_URL = "https://web-api.tp.entsoe.eu/api"

    def __init__(self):
        # Erstellt eine Session, die für alle Anfragen wiederverwendet wird
        self.session = requests.Session()

    def fetch_xml(self, params: dict) -> str:
        # Nutzt die Session anstelle von requests.get
        resp = self.session.get(self.API_URL, params=params)
        resp.raise_for_status()
        return resp.text