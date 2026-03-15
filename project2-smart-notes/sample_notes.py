#subscribe to my youtube channel
#realtime projects -- reach -- goal
# done alot of research

#openapi 
#groq -- https://console.groq.com/keys


import os
import sys
import argparse

from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI # the opeenAI-compatible library - works with groq too

# Step - 1: load the environment variables from .env file
load_dotenv() # read the .env file and load the variables into the environment

api_key = os.getenv("GROQ_API_KEY") # get the API key from the environment variable

if not api_key: # safety check
    print("Error: GROQ_API_KEY not found in .env file")
    print("Please create .env file with your key")
    print("get your free key at: https://console.groq.com/keys")

    sys.exit(1) # exit

# step -2: Setup commandlline argumen parsing
# argparse which will uses to manage program arguments from terminal  using flags
# --text "some txt"
# --file "path/to/file.txt"
# --output "path/to/output.txt"
# --model "llama-3.1-8b-instant"

parser = argparse.ArgumentParser(
    description="Smart Notes AI - AI-powered note summarization and organization"
)

parser.add_argument(
    "--text",
    type=str,
    help="Text to summarize",
    default=None    
)

parser.add_argument(
    "--file",
    type=str,
    help="Path to the file containing text to summarize",
    default=None
)

parser.add_argument(
    "--output",
    type=str,
    help="Path to save the summary output",
    default=None
)

args = parser.parse_args()  # parse the arguments

# Step -3 : Get the text to summarize

if args.text:
    input_text = args.text
    print(f"summarizinfg text: '{input_text[:60]}...") # preview first 60 characters, slicing.

elif args.file:
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1) # exit

    with open(args.file, "r", encoding="utf-8") as f:
        input_text = f.read()
        print(f"summarizing text from file: '{args.file} ({len(input_text)} chars)")

else:
    print("Error: No text or file provided.")
    print("Please type or paste your text below")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    input_text = "\n".join(lines)
    print(f"summarizing {len(input_text)} characters")

if not input_text or input_text.strip() == "":
    print("Error: No text provided for summarization")
    sys.exit(1) # exit

# Step -4: Setup the Groq client

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1" # this is the base url for groq's openai-compatible api
)

# Step -5: Define the summarization prompt

system_prompt = """You are an expert AI assistant that summarizes text. Your goal is to create concise, clear, and accurate summaries of the text provided by the user.

Rules:
1. Identify the main ideas and key points of the text.
2. Remove redundant information, examples, and filler content.
3. Keep the summary objective and neutral in tone.
4. Maintain the original meaning and context of the text.
5. Output the summary in clear, well-structured sentences.
6. The summary should be approximately 20-30% of the original text length.
7. If the text is very short (less than 100 words), provide a summary that captures all essential information.
8. If the text is very long (more than 1000 words), create a comprehensive summary that covers all main sections.
9. Use bullet points for lists or key takeaways when appropriate.
10. Do not add personal opinions or information not present in the original text.
11. Do not include any introductory or concluding phrases like "Here is the summary" or "In conclusion".
12. Just provide the summary text itself.
"""

# Step -6: Build the user messsage

user_message = f"""Please summarize the following text:

{input_text}
"""

# step 7 sent to Groq and get the summary
model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant") # get the model from the environment variable, default to llama-3.1-8b-instant

print(f"\nUsing model: {model}")
print("Generating summary...")

response = client.chat.completions.create(
    model=model,
    max_tokens=1024,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
)

summary_text = response.choices[0].message.content 

# step 8 Print the summary
print("\n" + "="*60)
print("SMART SUMMARY")
print("="*60)
print(summary_text)
print("="*60)

print(f"\nTokens used: {response.usage.prompt_tokens} input, {response.usage.completion_tokens} output")

# step 9: Save the output to a file (optional)

if args.output:
    output_content = f"""# Smart Summary
# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Model: {model}
# Input: {args.file if args.file else 'Direct Input'}
S
{summary_text}
"""
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output_content)
    print(f"\nSummary saved to: {args.output}")

print("\nDone!")