import os
import time
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import glob
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Konfiguration ---
BASE_URL = "https://transparency.entsoe.eu/balancing/r3/cbmpsForAfrrStandardProduct/show"
OUTPUT_DIR = os.path.abspath("entsoe_downloads")
START_DATE = "2024-01-01"
END_DATE   = "2024-01-02"

def setup_driver(download_path):
    """
    Initialisiert den WebDriver mit Optionen, um eine Bot-Erkennung zu erschweren.
    """
    print("Initialisiere Chrome-Browser im 'Stealth-Modus'...")
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    # --- OPTIONEN GEGEN BOT-ERKENNUNG ---
    # Deaktiviert das "Chrome wird von einer automatisierten Software gesteuert"-Banner
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Ändert den User-Agent, um wie ein normaler Browser auszusehen
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
    
    # Verhindert, dass die Webseite Selenium-spezifische JavaScript-Variablen abfragt
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Startet den Browser maximiert
    options.add_argument("--start-maximized")

    # Einstellungen für automatische Downloads
    prefs = {"download.default_directory": download_path, "download.prompt_for_download": False}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Die Funktionen download_data_for_day, rename_latest_download und main bleiben identisch
# Hier zur Vollständigkeit der gesamte Code:

def rename_latest_download(download_path, date_to_fetch):
    time.sleep(7)
    list_of_files = glob.glob(os.path.join(download_path, '*'))
    if not list_of_files:
        print(f"WARNUNG: Keine Datei für {date_to_fetch.strftime('%Y-%m-%d')} gefunden.")
        return False
    latest_file = max(list_of_files, key=os.path.getctime)
    if latest_file.endswith('.crdownload'):
        time.sleep(10)
        latest_file = max(glob.glob(os.path.join(download_path, '*')), key=os.path.getctime)
        if latest_file.endswith('.crdownload'):
            print(f"FEHLER: Download für {date_to_fetch.strftime('%Y-%m-%d')} unvollständig.")
            return False
    new_filename = os.path.join(download_path, f"entsoe_data_{date_to_fetch.strftime('%Y-%m-%d')}.xml.zip")
    try:
        if os.path.exists(new_filename): os.remove(latest_file)
        else: os.rename(latest_file, new_filename)
        return True
    except Exception as e:
        print(f"FEHLER beim Umbenennen für {date_to_fetch.strftime('%Y-%m-%d')}: {e}")
        return False

def download_data_for_day(driver, date_to_fetch, download_path):
    date_str_payload = date_to_fetch.strftime('%d.%m.%Y')
    params = {'viewType': 'TABLE', 'dateTime.dateTime': f'{date_str_payload} 00:00|CET|DAYTIMERANGE'}
    try:
        request = requests.Request('GET', BASE_URL, params=params).prepare()
        driver.get(request.url)
        wait = WebDriverWait(driver, 20)
        
        print("Wechsle in den iFrame...")
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
        print("Erfolgreich in den iFrame gewechselt.")

        export_button = wait.until(EC.element_to_be_clickable((By.ID, "dv-export-data")))
        export_button.click()
        
        xml_zip_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[exporttype='XML_COMPRESSED']")))
        xml_zip_link.click()

        driver.switch_to.default_content()
        
        if not rename_latest_download(download_path, date_to_fetch):
            return False
        return True
    except Exception as e:
        print(f"FEHLER bei der Verarbeitung von {date_to_fetch.strftime('%Y-%m-%d')}: {e}")
        driver.save_screenshot(f"download_fehler_{date_to_fetch.strftime('%Y-%m-%d')}.png")
        try:
            driver.switch_to.default_content()
        except: pass
        return False

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    driver = setup_driver(OUTPUT_DIR)
    driver.get(BASE_URL)
    time.sleep(35)  # Wartezeit, um sicherzustellen, dass die Seite vollständig geladen ist
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    successful_downloads, failed_downloads = [], []
    for date in tqdm(dates, desc="Herunterladen der Daten"):
        if download_data_for_day(driver, date, OUTPUT_DIR):
            successful_downloads.append(date)
        else:
            failed_downloads.append(date)
            time.sleep(5)
    driver.quit()
    print(f"\n--- Download-Zusammenfassung ---\nErfolgreich: {len(successful_downloads)}, Fehlgeschlagen: {len(failed_downloads)}")
    if failed_downloads:
        print("Fehlgeschlagene Tage:", [d.strftime('%Y-%m-%d') for d in failed_downloads])

if __name__ == "__main__":
    main()