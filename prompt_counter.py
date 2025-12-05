
import pandas as pd

def count_essays_by_prompt(csv_file):
    """
    Counts the number of essays for each unique prompt in the given CSV file.

    Parameters:
        csv_file (str): Path to the CSV file containing essays.

    Returns:
        dict: A dictionary where keys are prompts and values are counts.
    """
    df = pd.read_csv(csv_file)
    counts = df['prompt'].value_counts().to_dict()
    return counts

# Example usage:
# essay_counts = count_essays_by_prompt("essays.csv")

print(count_essays_by_prompt("more_random_essays.csv"))