import pandas as pd
import argparse
import time
from anthropic import Anthropic
from prompt_reader import load_prompts

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate essays using Claude API with prompt caching and cost tracking.")
parser.add_argument("--essays-per-prompt", type=int, default=500, help="Number of essays to generate per prompt (default: 500)")
parser.add_argument("--model", type=str, default="claude-haiku-4-5-20251001", help="Claude model to use (default: claude-haiku-4-5-20251001)")
parser.add_argument("--temperature", type=float, default=0.8, help="Temperature for generation (default: 0.8)")
args = parser.parse_args()

# Read API key
with open("ClaudeAPI.txt", "r", encoding="utf-8") as f:
    api_key = f.read().strip()

client = Anthropic(api_key=api_key)

prompts = load_prompts()

# Load existing data if available
existing_data = []
try:
    existing_df = pd.read_csv("essays.csv")
    existing_data = existing_df.to_dict(orient="records")
    print(f"# Loaded {len(existing_data)} existing essays from essays.csv")
except Exception as e:
    print(f"!! Could not read existing essays.csv: {e}")

data = existing_data.copy()

# Cost tracking
total_input_tokens = 0
total_output_tokens = 0
total_cache_creation_tokens = 0
total_cache_read_tokens = 0

# Pricing for Haiku 4.5 (per million tokens)
INPUT_COST = 0.25
OUTPUT_COST = 1.25
CACHE_CREATION_COST = 0.3125
CACHE_READ_COST = 0.025

call_count = 0
save_interval = 10  # Save progress every 10 essays

try:
    for prompt_index, prompt in enumerate(prompts, 1):
        print(f"\n{'='*60}")
        print(f"Starting Prompt {prompt_index}/{len(prompts)}")
        print(f"{'='*60}")
        
        for essay_num in range(1, args.essays_per_prompt + 1):
            print(f"Generating essay {essay_num}/{args.essays_per_prompt} for prompt {prompt_index}/{len(prompts)}...", end=" ")

            try:
                # Using prompt caching for the system message
                response = client.messages.create(
                    model=args.model,
                    max_tokens=2000,
                    temperature=args.temperature,
                    system=[
                        {
                            "type": "text",
                            "text": "You are an expert essay writer. Generate high-quality, well-structured essays that vary in style, tone, and approach. Each essay should be unique and demonstrate different writing techniques.",
                            "cache_control": {"type": "ephemeral"}
                        },
                        {
                            "type": "text", 
                            "text": f"Essay prompt: {prompt}",
                            "cache_control": {"type": "ephemeral"}
                        }
                    ],
                    messages=[
                        {"role": "user", "content": "Please write a complete essay responding to the prompt above. Aim for 750-1500 words."}
                    ]
                )

                essay = response.content[0].text.strip()
                data.append({"prompt": prompt, "essay": essay})

                # Track token usage
                usage = response.usage
                total_input_tokens += usage.input_tokens
                total_output_tokens += usage.output_tokens
                
                # Track cache tokens if present
                if hasattr(usage, 'cache_creation_input_tokens') and usage.cache_creation_input_tokens:
                    total_cache_creation_tokens += usage.cache_creation_input_tokens
                if hasattr(usage, 'cache_read_input_tokens') and usage.cache_read_input_tokens:
                    total_cache_read_tokens += usage.cache_read_input_tokens

                call_count += 1
                print("✓")

                # Save progress periodically
                if call_count % save_interval == 0:
                    df = pd.DataFrame(data)
                    df.to_csv("essays.csv", index=False)
                    
                    # Calculate current cost
                    current_cost = (
                        (total_input_tokens / 1_000_000) * INPUT_COST +
                        (total_output_tokens / 1_000_000) * OUTPUT_COST +
                        (total_cache_creation_tokens / 1_000_000) * CACHE_CREATION_COST +
                        (total_cache_read_tokens / 1_000_000) * CACHE_READ_COST
                    )
                    
                    print(f"  → Progress saved! {call_count} essays completed. Cost so far: ${current_cost:.4f}")

                # Small delay to be respectful to API
                time.sleep(0.5)

            except Exception as e:
                print(f"✗ Error: {e}")
                # Save progress even on error
                df = pd.DataFrame(data)
                df.to_csv("essays.csv", index=False)
                print(f"  → Progress saved after error")
                time.sleep(2)  # Wait a bit longer after error
                continue

    # Final save
    df = pd.DataFrame(data)
    df.to_csv("essays.csv", index=False)
    
    # Final cost calculation
    total_cost = (
        (total_input_tokens / 1_000_000) * INPUT_COST +
        (total_output_tokens / 1_000_000) * OUTPUT_COST +
        (total_cache_creation_tokens / 1_000_000) * CACHE_CREATION_COST +
        (total_cache_read_tokens / 1_000_000) * CACHE_READ_COST
    )
    
    print("\n" + "="*60)
    print("GENERATION COMPLETE!")
    print("="*60)
    print(f"Total essays generated: {call_count}")
    print(f"\nToken Usage:")
    print(f"  Input tokens: {total_input_tokens:,}")
    print(f"  Output tokens: {total_output_tokens:,}")
    print(f"  Cache creation tokens: {total_cache_creation_tokens:,}")
    print(f"  Cache read tokens: {total_cache_read_tokens:,}")
    print(f"\nTotal Cost: ${total_cost:.4f}")
    print(f"Average cost per essay: ${total_cost/call_count:.6f}")
    print(f"\nAll essays saved to essays.csv")

except KeyboardInterrupt:
    print("\n\n!! Generation interrupted by user")
    df = pd.DataFrame(data)
    df.to_csv("essays.csv", index=False)
    print(f"  → Progress saved: {len(data)} essays")
except Exception as e:
    print(f"\n\n!! Unexpected error: {e}")
    df = pd.DataFrame(data)
    df.to_csv("essays.csv", index=False)
    print(f"  → Progress saved: {len(data)} essays")
