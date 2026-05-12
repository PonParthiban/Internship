import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("StudentsPerformance.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())

print(df.duplicated().sum())
df = df.drop_duplicates()

X = df.drop(columns=['math score'])
y = df['math score']
X = pd.get_dummies(X)

model = RandomForestRegressor()

param_grid = {
    'max_depth': [3, 5, 10],
    'n_estimators': [50, 100]
}

grid = GridSearchCV(
    model,
    param_grid,
    cv=5
)

grid.fit(X, y)

print(grid.best_params_)
print(grid.best_score_)