from huggingface_hub import InferenceClient

client = InferenceClient(model="gpt2")

result = client.text_generation("AI is", max_new_tokens=20)
print(result)

"""import torch

x = torch.tensor([1, 2, 3])
print(x)
print(x.shape)

import torch

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x * 2
print(y)"""