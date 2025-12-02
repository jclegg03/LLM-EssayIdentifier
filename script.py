import time
import pandas as pd
import argparse
from openai import OpenAI
from prompt_reader import load_prompts

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate essays from prompts with rate limiting and crash safety.")
parser.add_argument("--essays-per-prompt", type=int, default=1, help="Number of essays to generate per prompt (default: 1)")
args = parser.parse_args()

# Read API key
with open("ChatAPI.txt", "r", encoding="utf-8") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

prompts = load_prompts()


existing_data = []
try:
    existing_df = pd.read_csv("essays.csv")
    existing_data = existing_df.to_dict(orient="records")
    print(f"# Loaded {len(existing_data)} existing essays from essays.csv")
except Exception as e:
    print(f"!! Could not read existing essays.csv: {e}")

data = existing_data.copy()

batch_start_time = None
call_count = 0

try:
    for prompt_index, prompt in enumerate(prompts, 1):
        for essay_num in range(1, args.essays_per_prompt + 1):
            # Start timing for batch of 3 API calls
            # if call_count % 3 == 0:
            #     batch_start_time = time.time()

            print(f"Generating essay {essay_num}/{args.essays_per_prompt} for prompt {prompt_index}/{len(prompts)}...")

            # API call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # or gpt-4o/gpt-5 if available
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.8
            )

            essay = response.choices[0].message.content.strip()
            data.append({"prompt": prompt, "essay": essay})

            call_count += 1

            # 5-second delay between calls
            # time.sleep(5)

            # After every 3 calls or at the end, save progress and enforce 61-second window
            if call_count % 3 == 0 or (prompt_index == len(prompts) and essay_num == args.essays_per_prompt):
                df = pd.DataFrame(data)
                df.to_csv("essays.csv", index=False)
                print(f"# Progress saved after {call_count} API calls.")

                # elapsed = time.time() - batch_start_time
                # if elapsed < 61:
                #     wait_time = 61 - elapsed
                #     print(f"... Waiting {wait_time:.1f} seconds to respect rate limits...")
                #     time.sleep(wait_time)

    print("# All essays generated and saved to essays.csv")
except Exception as e:
    df = pd.DataFrame(data)
    df.to_csv("essays.csv", index=False)
    print("There was an error")
    print(e)