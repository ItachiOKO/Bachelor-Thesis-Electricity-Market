
#Table Config
class ColumnNamesRaw:
    ENERGIE_CHARTS_DATE         = 'datum und uhrzeit'
    DA_AUC_PRICE                = 'day ahead auktion exaa' # Day-Ahead Auction Price (EUR / MWh)
    ID_PRICE_AUC_15min          = 'intraday auktion, 15 minuten preis'
    ID_PRICE_AUC_IDA1_GEKOPPELT = 'gekoppelte intraday auktion, 15 minuten ida1-preis'
    PRL_PRICE                   = 'DE_SETTLEMENTCAPACITY_PRICE_[EUR/MW]' #€/MWh
    SRL_POWER_PRICE             = 'GERMANY_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]' #€/MWh; muss neu aus original Daten gezogen werden wenn geändert wird
    SRL_WORK_PRICE_NEG              = 'Bester Preis NEG (EUR / MWh)' #€/MWh, nur die Spalte enthalten, ggf. neu aus original Daten ziehen wenn geändert wird
    SRL_WORK_PRICE_POS              = 'Bester Preis POS (EUR / MWh)' #€/MWh, nur die Spalte enthalten, ggf. neu aus original Daten ziehen wenn geändert wird

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
    SRL_WORK_PRICE_POS   = 'SRL Work Price Pos'
    SRL_WORK_PRICE_NEG   = 'SRL Work Price Neg'

    #results
    BUY_VOL              = 'Buy Volume'
    SELL_VOL             = 'Sell Volume'
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
    REVENUE_TOTAL_SUM   = 'Total Revenue Sum'
    TAXES_SUM           = 'Taxes Sum'
    OBJ                 = 'Objective Value'
