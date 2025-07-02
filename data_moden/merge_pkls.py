import os
import pickle

def merge_pickle_files(folder_path, output_filename):
    """
    Sucht alle .pkl-Dateien in einem Ordner, sortiert sie nach Namen und
    fügt ihren Inhalt in einer einzigen .pkl-Datei zusammen.

    Args:
        folder_path (str): Der Pfad zum Ordner mit den .pkl-Dateien.
        output_filename (str): Der Name der Zieldatei (z.B. 'combined_data.pkl').
    """
    # Überprüfen, ob der Ordner existiert
    if not os.path.isdir(folder_path):
        print(f"Fehler: Der fest einprogrammierte Ordner '{folder_path}' wurde nicht gefunden.")
        return

    # 1. Alle Dateien im Ordner finden und nur die .pkl-Dateien behalten
    try:
        pickle_files = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]
    except OSError as e:
        print(f"Fehler beim Lesen des Ordners '{folder_path}': {e}")
        return
        
    # Sicherstellen, dass die Zieldatei nicht versehentlich mitverarbeitet wird
    if output_filename in pickle_files:
        pickle_files.remove(output_filename)

    if not pickle_files:
        print(f"Keine .pkl-Dateien im Ordner '{folder_path}' gefunden.")
        return

    # 2. Die Liste der Dateinamen alphabetisch sortieren
    pickle_files.sort()
    print(f"{len(pickle_files)} .pkl-Dateien gefunden und sortiert.")

    # 3. Die Daten aus jeder Datei laden und in einer Hauptliste sammeln
    combined_data = []
    print("Starte das Zusammenfügen der Dateien...")

    for i, filename in enumerate(pickle_files):
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'rb') as f:
                # 'rb' steht für 'read binary', was für pickle-Dateien notwendig ist
                data = pickle.load(f)
                combined_data.append(data)
                # Fortschrittsanzeige, nützlich bei vielen Dateien
                print(f"  ({i+1}/{len(pickle_files)}) Datei '{filename}' erfolgreich geladen.")
        except pickle.UnpicklingError:
            print(f"  FEHLER: Datei '{filename}' konnte nicht als Pickle-Datei gelesen werden. Sie wird übersprungen.")
        except Exception as e:
            print(f"  FEHLER: Ein unerwarteter Fehler ist bei Datei '{filename}' aufgetreten: {e}. Sie wird übersprungen.")
            
    # 4. Die zusammengefügte Liste in eine neue .pkl-Datei schreiben
    output_path = os.path.join(folder_path, output_filename)
    try:
        with open(output_path, 'wb') as f:
            # 'wb' steht für 'write binary'
            pickle.dump(combined_data, f)
    except IOError as e:
        print(f"Fehler beim Schreiben der Zieldatei '{output_path}': {e}")
        return

    print("\n--------------------------------------------------")
    print("Zusammenfügen erfolgreich abgeschlossen!")
    print(f"Die Daten aus {len(combined_data)} Dateien wurden in der Datei '{output_path}' gespeichert.")
    print("--------------------------------------------------")


if __name__ == "__main__":
    # --- ÄNDERUNG HIER ---
    # Der Ordnerpfad ist jetzt fest einprogrammiert.
    input_folder = r"D:\WirSOlar\Bachelor-Thesis-Electricity-Market\data_moden\xml_srl_work_prices\pkl"
    
    print("--- Skript zum Zusammenfügen von Pickle-Dateien ---")
    print(f"Benutze festen Ordnerpfad: {input_folder}")
    
    # Der Benutzer muss nur noch den Namen der Zieldatei angeben.
    output_file = input("Bitte geben Sie einen Namen für die zusammengefügte Datei an (z.B. 'merged.pkl'): ")

    # Sicherstellen, dass der Dateiname auf .pkl endet
    if not output_file.endswith('.pkl'):
        output_file += '.pkl'

    # Die Hauptfunktion aufrufen
    merge_pickle_files(input_folder, output_file)