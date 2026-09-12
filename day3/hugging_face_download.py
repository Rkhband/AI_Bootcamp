import os
from dotenv import load_dotenv
load_dotenv()

os.environ['HF_HOME'] = '/Users/ankitbansal/Desktop/huggingface_llama_cache/'

from transformers import pipeline

model = pipeline(
    "text-generation",
    model="meta-llama/Llama-3.2-1B"
)

result = model(
    "what is spark ",
    max_new_tokens=20
)

print(result[0]["generated_text"])
