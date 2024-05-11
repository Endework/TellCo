import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Add the
def analyze_data(df):
    # Task 3.1
    df['TCP DL Retrans. Vol (Bytes)'] = df['TCP DL Retrans. Vol (Bytes)'].fillna(df['TCP DL Retrans. Vol (Bytes)'].mean())
    df['Avg RTT DL (ms)'] = df['Avg RTT DL (ms)'].fillna(df['Avg RTT DL (ms)'].mean())
    df['Avg Bearer TP DL (kbps)'] = df['Avg Bearer TP DL (kbps)'].fillna(df['Avg Bearer TP DL (kbps)'].mean())
    df['Handset Type'] = df['Handset Type'].fillna(df['Handset Type'].mode()[0])

    agg_df = df.groupby('MSISDN/Number').agg({
        'TCP DL Retrans. Vol (Bytes)': 'mean',
        'Avg RTT DL (ms)': 'mean',
        'Handset Type': lambda x: x.mode()[0] if not x.empty else 'Unknown',
        'Avg Bearer TP DL (kbps)': 'mean'
    })

    # Task 3.2
    top_10_tcp = df['TCP DL Retrans. Vol (Bytes)'].nlargest(10)
    bottom_10_tcp = df['TCP DL Retrans. Vol (Bytes)'].nsmallest(10)
    freq_10_tcp = df['TCP DL Retrans. Vol (Bytes)'].value_counts().nlargest(10)

    top_10_rtt = df['Avg RTT DL (ms)'].nlargest(10)
    bottom_10_rtt = df['Avg RTT DL (ms)'].nsmallest(10)
    freq_10_rtt = df['Avg RTT DL (ms)'].value_counts().nlargest(10)

    top_10_throughput = df['Avg Bearer TP DL (kbps)'].nlargest(10)
    bottom_10_throughput = df['Avg Bearer TP DL (kbps)'].nsmallest(10)
    freq_10_throughput = df['Avg Bearer TP DL (kbps)'].value_counts().nlargest(10)

    # Task 3.3
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Handset Type', y='Avg Bearer TP DL (kbps)', data=df)
    plt.title('Distribution of Average Throughput per Handset Type')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Handset Type', y='TCP DL Retrans. Vol (Bytes)', data=df)
    plt.title('Average TCP Retransmission per Handset Type')
    plt.show()

    # Task 3.4
    features = df[['TCP DL Retrans. Vol (Bytes)', 
    'Avg RTT DL (ms)', 
    'Avg Bearer TP DL (kbps)',
    'Avg RTT UL (ms)',
    'TCP UL Retrans. Vol (Bytes)',
    'Avg Bearer TP UL (kbps)']]
    kmeans = KMeans(n_clusters=3, random_state=0).fit(features)
    df['Cluster'] = kmeans.labels_
    np.save(r'C:\Users\ende\Desktop\10x\Week-2\less_engaged_centroid.npy', kmeans.cluster_centers_[0])
    np.save(r'C:\Users\ende\Desktop\10x\Week-2\worst_experience_centroid.npy', kmeans.cluster_centers_[1])

    return df
