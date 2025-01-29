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

def extract_field_from_html(file_path, message_class=None, liked_class=None):
    """
    Extracts fields from an HTML file based on the provided structure for messages and liked posts.
    """
    extracted_content = []
    extracted_href = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

            # Extract message content
            if message_class:
                for outer_div in soup.find_all('div', class_=message_class):
                    nested_div = outer_div.find('div', recursive=False)  # Get the first nested div
                    if nested_div:
                        inner_divs = nested_div.find_all('div', recursive=False)  # Get all direct children divs
                        if len(inner_divs) >= 2:  # Ensure at least 2 divs exist
                            content_div = inner_divs[1]  # Get the second div
                            content_text = content_div.get_text(strip=True)  # Extract content text
                            if content_text:
                                extracted_content.append({"content": content_text})

            # Extract liked post hrefs
            if liked_class:
                for outer_div in soup.find_all('div', class_=liked_class):
                    nested_div = outer_div.find('div')
                    if nested_div:
                        href_div = nested_div.find('div')
                        if href_div:
                            link = href_div.find('a', href=True)
                            if link and link['href']:
                                extracted_href.append({"href": link['href']})
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
                content, _ = extract_field_from_html(file_path, message_class="_3-95 _a6-p")
                message_list.extend(content)
            elif "liked_posts.html" in file_path:
                print(f"Processing HTML file: {file_path}")
                _, href = extract_field_from_html(file_path, liked_class="_a6-p")
                liked_list.extend(href)

    # Save content and hrefs to JSON files
    save_to_json_file(output_message_json, message_list, "message")
    save_to_json_file(output_liked_json, liked_list, "liked_content")

# Navigate to the project root directory
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of python.py
project_root = os.path.abspath(os.path.join(script_dir, "../../../"))  # Move two levels up

# Define folder paths relative to the project root
data_folder = os.path.join(project_root, "data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7")
output_folder = os.path.join(project_root, "collectedData\\chatGPT - conversation")

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Define collectedData file paths within the collectedData folder
output_message_json = os.path.join(output_folder, "message_content13.json")
output_liked_json = os.path.join(output_folder, "liked_content13.json")

# Execute the main function
main(data_folder, output_message_json, output_liked_json)
