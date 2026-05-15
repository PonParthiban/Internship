import torch
import torch.nn as nn

from torchvision import transforms, models
from PIL import Image

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = models.resnet18(pretrained=False)

model.fc = nn.Linear(model.fc.in_features, 2)

model.load_state_dict(
    torch.load("cats_vs_dogs.pth")
)

model.to(device)

model.eval()

transform = transforms.Compose([

    transforms.Resize((224,224)),

    transforms.ToTensor()

])

image = Image.open("data1/test/Dog/10003.jpg")

image = image.convert("RGB")

image = transform(image)

image = image.unsqueeze(0)#Adds dimension.

image = image.to(device)

with torch.no_grad():

    outputs = model(image)

    _, predicted = torch.max(outputs, 1)

classes = ["Cat", "Dog"]

print(classes[predicted.item()])