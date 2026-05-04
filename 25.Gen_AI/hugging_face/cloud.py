from huggingface_hub import InferenceClient

client = InferenceClient(model="gpt2")

result = client.text_generation("AI is", max_new_tokens=20)
print(result)