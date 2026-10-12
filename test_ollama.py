
import ollama

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain RAG in one simple sentence."
        }
    ],
)

print(response["message"]["content"])
