from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

result = generator(
    "Explain AI in simple terms:",
    max_new_tokens=50,
    do_sample=True,
    temperature=0.7
)

print(result[0]["generated_text"])