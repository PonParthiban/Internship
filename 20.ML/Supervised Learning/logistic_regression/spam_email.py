import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("spam.csv",     
                 sep='\t',
                 header=None,
                 names=['label', 'message'])
print(df.head())
print(df.info())
print(df.isnull().sum())
print(df['label'].value_counts())

df['label'] = df['label'].map({
    'ham':0,
    'spam':1
})

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(df['message'])
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

predict = model.predict(X_test)

print(predict)