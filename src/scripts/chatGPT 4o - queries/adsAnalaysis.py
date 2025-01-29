import json
import os
from collections import Counter

def find_file(base_folder, target_file):
    """Recursively search for a file in the given folder."""
    for root, _, files in os.walk(base_folder):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def analyze_ads(base_folder):
    try:
        # Find the relevant file
        target_file = "ads_viewed.json"
        file_path = find_file(base_folder, target_file)

        if not file_path:
            print(f"File {target_file} not found in {base_folder}.")
            return {}

        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract ad view data
        ad_counts = Counter()
        for ad_data in data.get("impressions_history_ads_seen", []):
            string_map_data = ad_data.get("string_map_data", {})
            company = string_map_data.get("Author", {}).get("value")
            if company:
                ad_counts[company] += 1

        return ad_counts

    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the file structure.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def save_ad_analysis_to_file(ad_counts, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Advertisement Analysis:\n")
            file.write("\nCompany Name | Number of Ads Seen\n")
            file.write("-------------------------------\n")
            for company, count in ad_counts.items():
                file.write(f"{company} | {count}\n")
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# Path to the main folder
base_folder = "C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7"
# Output file path
output_file = "results/ads_analysis.txt"

def main():
    ad_counts = analyze_ads(base_folder)
    if ad_counts:
        save_ad_analysis_to_file(ad_counts, output_file)
    else:
        print("No advertisement data found or the file is empty.")

if __name__ == "__main__":
    main()
