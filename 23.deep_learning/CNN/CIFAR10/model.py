import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor()
])

val_transform = transforms.Compose([
    transforms.ToTensor()
])

test_transform = transforms.Compose([
    transforms.ToTensor()
])

full_train   = datasets.CIFAR10(root="./data", train=True,  download=True, transform=train_transform)
test_dataset = datasets.CIFAR10(root="./data", train=False, download=True, transform=test_transform)

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
        self.conv1   = nn.Conv2d(3, 32, 3, padding=1)
        self.bn1     = nn.BatchNorm2d(32)
        self.conv2   = nn.Conv2d(32, 64, 3, padding=1)
        self.bn2     = nn.BatchNorm2d(64)#(32,64,32,32)
        #(32,64,16,16)

        self.conv3   = nn.Conv2d(64, 128, 3, padding=1)
        self.bn3     = nn.BatchNorm2d(128)
        self.conv4   = nn.Conv2d(128, 128, 3, padding=1)
        self.bn4     = nn.BatchNorm2d(128)#(32,128,16,16)
        #(32,128,8,8)

        self.conv5   = nn.Conv2d(128, 256, 3, padding=1)
        self.bn5     = nn.BatchNorm2d(256)
        self.conv6   = nn.Conv2d(256, 256, 3, padding=1)
        self.bn6     = nn.BatchNorm2d(256)#(32,256,8,8)

        self.pool    = nn.MaxPool2d(2)#(32,256,4,4)

        self.fc1     = nn.Linear(4096, 128)#256 × 4 × 4 = 4096
        self.dropout = nn.Dropout(0.5)
        self.fc2     = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.bn1(self.conv1(x)))
        x = torch.relu(self.bn2(self.conv2(x)))
        x = self.pool(x)

        x = torch.relu(self.bn3(self.conv3(x)))
        x = torch.relu(self.bn4(self.conv4(x)))
        x = self.pool(x)

        x = torch.relu(self.bn5(self.conv5(x)))
        x = torch.relu(self.bn6(self.conv6(x)))
        x = self.pool(x)

        x = torch.flatten(x, 1)
        x = self.dropout(torch.relu(self.fc1(x)))
        return self.fc2(x)
    

model     = CNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = StepLR(
    optimizer,
    step_size=10,
    gamma=0.1
)

for epoch in range(30):

    # ── Training ──────────────────────────────────
    model.train()

    train_loss = 0
    correct = 0
    total = 0

    for images, labels in train_loader:

        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        train_loss += loss.item()

        # predictions
        _, predicted = torch.max(outputs, 1)

        # count correct
        correct += (predicted == labels).sum().item()

        # total samples
        total += labels.size(0)
        
        
    train_loss /= len(train_loader)

    train_acc = 100 * correct / total


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
    current_lr = optimizer.param_groups[0]['lr']

    print(
        f"Epoch {epoch+1} | "
        f"Train Loss: {train_loss:.4f} | "
        f"Train Acc: {train_acc:.2f}% | "
        f"Val Loss: {val_loss:.4f} | "
        f"Val Acc: {val_acc:.2f}% | "
        f"LR: {current_lr}"
    )
    scheduler.step()

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