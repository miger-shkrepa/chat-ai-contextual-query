import os
import json


def extract_field_from_json(file_path, field, nested_key=None, sub_nested_key=None):
    """
    Extracts all instances of a specific field from a JSON file.
    Handles nested structures if `nested_key` and `sub_nested_key` are provided.
    """
    extracted_values = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if nested_key and nested_key in data:
                for item in data[nested_key]:
                    if sub_nested_key and sub_nested_key in item:
                        for sub_item in item[sub_nested_key]:
                            if field in sub_item:
                                extracted_values.append(sub_item[field])
                    elif field in item:
                        extracted_values.append(item[field])
            elif not nested_key:
                if field in data:
                    extracted_values.append(data[field])
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading file {file_path}: {e}")
    return extracted_values


def find_specific_files(base_path, target_files):
    """
    Recursively searches for specific files in the directory.
    """
    for root, _, files in os.walk(base_path):
        for file in files:
            if file in target_files:
                yield os.path.join(root, file)


def save_to_json_file(file_path, data, top_level_key):
    """
    Saves the given data to a JSON file under a specified top-level key.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump({top_level_key: data}, json_file, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {file_path}")
    except IOError as e:
        print(f"Error writing to {file_path}: {e}")


def main(base_folder, output_content_file, output_href_file, output_message_json, output_liked_json):
    """
    Main function to locate and process files for extracting fields.
    """
    content_list = []
    href_list = []

    # Process message_1.json for content fields
    print("Processing message_1.json files...")
    for file_path in find_specific_files(base_folder, ["message_1.json"]):
        print(f"Processing file: {file_path}")
        content_list.extend(extract_field_from_json(file_path, "content", nested_key="messages"))

    # Write content to text file
    try:
        with open(output_content_file, 'w', encoding='utf-8') as content_file:
            for content in content_list:
                content_file.write(content + '\n')
        print(f"All 'content' fields written to {output_content_file}")
    except IOError as e:
        print(f"Error writing to {output_content_file}: {e}")

    # Save content to JSON file
    save_to_json_file(output_message_json, content_list, "message")

    # Process liked_posts.json for href fields
    print("Processing liked_posts.json files...")
    for file_path in find_specific_files(base_folder, ["liked_posts.json"]):
        print(f"Processing file: {file_path}")
        href_list.extend(extract_field_from_json(file_path, "href", nested_key="likes_media_likes",
                                                 sub_nested_key="string_list_data"))

    # Write href to text file
    try:
        with open(output_href_file, 'w', encoding='utf-8') as href_file:
            for href in href_list:
                href_file.write(href + '\n')
        print(f"All 'href' fields written to {output_href_file}")
    except IOError as e:
        print(f"Error writing to {output_href_file}: {e}")

    # Save href to JSON file
    save_to_json_file(output_liked_json, href_list, "liked_content")


# Navigate to the project root directory
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of python.py
project_root = os.path.abspath(os.path.join(script_dir, "../../../"))  # Move two levels up

# Define folder paths relative to the project root
data_folder = os.path.join(project_root, "data\\instagram-miger_shkrepa-2025-01-21-ntf85kwz")
output_folder = os.path.join(project_root, "collectedData\\chatGPT - conversation")

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Define collectedData file paths within the collectedData folder
output_content_txt = output_folder + '/collected_contents6.txt'
output_href_txt = output_folder + '/collected_hrefs6.txt'
output_message_json = output_folder + '/message_content6.json'
output_liked_json = output_folder + '/liked_content6.json'

main(data_folder, output_content_txt, output_href_txt, output_message_json, output_liked_json)
