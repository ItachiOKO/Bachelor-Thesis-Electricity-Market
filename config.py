from pathlib import Path


#Data Config
START_DATE = "2023-01-01" #included
END_DATE = "2023-01-05" #excluded

PATH_DA_AUC_DATA = "data\Energy-Charts DayAhead 2021 bis 2024.xlsx"
PATH_INTRADAY_DATA = "data\Energy-Charts Intraday 2021 bis 2024.xlsx"
PATH_PRL_DATA = "data\Primär Ergebnisse 2021 bis 2024.xlsx"
PATH_SRL_POWER_DATA = 'data/Sekundär Leistung Ergebnisse 2021 bis 2024.xlsx'
PATH_SRL_WORK_DATA = 'data/Sekundär Arbeit Ergebnisse 2021 bis 2024.xlsx'


#Battery Config
BAT_CAPACITY = 1.2 #MWh
SYSTEM_POWER = 1.2 #MW (1MW = 1MWh/1h)
BAT_PRICE = 270000 * BAT_CAPACITY #€
LIFETIME_CYCLES = 9000
EFFICIENCY = 0.86 # AC Seitig vom Umrichter. einseitiger Wirkungsgrad (jeweils Lade- und Entladeverluste)
SPECIFIC_AGING_COST = BAT_PRICE / (BAT_CAPACITY * LIFETIME_CYCLES * 2) #€/(MWh*Cycle)
CHARGE_RATE = SYSTEM_POWER * (15/60) 


#Regelleistungsmarkt Config
SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE = 1/3 / 16 # 1/3 -> MWh/MW (in 4 Stunden) 1/3 / 16 -> MWh/MW (in 15min)
SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE = 1/99 # 1/99 -> MWh/MW (in 15min)


#Export Config
RESULTS_DIR = Path("results")
FILE_NAME = f"results_{BAT_CAPACITY}MWH_SCR-{SYSTEM_POWER}MW_P-{BAT_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}"
RESULTS_FILE_NAME_EXCEL =  f"{FILE_NAME}.xlsx"
RESULTS_FILE_NAME_PICKLE = f"{FILE_NAME}.pkl"






