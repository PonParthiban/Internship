import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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

X_train,X_val,y_train,y_val = train_test_split(X_train,y_train,test_size=0.2,random_state=42,stratify=y_train)

# Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
X_val = scaler.transform(X_val)

# Convert to tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
X_val = torch.tensor(X_val, dtype=torch.float32)

y_train = torch.tensor(y_train.values, dtype=torch.float32).view(-1,1)
y_test = torch.tensor(y_test.values, dtype=torch.float32).view(-1,1)
y_val = torch.tensor(y_val.values, dtype=torch.float32).view(-1,1)


train_dataset = TensorDataset(X_train, y_train)

val_dataset = TensorDataset(X_val, y_val)

train_data = DataLoader(
              train_dataset,
              batch_size=32,
              shuffle=True
)

val_data = DataLoader(
              val_dataset,
              batch_size=32,
              shuffle=False
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

for epoch in range(100):

    # TRAINING
    model.train()

    train_loss = 0

    for X_batch, y_batch in train_data:

        outputs = model(X_batch)

        loss = criterion(outputs, y_batch)

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        train_loss += loss.item()

    train_loss /= len(train_data)

    # VALIDATION
    model.eval()

    val_loss = 0

    with torch.no_grad():

        for X_batch, y_batch in val_data:

            outputs = model(X_batch)

            v_loss = criterion(outputs, y_batch)

            val_loss += v_loss.item()

    val_loss /= len(val_data)

    if epoch % 10 == 0:
        print(
            f"Epoch {epoch}, "
            f"Train Loss: {train_loss:.4f}, "
            f"Val Loss: {val_loss:.4f}"
        )

model.eval()

# Predictions
with torch.no_grad():

    predictions = model(X_test)

    predictions = (predictions > 0.5).float()



accuracy = accuracy_score(y_test.numpy(),predictions.numpy())
classif = classification_report(y_test.numpy(),predictions.numpy())
confuse = confusion_matrix(y_test.numpy(),predictions.numpy())

print(f"Accuracy: {accuracy}")
print(f"classification report: {classif}")
print(f"confuse matrix: {confuse}")

torch.save(model.state_dict(), "cancer_model.pth")#state_dict() -> all learned weights and biases

