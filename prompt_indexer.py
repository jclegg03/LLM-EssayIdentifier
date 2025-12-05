import pandas as pd

def compress_dataset(
    input_file="essays.csv",
    output_file="essays.csv",
    encoding_file="prompt_encoding.csv"
):
    """
    Reads essays.csv where each row has columns:
        prompt, essay
    Assigns each unique prompt an integer ID.
    Rewrites essays.csv with columns:
        id, essay
    Writes a second CSV mapping:
        id, prompt
    """

    # Load original data
    df = pd.read_csv(input_file)

    if "prompt" not in df.columns or "essay" not in df.columns:
        raise ValueError("Input CSV must contain 'prompt' and 'essay' columns.")

    # Identify unique prompts and assign IDs
    unique_prompts = df["prompt"].unique()

    prompt_to_id = {prompt: i+1 for i, prompt in enumerate(unique_prompts)}

    # Create encoding table
    encoding_rows = [
        {"id": prompt_to_id[prompt], "prompt": prompt}
        for prompt in unique_prompts
    ]
    encoding_df = pd.DataFrame(encoding_rows).sort_values("id")

    # Convert main dataset to id + essay only
    df["prompt"] = df["prompt"].map(prompt_to_id)
    df = df[["essay", "prompt"]]

    # Write outputs
    df.to_csv(output_file, index=False)
    encoding_df.to_csv(encoding_file, index=False)

    print(f"✅ Compressed dataset written to {output_file}")
    print(f"🔎 Prompt → ID mapping written to {encoding_file}")

compress_dataset("essays_all.csv", "more_random_essays.csv", "more_random_encoding.csv")