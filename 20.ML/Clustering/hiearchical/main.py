from sklearn.cluster import AgglomerativeClustering
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage

df = pd.read_csv("Mall_Customers.csv")


print(df.head())
print(df.info())
print(df.isnull().sum())

print(df.duplicated().sum())
df = df.drop_duplicates()

x = df.drop(columns=['Genre','CustomerID','Age'])

scaler = StandardScaler()

X = scaler.fit_transform(x)

linked = linkage(X, method='ward') #This computes: hierarchical merge structure

model = AgglomerativeClustering(n_clusters=5,linkage='ward')
model.fit(X)

plt.figure(figsize=(10, 5))

dendrogram(linked)

plt.title("Dendrogram")
plt.xlabel("Data Points")
plt.ylabel("Distance")

plt.show()

df['Cluster'] = model.labels_
print(df.head())
print(df['Cluster'].value_counts())
score = silhouette_score(X, model.labels_)
print(score)