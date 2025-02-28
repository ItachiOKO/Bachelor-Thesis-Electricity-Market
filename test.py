from config import PATH_PRL_DATA
import pandas as pd

df = pd.read_excel(PATH_PRL_DATA, sheet_name="001")

df_x = df["GERMANY_SETTLEMENTCAPACITY_PRICE_[EUR/MW]"].tolist()
print(df_x)