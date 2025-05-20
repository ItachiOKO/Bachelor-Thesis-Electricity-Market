#Data Config
START_DATE = "2023-01-01" #included
END_DATE = "2023-02-01" #excluded
PATH_MARKET_DATA = "data\energy-charts_Stromproduktion_und_Börsenstrompreise_in_Deutschland_2023.csv"
PATH_INTRADAY_DATA = "data\Energy-Charts - 2023 - Komplett.xlsx"
PATH_PRL_DATA = "data\RESULT_OVERVIEW_CAPACITY_MARKET_FCR_2023-01-01_2023-12-31.xlsx"
PATH_SRL_POWER_DATA = 'data/Leistung_Ergebnisse_SRL_2023-01-01_2023-12-31.xlsx'
PATH_SRL_WORK_DATA = 'data/Arbeit_Ergebnisse_2023_SRL_2023-01-01_2023-12-31.xlsx'


#Battery Config
BATTERY_CAPACITY = 1 #MWh
SYSTEM_POWER = 1 #MW (1MW = 1MWh/1h)
BATTERY_PRICE = 270000 * BATTERY_CAPACITY #€
LIFETIME_CYCLES = 9000
EFFICIENCY = 0.86 # einseitiger Wirkungsgrad (jeweils Lade- und Entladeverluste)
SPECIFIC_AGING_COST = BATTERY_PRICE / (BATTERY_CAPACITY * LIFETIME_CYCLES * 2) #€/(MWh*Cycle)


#Regelleistungsmarkt Config
SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE = 1/3 # 1/3 -> MWh/MW (in 4 Stunden)
SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE = 1/99 # 1/99 -> MWh/MW (in 15min)


#Export Config
RESULTS_FILE_NAME_EXCEL =  f"results_{BATTERY_CAPACITY}MWH_SCR-{SYSTEM_POWER}MW_P-{BATTERY_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}.xlsx"
RESULTS_FILE_NAME_PICKLE = f"results_{BATTERY_CAPACITY}MWH_SCR-{SYSTEM_POWER}MW_P-{BATTERY_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}.pkl"


#Table Config
class ColumnNamesRaw:
    ID_PRICE         = 'Intraday Auktion, 15 Minuten Preis (DE-LU) (EUR / MWh)'
    PRL_PRICE        = 'GERMANY_SETTLEMENTCAPACITY_PRICE_[EUR/MW]' #€/MWh
    SRL_POWER_PRICE  = 'GERMANY_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]' #€/MWh
    SRL_WORK_PRICE = 'GERMANY_AVERAGE_ENERGY_PRICE_[EUR/MWh]' #€/MWh


class ColumnNamesClean:
    DATE                 = 'Date'
    DA_PRICE             = 'Day-Ahead Price'
    ID_PRICE             = 'Intra-Day Price'

    PRL_PRICE            = 'PRL Price'
    SRL_POWER_PRICE_POS  = 'SRL Power Price Pos'
    SRL_POWER_PRICE_NEG  = 'SRL Power Price Neg'
    SRL_WORK_PRICE_POS   = 'SRL Wokr Price Pos'
    SRL_WORK_PRICE_NEG   = 'SRL Wokr Price Neg'


    BUY_VOL           = 'Buy Volume'
    SELL_VOL          = 'Sell Volume'
    BAT_SOC          = 'Battery SOC'
    PRL_POWER         = 'PRL Power'
    SRL_POWER_POS        = 'SRL Power Pos'
    SRL_POWER_NEG        = 'SRL Power Neg'
    AGING_COST           = 'Aging Cost'
    
    PROFIT_CALC          = 'Profit'
    ORDER_COST           = 'Net order value'
