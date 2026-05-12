import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
df = pd.read_csv("data.csv")
from sklearn.decomposition import PCA

print(df.head())
print(df.info())
print(df.isnull().sum())

print(df.duplicated().sum())
df = df.drop_duplicates()

X = df.drop(columns=['id', 'Unnamed: 32', 'diagnosis'])
y = df['diagnosis']
y = y.map({
    'B':0,
    'M':1
})

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

pca = PCA(n_components=10)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

model = SVC(kernel='linear')
model.fit(X_train_pca,y_train)

prediction = model.predict(X_test_pca)

accuracy = accuracy_score(y_test, prediction)
classif = classification_report(y_test, prediction)
confuse = confusion_matrix(y_test, prediction)

print(f"Accuracy: {accuracy}")
print(f"classification report: {classif}")
print(f"confuse matrix: {confuse}")
print(pca.explained_variance_ratio_)