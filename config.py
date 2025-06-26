from pathlib import Path


#Data Config
START_DATE = "2023-01-01" #included
END_DATE = "2023-03-01" #excluded

PATH_DA_AUC_DATA = "data\Energy-Charts DayAhead 2021 bis 2024.xlsx"
PATH_INTRADAY_DATA = "data\Energy-Charts Intraday 2021 bis 2024.xlsx"
PATH_PRL_DATA = "data\Primär Ergebnisse 2021 bis 2024.xlsx"
PATH_SRL_POWER_DATA = 'data/Sekundär Leistung Ergebnisse 2021 bis 2024.xlsx'
PATH_SRL_WORK_DATA = 'data/SRL Arbeitspreise berechnet 2021 bis 2024.xlsx'


#Battery Config
BAT_CAPACITY = 1.2 #MWh
SYSTEM_POWER = 1.2 #MW (1MW = 1MWh/1h)
BAT_PRICE = 270000 * BAT_CAPACITY #€
LIFETIME_CYCLES = 9000
EFFICIENCY = 0.86 # AC Seitig vom Umrichter. einseitiger Wirkungsgrad (jeweils Lade- und Entladeverluste)
SPECIFIC_AGING_COST = BAT_PRICE / (BAT_CAPACITY * LIFETIME_CYCLES * 2) #€/(MWh durchsatz) sowohl Laden als auch Entladen
CHARGE_RATE = SYSTEM_POWER * (15/60) 


#Regelleistungsmarkt Config
SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE = 1/3 / 16 # 1/3 -> MWh/MW (in 4 Stunden) 1/3 / 16 -> MWh/MW (in 15min)
SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE = 1/99 # 1/99 -> MWh/MW (in 15min)

#Märkte
MARKET_SWITCH = 1
PRL_SWITCH = 1
SRL_SWITCH = 1

#Export Config
RESULTS_DIR = Path("results")
FILE_NAME = f"results_market-{MARKET_SWITCH}_prl-{PRL_SWITCH}_srl-{SRL_SWITCH}_{BAT_CAPACITY}-MWH_{SYSTEM_POWER}MW_{BAT_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}"
RESULTS_FILE_NAME_EXCEL =  f"{FILE_NAME}.xlsx"
RESULTS_FILE_NAME_PICKLE = f"{FILE_NAME}.pkl"






