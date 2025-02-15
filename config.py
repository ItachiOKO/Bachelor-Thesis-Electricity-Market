#Data Config
START_DATE = "2023-01-01" #included
END_DATE = "2023-01-02" #excluded
CSV_PATH = "energy-charts_Stromproduktion_und_Börsenstrompreise_in_Deutschland_2023.csv"
STEP_INTERVAL = "15min"
SKIPROWS = 2

#Battery Config
BATTERY_CAPACITY = 1 #MWh
BATTERY_PRICE = 150000 #€
LIFETIME_CYCLES = 5000
EFFICIENCY = 0.96 
SPECIFIC_CHARGE_RATE = 1 #MW

#Export Config
RESULTS_FILE_NAME = f"results_BC-{BATTERY_CAPACITY}_n-{EFFICIENCY}_{START_DATE}-{END_DATE}.xlsx"
