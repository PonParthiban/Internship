import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader

from torchvision import datasets, transforms

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

print(device)
transform = transforms.ToTensor()#PIL image → PyTorch tensor

train_dataset = datasets.MNIST(
    root="./data",
    train=True,
    download=True,
    transform=transform
)

test_dataset = datasets.MNIST(
    root="./data",
    train=False,
    download=True,
    transform=transform
)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False
)

class CNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)

        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)

        self.pool = nn.MaxPool2d(2)

        self.fc1 = nn.Linear(64 * 14 * 14, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):

        x = torch.relu(self.conv1(x))
        print(x.shape)

        x = torch.relu(self.conv2(x))
        print(x.shape)

        x = self.pool(x)
        print(x.shape)

        x = torch.flatten(x, 1)
        print(x.shape)

        x = torch.relu(self.fc1(x))
        print(x.shape)

        x = self.fc2(x)
        print(x.shape)

        return x

model = CNN().to(device)

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.001
)

for epoch in range(5):
        model.train()

        train_loss = 0

        for images, labels in train_loader:
                
            images = images.to(device)

            labels = labels.to(device)

            outputs = model(images)

            loss = criterion(outputs, labels)
            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            train_loss += loss.item()

        train_loss /= len(train_loader)
                
        print(
        f"Epoch {epoch+1}, "
        f"Loss: {train_loss:.4f}"
    )
        
model.eval()

correct = 0

total = 0

with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(device)

        labels = labels.to(device)

        outputs = model(images)

        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)

        correct += (
            predicted == labels
        ).sum().item()

accuracy = 100 * correct / total
print(f"Accuracy: {accuracy:.2f}%")

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