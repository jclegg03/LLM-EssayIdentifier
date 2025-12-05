
#!/usr/bin/env python3
"""
Merge essays.csv from folders 1–5 into one central CSV file.
Run this from the directory that contains folders '1', '2', '3', '4', '5'.
"""

import os
import pandas as pd

def main():
    # Change these if needed
    folder_names = [str(i) for i in range(1, 6)]
    source_filename = "essays.csv"
    output_filename = "essays_all.csv"  # central merged file
    output_path = os.path.join(os.getcwd(), output_filename)

    frames = []
    for folder in folder_names:
        csv_path = os.path.join(os.getcwd(), folder, source_filename)
        if not os.path.isfile(csv_path):
            print(f"[WARN] Missing file: {csv_path} — skipping.")
            continue
        try:
            # Adjust encoding or sep if necessary, e.g., encoding='utf-8-sig', sep=';'
            df = pd.read_csv(csv_path)
            frames.append(df)
            print(f"[OK] Loaded {csv_path} — {len(df)} rows.")
        except Exception as e:
            print(f"[ERROR] Failed reading {csv_path}: {e}")

    if not frames:
        print("[INFO] No data loaded; nothing to write.")
        return

    merged = pd.concat(frames, ignore_index=True)

    # Write output; index=False prevents row numbers in the CSV
    try:
        merged.to_csv(output_path, index=False)
        print(f"[DONE] Wrote merged file: {output_path} — {len(merged)} rows.")
    except Exception as e:
        print(f"[ERROR] Failed writing output to {output_path}: {e}")

if __name__ == "__main__":
    main()
