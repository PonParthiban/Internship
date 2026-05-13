import torch

x = torch.tensor(2.0, requires_grad=True)#Track operations on this tensor

y = x**2

y.backward()#backpropagation

print(x.grad)