import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data.csv")

# Remove duplicates
df = df.drop_duplicates()

# Features and labels
X = df.drop(columns=['id', 'Unnamed: 32', 'diagnosis'])

y = df['diagnosis'].map({
    'B':0,
    'M':1
})

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert to tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)

y_train = torch.tensor(y_train.values, dtype=torch.float32).view(-1,1)
y_test = torch.tensor(y_test.values, dtype=torch.float32).view(-1,1)

tensor_data = DataLoader(
              X_train,y_train,
              batch_size=32,
              suffle=True
)

# Neural Network
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

# Create model
model = CancerNN()

# Loss function
criterion = nn.BCELoss()

# Optimizer
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(1000):

    # Forward propagation
    outputs = model(X_train)

    # Loss
    loss = criterion(outputs, y_train)

    # Clear old gradients
    optimizer.zero_grad()

    # Backpropagation
    loss.backward()

    # Update weights
    optimizer.step()

    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item()}")

# Predictions
with torch.no_grad():

    predictions = model(X_test)

    predictions = (predictions > 0.5).float()

print(predictions)

# Accuracy
accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Accuracy: {accuracy}")