import pandas as pd
import numpy as np
import os
import re
from datetime import datetime

def verarbeite_balancing_xml_final(xml_pfad, excel_pfad, pickle_pfad):
    """
    Liest eine Balancing-Energy-XML-Datei, verarbeitet zwei Zeitreihen,
    respektiert explizit leere Preise beim Auffüllen und speichert das
    Ergebnis in einer Excel- und einer Pickle-Datei.
    """
    try:
        # Schritt 1: Datum aus dem Dateinamen extrahieren
        dateiname = os.path.basename(xml_pfad)
        match = re.search(r'\d{12}-(\d{12})', dateiname)
        if not match:
            print(f"FEHLER: Konnte das Datumsformat im Dateinamen '{dateiname}' nicht finden. Datei wird übersprungen.")
            return
        end_datum_str = match.group(1)
        basis_datum = datetime.strptime(end_datum_str, '%Y%m%d%H%M').date()
        print(f"Datum '{basis_datum}' wurde aus dem Dateinamen extrahiert.")

        # Schritt 2: XML-Daten für beide Zeitreihen einlesen
        namespaces = {'ns': 'urn:iec62325.351:tc57wg16:451-6:balancingdocument:4:1'}
        xpath_up = '(//ns:TimeSeries)[1]//ns:Point'
        xpath_down = '(//ns:TimeSeries)[2]//ns:Point'

        print("Lese Zeitreihen (Up und Down)...")
        df_up = pd.read_xml(xml_pfad, xpath=xpath_up, namespaces=namespaces, parser="lxml")
        df_down = pd.read_xml(xml_pfad, xpath=xpath_down, namespaces=namespaces, parser="lxml")

        # Schritt 3: Datenverarbeitung und Zusammenführung
        df_up['position'] = pd.to_numeric(df_up['position'])
        df_up = df_up.drop_duplicates(subset='position', keep='first').set_index('position')
        df_up = df_up.rename(columns={'activation_Price.amount': 'Price [EUR/MWh] Up'})
        df_up = df_up.drop(columns=['imbalance_Price.category'], errors='ignore')

        df_down['position'] = pd.to_numeric(df_down['position'])
        df_down = df_down.drop_duplicates(subset='position', keep='first').set_index('position')
        df_down = df_down.rename(columns={'activation_Price.amount': 'Price [EUR/MWh] Down'})
        df_down = df_down.drop(columns=['imbalance_Price.category'], errors='ignore')
        
        df_merged = pd.concat([df_up, df_down], axis=1)
        print("Beide Zeitreihen zusammengeführt. Starte Auffüll-Logik...")

        # --- VERBESSERTE AUFFÜLL-LOGIK ---
        placeholder = -999999.99
        df_merged_with_placeholder = df_merged.fillna(placeholder)
        vollstaendiger_index = pd.RangeIndex(start=1, stop=21601, name='position')
        df_reindexed = df_merged_with_placeholder.reindex(vollstaendiger_index)
        df_filled = df_reindexed.ffill()
        df_final = df_filled.replace(placeholder, np.nan)
        print("Fehlende Positionen wurden korrekt aufgefüllt (explizite Lücken bleiben erhalten).")
        
        # Schritt 9: Zeitstempel erstellen
        df_final = df_final.reset_index()
        start_zeitstempel = pd.to_datetime(basis_datum)
        zeit_offset = pd.to_timedelta((df_final['position'] - 1) * 4, unit='s')
        df_final['Datum'] = start_zeitstempel + zeit_offset
        print("Zeitstempel-Spalte 'Datum' wurde erstellt.")

        # Schritt 10: Finale Spaltenanordnung
        finale_spalten_reihenfolge = ['position', 'Datum', 'Price [EUR/MWh] Up', 'Price [EUR/MWh] Down']
        df_final = df_final[finale_spalten_reihenfolge]
        
        # Schritt 11: Speichern als Excel UND Pickle
        # Excel
        df_final.to_excel(excel_pfad, index=False)
        # Pickle
        df_final.to_pickle(pickle_pfad)
        
        print(f"\nERFOLGREICH ABGESCHLOSSEN:")
        print(f" -> Excel gespeichert in: '{excel_pfad}'")
        print(f" -> Pickle gespeichert in: '{pickle_pfad}'")

    except ValueError as ve:
        print(f"Ein Wert-Fehler ist aufgetreten bei Datei '{dateiname}': {ve}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten bei Datei '{dateiname}': {e}")


# --- ANLEITUNG & AUTOMATISIERUNG ---
if __name__ == "__main__":
    # 1. Definieren der Ordnerpfade
    eingabe_ordner = r"D:\WirSOlar\Bachelor-Thesis-Electricity-Market\data_moden\xml_srl_work_prices"
    ausgabe_ordner_xlsx = r"D:\WirSOlar\Bachelor-Thesis-Electricity-Market\data_moden\xml_srl_work_prices\xlsx"
    ausgabe_ordner_pkl = r"D:\WirSOlar\Bachelor-Thesis-Electricity-Market\data_moden\xml_srl_work_prices\pkl"

    # 2. Erstellen der Ausgabeordner, falls sie nicht existieren
    os.makedirs(ausgabe_ordner_xlsx, exist_ok=True)
    os.makedirs(ausgabe_ordner_pkl, exist_ok=True)
    print(f"Eingabeordner: {eingabe_ordner}")
    print(f"Ausgabeordner für Excel: {ausgabe_ordner_xlsx}")
    print(f"Ausgabeordner für Pickle: {ausgabe_ordner_pkl}\n")

    # 3. Alle XML-Dateien im Eingabeordner durchlaufen
    dateien_im_ordner = os.listdir(eingabe_ordner)
    xml_dateien = [f for f in dateien_im_ordner if f.lower().endswith('.xml')]
    
    if not xml_dateien:
        print("Keine XML-Dateien im angegebenen Ordner gefunden.")
    else:
        print(f"{len(xml_dateien)} XML-Dateien zur Verarbeitung gefunden.\n")

    for dateiname in xml_dateien:
        print(f"--- Starte Verarbeitung von: {dateiname} ---")
        
        # Vollständige Pfade für Ein- und Ausgabedateien erstellen
        eingabe_xml_datei = os.path.join(eingabe_ordner, dateiname)
        
        # Dateiname ohne die .xml-Endung extrahieren
        basis_dateiname = os.path.splitext(dateiname)[0]
        
        # Ausgabepfade erstellen
        ausgabe_excel_datei = os.path.join(ausgabe_ordner_xlsx, basis_dateiname + ".xlsx")
        ausgabe_pickle_datei = os.path.join(ausgabe_ordner_pkl, basis_dateiname + ".pkl")

        # Die Verarbeitungsfunktion für die aktuelle Datei aufrufen
        verarbeite_balancing_xml_final(eingabe_xml_datei, ausgabe_excel_datei, ausgabe_pickle_datei)
        print("---------------------------------------------------\n")

    print("Alle Dateien wurden verarbeitet.")