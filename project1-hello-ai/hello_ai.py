#Basic Proj  send Message to an openai model and get response
#python hello_ai.py

#.env file

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI #official openai python library

# load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# safety check for api key
if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file")
    print("Please do these steps")
    print("copy .env.example to a new .env file")
    print("Get your API key from https://platform.openai.com/api-keys")
    print("Paste your API key into the .env file")
    sys.exit(1)

print("API key loaded successfully!")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Define message to send
my_question = "Hello! explain DevOps with AI in 2 Sentences, like I'm 10 years old"

model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

#print a status message
print("\n\nSending message to OpenAI...")
print("Your question:", my_question)
print(f"Model: {model}")

# send message and get response
response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": my_question
        }
    ],
    max_tokens=300,
)

# extract the response text
answer_text = response.choices[0].message.content

# print the response
print("\n\nAI Response:")
print("--------------------------------------------------")
print(answer_text)
print("--------------------------------------------------")

# show token usage 
print("\nToken Usage:")
if response.usage:
    print(f"Input tokens: {response.usage.prompt_tokens}")
    print(f"Output tokens: {response.usage.completion_tokens}")
    print(f"Total tokens: {response.usage.total_tokens}")
else:
    print("Token usage not available")

print("\Done! Your first AI call was a success!")    