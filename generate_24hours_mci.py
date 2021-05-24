'''
计算2016-01-01当天所有用户在24小时时段内的MCI（24个，基于每小时）
连同用户当天总消费存入user_24hours_mci_cleaned.scv

因为只提取一天的数据，时间都是手工切割的。就很笨。

简单改一下就可以只算用户在2016-01-01当天的总MCI（基于全天总24小时）
然后生成了user_1day_mci.csv 这个数据集是1day_mci_clustering.py用到的数据集
'''

import pandas as pd

df_day = pd.read_csv("day_usage.csv")
df_night = pd.read_csv("night_usage.csv")

# 去除时区
# df1['localminute'] = df1['localminute'].map(lambda x: str(x)[:-3])

# str时间数据转换为时间戳
df_night['minute'] = pd.to_datetime(df_night['minute'])
df_night.set_index("minute", inplace=True)
df_night.sort_index(inplace=True)

df_day['minute'] = pd.to_datetime(df_day['minute'])
df_day.set_index("minute", inplace=True)
df_day.sort_index(inplace=True)


print(df_day.head())

print(df_night.head())

# print("1-Minute total electricity consumption: ")
# print(df_1day.resample('1Min').sum())

# print("id = 26 consumer's 1-minute consumption: ")
# print( sum(df_1day[df_1day['dataid'] == 26]['use']) )

A = 0.01
B = 20


def mci(df, user_id):
    return sum((A * (df.resample('1Min').sum())['use'] + B) * df[df['dataid'] == user_id]['use']
               / sum(df[df['dataid'] == user_id]['use']))


ID = df_night['dataid'].value_counts().index

data = pd.DataFrame(columns=('dataid', 'mci_day', 'mci_night','space'))

for user_id in ID:

    data = data.append(pd.DataFrame({
        'dataid': [user_id],
        'mci_day': [mci(df_day, user_id)],
        'mci_night': [mci(df_night, user_id)],
        'space': [0]
    }))

data.to_csv('user_day_night_mci.csv')
