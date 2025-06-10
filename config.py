from pathlib import Path


#Data Config
START_DATE = "2021-12-30" #included
END_DATE = "2022-01-05" #excluded

PATH_DA_AUC_DATA = "data\Energy-Charts DayAhead 2021 bis 2024.xlsx"
PATH_INTRADAY_DATA = "data\Energy-Charts Intraday 2021 bis 2024.xlsx"
PATH_PRL_DATA = "data\Primär Ergebnisse 2021 bis 2024.xlsx"
PATH_SRL_POWER_DATA = 'data/Sekundär Leistung Ergebnisse 2021 bis 2024.xlsx'
PATH_SRL_WORK_DATA = 'data/Sekundär Arbeit Ergebnisse 2021 bis 2024.xlsx'


#Battery Config
BAT_CAPACITY = 1 #MWh
SYSTEM_POWER = 1 #MW (1MW = 1MWh/1h)
BAT_PRICE = 270000 * BAT_CAPACITY #€
LIFETIME_CYCLES = 9000
EFFICIENCY = 0.86 # AC Seitig vom Umrichter. einseitiger Wirkungsgrad (jeweils Lade- und Entladeverluste)
SPECIFIC_AGING_COST = BAT_PRICE / (BAT_CAPACITY * LIFETIME_CYCLES * 2) #€/(MWh*Cycle)
CHARGE_RATE = SYSTEM_POWER * (15/60) 


#Regelleistungsmarkt Config
SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE = 1/3 # 1/3 -> MWh/MW (in 4 Stunden)
SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE = 1/99 # 1/99 -> MWh/MW (in 15min)


#Export Config
RESULTS_DIR = Path("results")
RESULTS_FILE_NAME_EXCEL =  f"results_{BAT_CAPACITY}MWH_SCR-{SYSTEM_POWER}MW_P-{BAT_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}.xlsx"
RESULTS_FILE_NAME_PICKLE = f"results_{BAT_CAPACITY}MWH_SCR-{SYSTEM_POWER}MW_P-{BAT_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}.pkl"


#Table Config
class ColumnNamesRaw:
    ENERGIE_CHARTS_DATE         = 'datum und uhrzeit'
    DA_AUC_PRICE                = 'day ahead auktion exaa' # Day-Ahead Auction Price (EUR / MWh)
    ID_PRICE_AUC_15min          = 'intraday auktion, 15 minuten preis'
    ID_PRICE_AUC_IDA1_GEKOPPELT = 'gekoppelte intraday auktion, 15 minuten ida1-preis'
    PRL_PRICE                   = 'DE_SETTLEMENTCAPACITY_PRICE_[EUR/MW]' #€/MWh
    SRL_POWER_PRICE             = 'GERMANY_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]' #€/MWh; muss neu aus original Daten gezogen werden wenn geändert wird
    SRL_WORK_PRICE              = 'GERMANY_AVERAGE_ENERGY_PRICE_[EUR/MWh]' #€/MWh, nur die Spalte enthalten, ggf. neu aus original Daten ziehen wenn geändert wird


class ColumnNamesClean:
    #data
    DATE                 = 'Date'
    DA_AUC_PRICE            = 'DA'
    ID_AUC_PRICE             = 'ID'
    HiGHER_MARKET_PRICE = 'Higher Market Price'
    LOWER_MARKET_PRICE  = 'Lower Market Price'
    MARKET_HI            = 'Market Higher'
    MARKET_LO            = 'Market Lower'

    PRL_PRICE            = 'PRL Price'
    SRL_POWER_PRICE_POS  = 'SRL Power Price Pos'
    SRL_POWER_PRICE_NEG  = 'SRL Power Price Neg'
    SRL_WORK_PRICE_POS   = 'SRL Wokr Price Pos'
    SRL_WORK_PRICE_NEG   = 'SRL Wokr Price Neg'

    #results
    DA_AUC_BUY_VOL       = 'Buy Volume Day-Ahead Auc'
    DA_AUC_SELL_VOL      = 'Sell Volume Day-Ahead Auc'
    ID_BUY_VOL           = 'Buy Volume Intraday'
    ID_SELL_VOL          = 'Sell Volume Intraday'
    BAT_SOC              = 'Battery SOC'
    PRL_POWER            = 'PRL Power'
    SRL_POWER_POS        = 'SRL Power Pos'
    SRL_POWER_NEG        = 'SRL Power Neg'
    AGING_COST           = 'Aging Cost'
    
    REVENUE_MARKET       = 'Revenue Market'
    REVENUE_PRL          = 'Revenue PRL'    
    REVENUE_SRL          = 'Revenue SRL'
    REVENUE_TOTAL        = 'Total Revenue'

    #attrs
    PRL_POWER_SUM       = 'PRL Power Sum'
    SRL_POWER_POS_SUM   = 'SRL Power Pos Sum'
    SRL_POWER_NEG_SUM   = 'SRL Power Neg Sum'
    AGING_COST_SUM      = 'Aging Cost Sum'


    REVENUE_MARKET_SUM  = 'Revenue Market Sum'
    REVENUE_PRL_SUM     = 'Revenue PRL Sum'
    REVENUE_SRL_SUM     = 'Revenue SRL Sum'  
    TOTAL_REVENUE_SUM   = 'Total Revenue Sum'
    TAXES_SUM           = 'Taxes Sum'
    OBJ                 = 'Objective Value'





