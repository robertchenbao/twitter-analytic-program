import pandas as pd
from datetime import datetime

pd.set_option('display.max_columns', None)

# start = datetime.now()

df = pd.read_csv("/Volumes/RESEARCH/IR_12/data/raw/tesla_week_10.csv",
                 error_bad_lines=False, encoding='UTF-8')
df = df.drop_duplicates()
df = df.dropna()
df = df.sample(20000)
df.to_csv('tesla_20000.csv', index=False)

# df = pd.read_csv("/Users/robertbao/Desktop/tesla_5000.csv")
# print(df.head(10))
