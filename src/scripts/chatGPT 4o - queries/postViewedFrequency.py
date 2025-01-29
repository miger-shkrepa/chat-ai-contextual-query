import json
import os
from collections import Counter
from datetime import datetime

def find_file(base_folder, target_file):
    """Recursively search for a file in the given folder."""
    for root, _, files in os.walk(base_folder):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def analyze_post_frequency(base_folder):
    try:
        # Find the relevant file
        target_file = "posts_viewed.json"
        file_path = find_file(base_folder, target_file)

        if not file_path:
            print(f"File {target_file} not found in {base_folder}.")
            return {}

        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract post view timestamps
        date_counter = Counter()
        for post_data in data.get("impressions_history_posts_seen", []):
            string_map_data = post_data.get("string_map_data", {})
            timestamp = string_map_data.get("Time", {}).get("timestamp")
            if timestamp:
                # Convert timestamp to a date object
                date = datetime.fromtimestamp(timestamp).date()
                date_counter[date] += 1

        return date_counter

    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the file structure.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def save_post_frequency_to_file(date_counter, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Post Viewing Frequency Analysis:\n")
            file.write("\nDate       | Number of Posts Seen\n")
            file.write("-----------------------------\n")

            for date, count in sorted(date_counter.items()):
                file.write(f"{date} | {count}\n")

        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# Path to the main folder
base_folder = "C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7"
# Output file path
output_file = "results/post_frequency_analysis.txt"

def main():
    date_counter = analyze_post_frequency(base_folder)
    if date_counter:
        save_post_frequency_to_file(date_counter, output_file)
    else:
        print("No post viewing data found or the file is empty.")

if __name__ == "__main__":
    main()
