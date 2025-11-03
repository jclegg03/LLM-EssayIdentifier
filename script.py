from openai import OpenAI
import pandas as pd

client = OpenAI()

prompts = [
    "Write a 300-word essay about the importance of curiosity in science.",
    "Discuss the role of social media in modern political movements.",
    "Explain how urbanization affects biodiversity."
]

data = []

for i, prompt in enumerate(prompts, 1):
    print(f"Generating essay {i}/{len(prompts)}...")
    
    response = client.chat.completions.create(
        model="gpt-5",  # You can use gpt-4o or gpt-5 depending on access
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