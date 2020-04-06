import pandas as pd
from src.backend import pipeline

df = pd.read_csv("/Users/robertbao/Downloads/tesla_5000.csv",
                 error_bad_lines=False, encoding='UTF-8')
df = df.drop_duplicates()
df = df.dropna()
# df['date'] = pd.to_datetime(df['date'])
# df = df.sort_values(by='date')
# print(df)
# print(len(df.index))
# print(df.iat[0, 0])
# print("------")
# print(df.iat[(len(df.index) - 1), 0])
# print("------")
# print(df.tail(1))
# print("------")
# time = df.iat[(len(df.index) - 1), 0] - df.iat[0, 0]
# print(time.days)
# print(type(time))
df = pipeline(df, clf='sgd')
print(df)
# Group the sentiment by date
# df.Index = pd.to_datetime(df['date'])
# day = df.Index.dt.date
#
# sentiment_df = df.groupby(day).sentiment.mean().reset_index(name='sentiment')
# sentiment_df.sentiment = sentiment_df.sentiment.round(2)
# print("----------")
# # quantity = df['name']
# # print(quantity)
# # print(quantity.nunique())
# print(sentiment_df)
df.Index = pd.to_datetime(df['date'])
day = df.Index.dt.date
quantity_df = df.groupby(day).text.size().reset_index(name='quantity')
print(quantity_df)
