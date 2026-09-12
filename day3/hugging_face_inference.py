# keep HF_TOKEN in .env file
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

client = InferenceClient()

response = client.chat_completion(
    model="meta-llama/Llama-3.3-70B-Instruct",
    messages=[
        {"role": "user", "content": "tell me about Spark"}
    ],
    max_tokens=20
)

print(response.choices[0].message.content)
