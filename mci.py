# 计算第26号用户在2016-01-01当天的MCI

import pandas as pd

# read in dataset
df1 = pd.read_csv("dataset/pecan_1_min_part1.csv")

# 去除时区
df1['localminute'] = df1['localminute'].map(lambda x: str(x)[:-3])

# str时间数据转换为时间戳
df1['localminute'] = pd.to_datetime(df1['localminute'], format='%Y-%m-%d %H:%M')
df1.set_index("localminute", inplace=True)

# 切出第一天的数据
df_1day = df1['2016-01-01']

print("1-Minute total electricity consumption: ")
print(df_1day.resample('1Min').sum())

print("id = 26 consumer's 1-minute consumption: ")
print( sum(df_1day[df_1day['dataid'] == 26]['use']) )

A = 100
B = 20
print(sum( (A * (df_1day.resample('1Min').sum())['use'] + B) * df_1day[df_1day['dataid'] == 26]['use'] / sum(df_1day[df_1day['dataid'] == 26]['use']) ) )





