import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

df = pd.read_csv("Mall_Customers.csv")


print(df.head())
print(df.info())
print(df.isnull().sum())

print(df.duplicated().sum())
df = df.drop_duplicates()

x = df.drop(columns=['Genre','CustomerID','Age'])

scaler = StandardScaler()

X = scaler.fit_transform(x)

model = DBSCAN(eps=0.6, min_samples=5)
model.fit(X)

df['Cluster'] = model.labels_
print(df.head())
print(df['Cluster'].value_counts())
score = silhouette_score(X, model.labels_)
print(score)
