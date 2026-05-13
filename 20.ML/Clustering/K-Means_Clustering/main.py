import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv("Mall_Customers.csv")



print(df.head())
print(df.info())
print(df.isnull().sum())

print(df.duplicated().sum())
df = df.drop_duplicates()

x = df.drop(columns=['Genre','CustomerID'])

scaler = StandardScaler()

X = scaler.fit_transform(x)

model = KMeans(n_clusters=5) # 5 is best
model.fit(X)

"""inertia_values = []

for k in range(1, 11):

    model = KMeans(n_clusters=k)
    model.fit(X)

    inertia_values.append(model.inertia_)

print(inertia_values)

plt.plot(range(1, 11), inertia_values)

plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")

plt.title("Elbow Method")

plt.show()"""

df['Cluster'] = model.labels_

print(df.head())
print(model.cluster_centers_)

df.to_csv("clustered_customers.csv", index=False)


