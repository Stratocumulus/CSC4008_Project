'''
计算总数据集里每个用户的数据记录数量
'''

import pandas as pd

# read in dataset
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

# print(df1.head())
# print(df1['dataid'].value_counts())

# count number of costumers
df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11])

df.to_csv("user_total_counts.txt")

# 调出某个用户的数据
'''
df['localminute'] = df['localminute'].map(lambda x: str(x)[:-3])
df['localminute'] = pd.to_datetime(df['localminute'], format='%Y-%m-%d %H:%M')
df.set_index("localminute", inplace=True)

df = df["2016-01-01":"2016-04-29"]

count = df[df['dataid'] == 4031]
count.to_csv("consumer4031_count.txt")
'''
