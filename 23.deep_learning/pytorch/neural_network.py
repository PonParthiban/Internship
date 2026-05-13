import torch
import torch.nn as nn
import torch.optim as optim

# Input data
X = torch.tensor([
    [1.0, 2.0],
    [2.0, 3.0],
    [3.0, 4.0],
    [4.0, 5.0]
])

# Target output
y = torch.tensor([
    [0.0],
    [0.0],
    [1.0],
    [1.0]
])

# Neural Network
class SimpleNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.fc1 = nn.Linear(2, 4)
        self.fc2 = nn.Linear(4, 1)

    def forward(self, x):

        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))

        return x

# Create model
model = SimpleNN()

# Loss function
criterion = nn.BCELoss()

# Optimizer
optimizer = optim.Adam(model.parameters(), lr=0.01)#Learning rate

# Training loop
for epoch in range(1000):

    # Forward propagation
    outputs = model(X)

    # Calculate loss
    loss = criterion(outputs, y)

    # Clear old gradients
    optimizer.zero_grad()#it resets

    # Backpropagation
    loss.backward()

    # Update weights
    optimizer.step()#update weights

    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item()}")

# Final predictions
print(model(X))






"""import torch
import torch.nn as nn #this is how we define the neural network

class SimpleNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.fc1 = nn.Linear(2, 4)#layer:2 inputs → 4 neurons
        self.fc2 = nn.Linear(4, 1)

    def forward(self, x):#forward propagation

        x = torch.relu(self.fc1(x))
        x = self.fc2(x)

        return x
    
model = SimpleNN()
x = torch.tensor([[1.0, 2.0]])
output = model(x)

print(output)"""