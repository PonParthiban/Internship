import torch

"""#x = torch.tensor([1, 2, 3])
x = torch.tensor([
    [1, 2],
    [3, 4]
])

print(x)
print(x.shape)
print(x.dtype)"""

x = torch.tensor([1, 2, 3])
y = torch.tensor([4, 5, 6])

print(x + y)

print(x * y)

a = torch.tensor([
    [1, 2],
    [3, 4]
])

b = torch.tensor([
    [5, 6],
    [7, 8]
])

print(torch.matmul(a, b))

#Tensor reshaping
z = torch.tensor([1,2,3,4])

print(z.reshape(2,2))