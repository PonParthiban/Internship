import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


df = pd.read_csv("heart.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())

"""print(df.duplicated().sum())"""
df = df.drop_duplicates()

X = df[['age','sex','chol','trestbps','fbs','restecg','thalach','exang','oldpeak']]
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42, stratify=y)

model = DecisionTreeClassifier(max_depth=10)
model.fit(X_train,y_train)

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)
classif = classification_report(y_test, prediction)
confuse = confusion_matrix(y_test, prediction)

print(f"Accuracy: {accuracy}")
print(f"classification report: {classif}")
print(f"confuse matrix: {confuse}")
print(model.get_depth())
print(model.get_n_leaves())