import torch
from model import CancerNN

print(torch.cuda.is_available())

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

model = CancerNN().to(device)