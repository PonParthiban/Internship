import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("StudentsPerformance.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())

print(df.duplicated().sum())
df = df.drop_duplicates()

X = df.drop(columns=['math score'])
y = df['math score']
X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

model = DecisionTreeRegressor(max_depth=10)
model.fit(X_train,y_train)

prediction = model.predict(X_test)

mse = mean_squared_error(y_test, prediction)
mae = mean_absolute_error(y_test, prediction)
r2 = r2_score(y_test, prediction)

print(f"mean_squared_error {mse}")
print(f"mean_absolute_error {mae}")
print(f"r2_score {r2}")
