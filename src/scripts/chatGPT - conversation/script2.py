import os
import json

def extract_all_content_from_message(file_path):
    """Extracts all instances of the 'content' field from a given message_1.json file."""
    content_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if "messages" in data:
                for message in data["messages"]:
                    if "content" in message:
                        content_list.append(message["content"])
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading file {file_path}: {e}")
    return content_list

def find_message_files(base_path):
    """Recursively searches for message_1.json files in the given folder."""
    for root, _, files in os.walk(base_path):
        for file in files:
            if file == "message_1.json":
                yield os.path.join(root, file)

def main(base_folder, output_file):
    """Main function to locate message_1.json files and extract all content fields."""
    all_content = []
    for file_path in find_message_files(base_folder):
        contents = extract_all_content_from_message(file_path)
        all_content.extend(contents)

    # Write all collected content to the collectedData file
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            for content in all_content:
                output.write(content + '\n')
        print(f"All content written to {output_file}")
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")

# Replace 'your_main_folder_path' with the path to the main folder
main_folder = 'C:/Users/Miger Shkrepa/Downloads/instagram-miger_shkrepa-2025-01-21-ntf85kwz'
output_txt_file = '../../../collectedData/chatGPT - conversation/collected_contents2.txt'
main(main_folder, output_txt_file)
