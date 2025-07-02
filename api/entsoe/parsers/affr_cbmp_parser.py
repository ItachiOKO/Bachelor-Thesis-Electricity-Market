# data_acquisition/parsers/affr_parser.py
import xml.etree.ElementTree as ET
import pandas as pd

def parse_affr_cbmp(xml_string: str) -> pd.DataFrame:
    root = ET.fromstring(xml_string)
    uri  = root.tag.split("}")[0].strip("{")
    ns   = {"e": uri}

    records = []
    for ts in root.findall(".//e:TimeSeries", namespaces=ns):
        code      = ts.find("e:flowDirection.direction", namespaces=ns).text
        direction = "Up" if code == "A01" else "Down"
        for p in ts.findall(".//e:Point", namespaces=ns):
            pos = int(p.find("e:position", namespaces=ns).text)
            elt = p.find("e:activation_Price.amount", namespaces=ns)
            price = float(elt.text) if elt is not None else None
            records.append({
                "Position": pos,
                "Direction": direction,
                "Preis": price
            })
    df = pd.DataFrame(records)
    df_wide = (
        df
        .pivot_table(
            index="Position",
            columns="Direction",
            values="Preis",
            aggfunc="first",    # oder np.mean, wenn mehrere Werte pro Kombination möglich sind
            fill_value=None     # oder 0, wenn Du fehlende Preise als 0 sehen willst
        )
        .reset_index()
)
    return df_wide

