import json
import os

def find_file(base_folder, target_file):
    """Recursively search for a file in the given folder."""
    for root, _, files in os.walk(base_folder):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def get_topics_of_interest(base_folder):
    try:
        # Find the relevant file
        target_file = "recommended_topics.json"
        file_path = find_file(base_folder, target_file)

        if not file_path:
            print(f"File {target_file} not found in {base_folder}.")
            return []

        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract topics of interest
        topics = []
        for topic_data in data.get("topics_your_topics", []):
            string_map_data = topic_data.get("string_map_data", {})
            topic_name = string_map_data.get("Name", {}).get("value")
            if topic_name:
                topics.append(topic_name)

        return topics

    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the file structure.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def save_topics_to_file(topics, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Topics of interest determined by Instagram:\n")
            for idx, topic in enumerate(topics, start=1):
                file.write(f"{idx}. {topic}\n")
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# Path to the main folder
#C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-21-TDz5ZSZM
base_folder = "C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7"
# Output file path
output_file = "results/topics_of_interest.txt"

def main():
    topics = get_topics_of_interest(base_folder)
    if topics:
        save_topics_to_file(topics, output_file)
    else:
        print("No topics of interest found or the file is empty.")

if __name__ == "__main__":
    main()
