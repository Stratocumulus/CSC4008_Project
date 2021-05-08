'''
计算2016-01-01当天所有用户在24小时时段内的MCI（24个，基于每小时）
连同用户当天总消费存入user_24hours_mci_cleaned.scv

因为只提取一天的数据，时间都是手工切割的。就很笨。

简单改一下就可以只算用户在2016-01-01当天的总MCI（基于全天总24小时）
然后生成了user_1day_mci.csv 这个数据集是1day_mci_clustering.py用到的数据集
'''

import pandas as pd

df1 = pd.read_csv("dataset/pecan_1_min_part1.csv")
df2 = pd.read_csv("dataset/pecan_1_min_part2.csv")
df3 = pd.read_csv("dataset/pecan_1_min_part3.csv")
df4 = pd.read_csv("dataset/pecan_1_min_part4.csv")
df5 = pd.read_csv("dataset/pecan_1_min_part5.csv")
df6 = pd.read_csv("dataset/pecan_1_min_part6.csv")
df7 = pd.read_csv("dataset/pecan_1_min_part7.csv")
df8 = pd.read_csv("dataset/pecan_1_min_part8.csv")
df9 = pd.read_csv("dataset/pecan_1_min_part9.csv")
df10 = pd.read_csv("dataset/pecan_1_min_part10.csv")
df11 = pd.read_csv("dataset/pecan_1_min_part11.csv")

# read in dataset
df1 = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11])

# 去除时区
df1['localminute'] = df1['localminute'].map(lambda x: str(x)[:-3])

# str时间数据转换为时间戳
df1['localminute'] = pd.to_datetime(df1['localminute'], format='%Y-%m-%d %H:%M')
df1.set_index("localminute", inplace=True)

df1.sort_index(inplace=True)

# print("1-Minute total electricity consumption: ")
# print(df_1day.resample('1Min').sum())

# print("id = 26 consumer's 1-minute consumption: ")
# print( sum(df_1day[df_1day['dataid'] == 26]['use']) )

A = 0.01
B = 20

# 切出第一天的数据
# 获取按时间分割的MCI
df_1day = df1['2016-01-01']
df_00 = df1.truncate(before='2016-01-01 00:00:00', after='2016-01-01 01:00:00')
df_01 = df1.truncate(before='2016-01-01 01:00:00', after='2016-01-01 02:00:00')
df_02 = df1.truncate(before='2016-01-01 02:00:00', after='2016-01-01 03:00:00')
df_03 = df1.truncate(before='2016-01-01 03:00:00', after='2016-01-01 04:00:00')
df_04 = df1.truncate(before='2016-01-01 04:00:00', after='2016-01-01 05:00:00')
df_05 = df1.truncate(before='2016-01-01 05:00:00', after='2016-01-01 06:00:00')
df_06 = df1.truncate(before='2016-01-01 06:00:00', after='2016-01-01 07:00:00')
df_07 = df1.truncate(before='2016-01-01 07:00:00', after='2016-01-01 08:00:00')
df_08 = df1.truncate(before='2016-01-01 08:00:00', after='2016-01-01 09:00:00')
df_09 = df1.truncate(before='2016-01-01 09:00:00', after='2016-01-01 10:00:00')
df_10 = df1.truncate(before='2016-01-01 10:00:00', after='2016-01-01 11:00:00')
df_11 = df1.truncate(before='2016-01-01 11:00:00', after='2016-01-01 12:00:00')
df_12 = df1.truncate(before='2016-01-01 12:00:00', after='2016-01-01 13:00:00')
df_13 = df1.truncate(before='2016-01-01 13:00:00', after='2016-01-01 14:00:00')
df_14 = df1.truncate(before='2016-01-01 14:00:00', after='2016-01-01 15:00:00')
df_15 = df1.truncate(before='2016-01-01 15:00:00', after='2016-01-01 16:00:00')
df_16 = df1.truncate(before='2016-01-01 16:00:00', after='2016-01-01 17:00:00')
df_17 = df1.truncate(before='2016-01-01 17:00:00', after='2016-01-01 18:00:00')
df_18 = df1.truncate(before='2016-01-01 18:00:00', after='2016-01-01 19:00:00')
df_19 = df1.truncate(before='2016-01-01 19:00:00', after='2016-01-01 20:00:00')
df_20 = df1.truncate(before='2016-01-01 20:00:00', after='2016-01-01 21:00:00')
df_21 = df1.truncate(before='2016-01-01 21:00:00', after='2016-01-01 22:00:00')
df_22 = df1.truncate(before='2016-01-01 22:00:00', after='2016-01-01 23:00:00')
df_23 = df1.truncate(before='2016-01-01 23:00:00', after='2016-01-02 00:00:00')

ID = df_1day['dataid'].value_counts().index
data = pd.DataFrame(columns=('dataid', 'total_consumption', 'mci_00',
                             'mci_01', 'mci_02', 'mci_03', 'mci_04',
                             'mci_05', 'mci_06', 'mci_07', 'mci_08',
                             'mci_09', 'mci_10', 'mci_11', 'mci_12',
                             'mci_13', 'mci_14', 'mci_15', 'mci_16',
                             'mci_17', 'mci_18', 'mci_19', 'mci_20',
                             'mci_21', 'mci_22', 'mci_23'))


def mci(df, user_id):
    return sum((A * (df.resample('1Min').sum())['use'] + B) * df[df['dataid'] == user_id]['use']
               / sum(df[df['dataid'] == user_id]['use']))


for user_id in ID:
    '''
    print("User ID is: ")
    print(user_id)

    print("User daily consumption is: ")
    print(sum(df_1day[df_1day['dataid'] == user_id]['use']))

    print("User's daily MCI is: ")
    print(sum((A * (df_1day.resample('1Min').sum())['use'] + B) * df_1day[df_1day['dataid'] == user_id]['use']
           / sum(df_1day[df_1day['dataid'] == user_id]['use']) ) )

    print("*" * 20)
    '''

    consumption = sum(df_1day[df_1day['dataid'] == user_id]['use'])

    data = data.append(pd.DataFrame({
        'dataid': [user_id],
        'total_consumption': [consumption],
        'mci_00': [mci(df_00, user_id)],
        'mci_01': [mci(df_01, user_id)],
        'mci_02': [mci(df_02, user_id)],
        'mci_03': [mci(df_03, user_id)],
        'mci_04': [mci(df_04, user_id)],
        'mci_05': [mci(df_05, user_id)],
        'mci_06': [mci(df_06, user_id)],
        'mci_07': [mci(df_07, user_id)],
        'mci_08': [mci(df_08, user_id)],
        'mci_09': [mci(df_09, user_id)],
        'mci_10': [mci(df_10, user_id)],
        'mci_11': [mci(df_11, user_id)],
        'mci_12': [mci(df_12, user_id)],
        'mci_13': [mci(df_13, user_id)],
        'mci_14': [mci(df_14, user_id)],
        'mci_15': [mci(df_15, user_id)],
        'mci_16': [mci(df_16, user_id)],
        'mci_17': [mci(df_17, user_id)],
        'mci_18': [mci(df_18, user_id)],
        'mci_19': [mci(df_19, user_id)],
        'mci_20': [mci(df_20, user_id)],
        'mci_21': [mci(df_21, user_id)],
        'mci_22': [mci(df_22, user_id)],
        'mci_23': [mci(df_23, user_id)],
    }))

data.to_csv('user_24hours_mci.csv')
