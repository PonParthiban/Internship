import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_transform = transforms.Compose([
                 transforms.RandomRotation(10),
                 transforms.ToTensor()
                 
])

test_transform = transforms.Compose([
                 transforms.ToTensor()
                 
])

full_train   = datasets.MNIST(root="./data", train=True,  download=True, transform=train_transform)
test_dataset = datasets.MNIST(root="./data", train=False, download=True, transform=test_transform)

# Split 80% train, 20% val
val_size     = int(0.2 * len(full_train))
train_size   = len(full_train) - val_size
train_dataset, val_dataset = random_split(full_train, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_dataset,   batch_size=32, shuffle=False)
test_loader  = DataLoader(test_dataset,  batch_size=32, shuffle=False)

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1   = nn.Conv2d(1, 32, 3, padding=1)
        self.bn1     = nn.BatchNorm2d(32)
        self.conv2   = nn.Conv2d(32, 64, 3, padding=1)
        self.bn2     = nn.BatchNorm2d(64)
        self.pool    = nn.MaxPool2d(2)
        self.fc1     = nn.Linear(64 * 14 * 14, 128)
        self.dropout = nn.Dropout(0.5)
        self.fc2     = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.bn1(self.conv1(x)))
        x = torch.relu(self.bn2(self.conv2(x)))
        x = self.pool(x)
        x = torch.flatten(x, 1)
        x = self.dropout(torch.relu(self.fc1(x)))
        return self.fc2(x)

model     = CNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(5):

    # ── Training ──────────────────────────────────
    model.train()
    train_loss = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss    = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()

    train_loss /= len(train_loader)

    # ── Validation ────────────────────────────────
    model.eval()
    val_loss = 0
    correct  = 0
    total    = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs  = model(images)
            val_loss += criterion(outputs, labels).item()
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total   += labels.size(0)

    val_loss /= len(val_loader)
    val_acc   = 100 * correct / total

    print(f"Epoch {epoch+1} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")

# ── Test ──────────────────────────────────────────
model.eval()
correct = 0
total   = 0

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        correct += (predicted == labels).sum().item()
        total   += labels.size(0)

print(f"Test Accuracy: {100 * correct / total:.2f}%")

"""(32,1,28,28)

↓ Conv

(32,32,28,28)

↓ Conv

(32,64,28,28)

↓ Pool

(32,64,14,14)

↓ Flatten

(32,12544)

↓ FC1

(32,128)

↓ FC2

(32,10)"""