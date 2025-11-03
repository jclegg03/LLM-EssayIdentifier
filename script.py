from openai import OpenAI
import pandas as pd
from prompt_reader import load_prompts

with open("ChatAPI.txt", "r", encoding="utf-8") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

prompts = load_prompts()

data = []

for i, prompt in enumerate(prompts, 1):
    print(f"Generating essay {i}/{len(prompts)}...")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use gpt-4o or gpt-5 depending on access
        messages=[
            {"role": "system", "content": "You are an expert essay writer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,  # Control essay length
        temperature=0.8  # Control creativity
    )

    essay = response.choices[0].message.content.strip()
    data.append({"prompt": prompt, "essay": essay})

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("essays.csv", index=False)

print("✅ Dataset saved to essays.csv")