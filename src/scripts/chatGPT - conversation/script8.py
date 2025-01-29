import os
import json
from bs4 import BeautifulSoup  # For HTML parsing

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
                                extracted_values.append({field: sub_item[field]})
                    elif field in item:
                        extracted_values.append({field: item[field]})
            elif not nested_key:
                if field in data:
                    extracted_values.append({field: data[field]})
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading file {file_path}: {e}")
    return extracted_values

def extract_field_from_html(file_path, content_class=None, href_tag=None):
    """
    Extracts fields from an HTML file based on the provided tag/class structure.
    """
    extracted_content = []
    extracted_href = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

            # Extract content fields
            if content_class:
                for tag in soup.find_all(attrs={"class": content_class}):
                    content_text = tag.get_text(strip=True)
                    if content_text:
                        extracted_content.append({"content": content_text})

            # Extract href fields
            if href_tag:
                for tag in soup.find_all(href=True):
                    href_value = tag.get("href")
                    if href_value:
                        extracted_href.append({"href": href_value})
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
    return extracted_content, extracted_href

def find_specific_files(base_path, extensions):
    """
    Recursively searches for files with specific extensions in the directory.
    """
    for root, _, files in os.walk(base_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
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

def main(base_folder, output_message_json, output_liked_json):
    """
    Main function to locate and process files for extracting fields.
    """
    message_list = []
    liked_list = []

    # Process JSON and HTML files
    print("Processing files...")
    for file_path in find_specific_files(base_folder, [".json", ".html"]):
        if file_path.endswith(".json"):
            if "message_1.json" in file_path:
                print(f"Processing JSON file: {file_path}")
                message_list.extend(extract_field_from_json(file_path, "content", nested_key="messages"))
            elif "liked_posts.json" in file_path:
                print(f"Processing JSON file: {file_path}")
                liked_list.extend(extract_field_from_json(file_path, "href", nested_key="likes_media_likes", sub_nested_key="string_list_data"))
        elif file_path.endswith(".html"):
            if "message_1.html" in file_path:
                print(f"Processing HTML file: {file_path}")
                content, _ = extract_field_from_html(file_path, content_class="content")
                message_list.extend(content)
            elif "liked_posts.html" in file_path:
                print(f"Processing HTML file: {file_path}")
                _, href = extract_field_from_html(file_path, href_tag="a")
                liked_list.extend(href)

    # Save content and hrefs to JSON files
    save_to_json_file(output_message_json, message_list, "message")
    save_to_json_file(output_liked_json, liked_list, "liked_content")

# Navigate to the project root directory
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of python.py
project_root = os.path.abspath(os.path.join(script_dir, "../../../"))  # Move two levels up

# Define folder paths relative to the project root
data_folder = os.path.join(project_root, "data\\instagram-miger_shkrepa-2025-01-21-VvWLuxCS")
output_folder = os.path.join(project_root, "collectedData\\chatGPT - conversation")

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Define collectedData file paths within the collectedData folder
output_message_json = os.path.join(output_folder, "message_content8.json")
output_liked_json = os.path.join(output_folder, "liked_content8.json")

# Execute the main function
main(data_folder, output_message_json, output_liked_json)
