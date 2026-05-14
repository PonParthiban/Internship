from model import CancerNN

import pandas as pd
import torch

from sklearn.preprocessing import StandardScaler

model = CancerNN()

model.load_state_dict(
    torch.load("cancer_model.pth")
)
model.eval()
df = pd.read_csv("data.csv")
X = df.drop(
    columns=['id', 'Unnamed: 32', 'diagnosis']
)
scaler = StandardScaler()

X = scaler.fit_transform(X)
X = torch.tensor(X, dtype=torch.float32)
sample = X[:5]
with torch.no_grad():

    predictions = model(sample)

    predictions = (predictions > 0.5).float()


print(predictions)