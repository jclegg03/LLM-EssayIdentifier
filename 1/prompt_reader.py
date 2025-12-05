import os

def load_prompts(prompt_dir="prompts"):
    """
    Loads all prompt files from the given directory into a list of strings.
    Each file should contain a single prompt (UTF-8 text).
    
    Args:
        prompt_dir (str): Path to the directory containing prompt files.
    
    Returns:
        List[str]: A list of prompt texts.
    """
    if not os.path.isdir(prompt_dir):
        raise FileNotFoundError(f"Prompt directory '{prompt_dir}' does not exist.")

    prompts = []
    for filename in sorted(os.listdir(prompt_dir)):
        # skip hidden files and non-text files
        if filename.startswith(".") or not filename.lower().endswith((".txt", ".md")):
            continue

        path = os.path.join(prompt_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if content:
            prompts.append(content)
        else:
            print(f"!! Skipping empty file: {filename}")

    if not prompts:
        raise ValueError(f"No valid prompt files found in '{prompt_dir}'.")

    print(f"# Loaded {len(prompts)} prompts from '{prompt_dir}'")
    return prompts


# Allow standalone testing
if __name__ == "__main__":
    loaded = load_prompts()
    for i, p in enumerate(loaded, 1):
        print(f"\nPrompt {i}:\n{'-'*40}\n{p[:300]}{'...' if len(p) > 300 else ''}")