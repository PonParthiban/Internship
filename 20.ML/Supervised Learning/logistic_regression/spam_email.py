import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from string import punctuation

df = pd.read_csv("spam.csv",     
                 sep='\t',
                 header=None,
                 names=['label', 'message'])
print(df.info())
print(df.isnull().sum())
print(df['label'].value_counts())

def data_clean(text):
    text = text.lower()
    result = ""
    # Remove punctuation
    for char in text:
        if char not in punctuation:
            result += char
    # Remove extra whitespaces
    result = " ".join(result.split())
    return result

df['label'] = df['label'].map({
    'ham':0,
    'spam':1
})

df['message'] = df['message'].apply(data_clean)

X = df['message']
y = df['label']

print(df.head())

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42, stratify=y)

vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)
classif = classification_report(y_test, prediction)
confuse = confusion_matrix(y_test, prediction)

print(f"Accuracy: {accuracy}")
print(f"classification report: {classif}")
print(f"confuse matrix: {confuse}")

