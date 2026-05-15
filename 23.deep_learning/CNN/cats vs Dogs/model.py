import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader


train_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor()
])

val_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

test_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

train_dataset = datasets.ImageFolder(
    "data1/train",
    transform=train_transform
)

val_dataset = datasets.ImageFolder(
    "data1/val",
    transform=val_transform
)

test_dataset = datasets.ImageFolder(
    "data1/test",
    transform=test_transform
)


train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False
)


model = models.resnet18(pretrained=True)


for param in model.parameters():
    param.requires_grad = False


model.fc = nn.Linear(model.fc.in_features, 2)


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model.to(device)


criterion = nn.CrossEntropyLoss()


optimizer = optim.Adam(
    model.fc.parameters(),
    lr=0.001
)

for epoch in range(5):

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

    print(
        f"Epoch {epoch+1} | "
        f"Train Loss: {train_loss:.4f} | "
        f"Train Acc: {train_acc:.2f}% | "
        f"Val Loss: {val_loss:.4f} | "
        f"Val Acc: {val_acc:.2f}%"
    )

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

torch.save(model.state_dict(), "cats_vs_dogs.pth")