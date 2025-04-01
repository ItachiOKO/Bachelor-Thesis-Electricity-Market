import pandas as pd
from config import PATH_MARKET_DATA, SKIPROWS, START_DATE, END_DATE, PATH_PRL_DATA, CELL_NAMES



def load_fcr_data() -> pd.DataFrame:
    df = pd.read_excel(
        PATH_PRL_DATA,
        parse_dates=["DATE_FROM", "DATE_TO"],
    )
    
    df["start_hour"] = (
        df["PRODUCTNAME"]
        .str.split("_")
        .str[1]        
        .astype(int)    
    )
    
    df[CELL_NAMES['date']] = (
        df["DATE_FROM"].dt.floor("D")  
        + pd.to_timedelta(df["start_hour"], unit="H")
    )

    df[CELL_NAMES['date']] = df[CELL_NAMES['date']].dt.tz_localize("Europe/Berlin")
    df.set_index(CELL_NAMES['date'], inplace=True)
    df = df[["GERMANY_SETTLEMENTCAPACITY_PRICE_[EUR/MW]"]]
    return df

df_fcr_price = load_fcr_data()
print(df_fcr_price)
#print types





