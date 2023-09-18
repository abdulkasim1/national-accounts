import pandas as pd

df = pd.read_excel("NATP.ESA10.05_SDMX Output_Live_20_Jul_2023 - XML imported to Excel.xlsx")

df = df[["EXPENDITURE", "STO", "PRICES", "FREQ", "ADJUSTMENT",
       "REF_AREA", "COUNTERPART_AREA", "REF_SECTOR", "COUNTERPART_SECTOR",
       "ACCOUNTING_ENTRY", "INSTR_ASSET", "ACTIVITY", "UNIT_MEASURE",
       "TRANSFORMATION", "TIME_FORMAT", "REF_YEAR_PRICE", "DECIMALS",
       "TABLE_IDENTIFIER", "UNIT_MULT", "COMPILING_ORG",
       "TIME_PERIOD", "OBS_VALUE", "OBS_STATUS", "CONF_STATUS"]]

df.to_csv("na_2019Q3.csv", index=False)