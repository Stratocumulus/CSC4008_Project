'''
user_1day_mci.csv 中包含了多数用户在2016-01-01当日的日MCI和总用电消费

基于这个数据集（而不是24小时MCI的那个数据集）来进行简单分类
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read in dataset and initializing
user_df = pd.read_csv("user_1day_mci.csv")
user_df = user_df.set_index('dataid')
row_dim = len(user_df)  # amount of users

user_df['cluster'] = range(row_dim)  # the cluster of the user
user_df['link'] = 0  # amount of must links of the user

M = np.zeros([row_dim, row_dim])  # initialize similarity matrix

User_Data = user_df.T.to_dict('list')  # Key: User ID, Value: [total consumption, daily mci, cluster]
User_List = user_df.index  # List of User ID
User_Pos = dict(zip(range(row_dim), User_List))  # Key: 0...row_dim, Value: User ID

# Criteria of Must-Links:
MCI_Bound = 0.05  # if difference of MCI is less than 0.05
Consumption_Bound = 150  # if difference of total daily consumption is less than 150

Link_Bound = 0.7  # after low-rank completion, only links stronger than this value
# is counted as a link

Valid_Sigular_Values = 100  # the desirable rank of similarity matrix

# compute Must-Links
must_pair = 0

for i in range(row_dim):

    ith_user_id = User_Pos[i]
    ith_user_consumption = User_Data[ith_user_id][0]
    ith_user_mci = User_Data[ith_user_id][1]

    for j in range(row_dim):

        if j == i:
            continue

        jth_user_id = User_Pos[j]
        jth_user_consumption = User_Data[jth_user_id][0]
        jth_user_mci = User_Data[jth_user_id][1]

        if abs(ith_user_mci - jth_user_mci) < MCI_Bound:
            if abs(ith_user_consumption - jth_user_consumption) < Consumption_Bound:
                M[i, j] = 1
                must_pair += 1
                user_df.loc[ith_user_id, 'link'] += 1
                user_df.loc[jth_user_id, 'link'] += 1

print(M)
print(np.linalg.matrix_rank(M))  # 240
print(row_dim)  # 337
print(must_pair)  # 1158
print(sum(user_df['link']))  # 2376

# Show the must-links of each user
'''

x = user_df['mci']
y = user_df['total_consumption']
color = user_df['link']

# cmap = plasma, yellow to orange; Oranges: orange to transparent;
plt.scatter(x, y, alpha=0.6, c=color, cmap='plasma')
plt.xlim(23.4, 24.4)
plt.ylim(0, 5000)
plt.grid(c='grey', linestyle='--')
plt.show()
'''

# np.savetxt("similarity_matrix.txt", M)


# Trim sigular values
U, Sigma, V = np.linalg.svd(M)
out = np.trunc(Sigma)
out = out.astype(int)
out[Valid_Sigular_Values:] = 0

Sigma = np.diag(out)
M_hat = (U.dot(Sigma)).dot(V)

print(M_hat.shape)
print(M_hat)
print(np.linalg.matrix_rank(M_hat))

# read cluster information from the similarity matrix
for i in range(row_dim):

    ith_user_id = User_Pos[i]
    ith_user_consumption = User_Data[ith_user_id][0]
    ith_user_mci = User_Data[ith_user_id][1]

    for j in range(row_dim):
        if j == i:
            continue

        jth_user_id = User_Pos[j]
        jth_user_consumption = User_Data[jth_user_id][0]
        jth_user_mci = User_Data[jth_user_id][1]

        if M_hat[i, j] > Link_Bound:
            user_df.loc[jth_user_id, 'cluster'] = user_df.loc[ith_user_id, 'cluster']

# Assign color for each cluster
print(user_df['cluster'].value_counts())

cluster_df = user_df['cluster'].value_counts()
cluster_counts = dict(cluster_df)
cluster_df = pd.DataFrame(cluster_df)
cluster_df['sizerank'] = range(len(cluster_df))

print(cluster_df)

color_list = ["red", "salmon", "chocolate", "orange",
              "yellow", "yellowgreen", "lawngreen", "cyan",
              "deepskyblue", "dodgerblue", "blue", "blueviolet",
              "purple", "fuchsia", "grey"]

for user_id in User_List:
    cluster_id = user_df.loc[user_id, 'cluster']
    cluster_size = cluster_counts[cluster_id]
    cluster_rank = cluster_df.loc[cluster_id, 'sizerank']

    if cluster_size > 3:
        user_df.loc[user_id, 'cluster'] = color_list[min(cluster_rank, len(color_list) - 1)]
    else:
        user_df.loc[user_id, 'cluster'] = 'grey'

# plot the cluster result
x = user_df['mci']
y = user_df['total_consumption']
color = user_df['cluster']

# cmap = plasma, yellow to orange; Oranges: orange to transparent;
plt.scatter(x, y, alpha=0.6, c=color, cmap='Paired')
plt.xlim(23.4, 24.4)
plt.ylim(0, 5000)
plt.grid(c='grey', linestyle='--')
plt.show()
