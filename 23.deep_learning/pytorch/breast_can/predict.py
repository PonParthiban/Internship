import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class CancerNN(nn.Module):
 
    def __init__(self):
        super().__init__()

        self.fc1 = nn.Linear(30, 16)
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)

    def forward(self, x):

        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))

        return x

model = CancerNN()

model.load_state_dict(torch.load("cancer_model.pth"))

model.eval()

sample = torch.tensor(X_test[:5], dtype=torch.float32)

with torch.no_grad():

    predictions = model(sample)

    predictions = (predictions > 0.5).float()

print(predictions)
