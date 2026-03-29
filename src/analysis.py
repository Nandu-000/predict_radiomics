import os
import pandas as pd

from preprocessing import preprocess_pipeline
from feature_extraction import get_extractor, extract_features
from agatston import agatston_score, agatston_category



def process_dataset(data_dir):
    extractor = get_extractor()
    results = []

    files = os.listdir(data_dir)
    print("FILES FOUND:", files)
    path = os.path.join(data_dir, file)

    for file in files:
        if file.endswith(".nii") or file.endswith(".nii.gz") or os.path.isdir(path):
            print(f"\nProcessing {file}...")
        else:
            print(f"Skipping {file}")
            continue

        path = os.path.join(data_dir, file)
        print(f"\nProcessing {file}...")

        try:
            image, mask = preprocess_pipeline(path)

            print("Preprocessing done")

            features = extract_features(image, mask, extractor)
            print("Feature extraction done")

            score = agatston_score(image)
            category = agatston_category(score)

            features["AgatstonScore"] = score
            features["Category"] = category
            features["PatientID"] = file

            results.append(features)
            print("Added to results ")

        except Exception as e:
            print(f"Error processing {file}: {e}")

    print("\nTOTAL SUCCESS:", len(results))
    return pd.DataFrame(results)


def save_results(df, output_path="../outputs/features.csv"):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(BASE_DIR, "outputs", "features.csv")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Saved results to {output_path}")


if __name__ == "__main__":
    data_dir = "../data/raw"  # CHANGE THIS PATH

    df = process_dataset(data_dir)
    save_results(df)