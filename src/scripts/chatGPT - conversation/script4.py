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
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading file {file_path}: {e}")
    return extracted_values

def find_specific_files(base_path, target_files):
    """
    Recursively searches for specific files in the directory.
    :param base_path: The base folder to search.
    :param target_files: A list of file names to find (e.g., ["message_1.json", "liked_posts.json"]).
    :return: A generator of file paths that match the target files.
    """
    for root, _, files in os.walk(base_path):
        for file in files:
            if file in target_files:
                yield os.path.join(root, file)

def main(base_folder, output_content_file, output_href_file):
    """
    Main function to locate `message_1.json` and `liked_posts.json` files,
    extract specific fields, and write them to separate text files.
    """
    content_list = []
    href_list = []

    # Locate and process files
    for file_path in find_specific_files(base_folder, ["message_1.json", "liked_posts.json"]):
        if file_path.endswith("message_1.json"):
            content_list.extend(extract_field_from_json(file_path, "content", nested_key="messages"))
        elif file_path.endswith("liked_posts.json"):
            href_list.extend(extract_field_from_json(file_path, "href", nested_key="likes_media_likes", sub_nested_key="string_list_data"))

    # Write collected contents to their respective collectedData files
    try:
        with open(output_content_file, 'w', encoding='utf-8') as content_file:
            for content in content_list:
                content_file.write(content + '\n')
        print(f"All 'content' fields written to {output_content_file}")
    except IOError as e:
        print(f"Error writing to {output_content_file}: {e}")

    try:
        with open(output_href_file, 'w', encoding='utf-8') as href_file:
            for href in href_list:
                href_file.write(href + '\n')
        print(f"All 'href' fields written to {output_href_file}")
    except IOError as e:
        print(f"Error writing to {output_href_file}: {e}")

# Replace 'your_main_folder_path' with the path to the main folder
main_folder = 'C:/Users/Miger Shkrepa/Downloads/instagram-miger_shkrepa-2025-01-21-ntf85kwz'
output_content_txt = 'C:/Users/Miger Shkrepa/Desktop/python/runScript/collected_contents4.txt'
output_href_txt = 'C:/Users/Miger Shkrepa/Desktop/python/runScript/collected_hrefs4.txt'

main(main_folder, output_content_txt, output_href_txt)
