import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("Mall_Customers.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())

print(df.duplicated().sum())
df = df.drop_duplicates()

x = df.drop(columns=['Genre','CustomerID'])

scaler = StandardScaler()

X = scaler.fit_transform(x)

model = KMeans(n_clusters=3)
model.fit(X)

print(model.labels_)
print(model.cluster_centers_)


