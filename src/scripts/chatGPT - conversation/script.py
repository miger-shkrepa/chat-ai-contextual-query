import os
import json

def extract_content_from_message(file_path):
    """Extracts the first instance of the 'content' field from a given message_1.json file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if "messages" in data:
                for message in data["messages"]:
                    if "content" in message:
                        return message["content"]
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading file {file_path}: {e}")
    return None

def find_message_files(base_path):
    """Recursively searches for message_1.json files in the given folder."""
    for root, _, files in os.walk(base_path):
        for file in files:
            if file == "message_1.json":
                yield os.path.join(root, file)

def main(base_folder):
    """Main function to locate and extract content from message_1.json files."""
    for file_path in find_message_files(base_folder):
        content = extract_content_from_message(file_path)
        if content:
            print(f"Content found in {file_path}: {content}")
            break  # Stop after finding the first content field

# Replace 'your_main_folder_path' with the path to the main folder
main_folder = 'C:/Users/Miger Shkrepa/Downloads/instagram-miger_shkrepa-2025-01-21-ntf85kwz'
main(main_folder)