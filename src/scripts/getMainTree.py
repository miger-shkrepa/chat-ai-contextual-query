import os
import json


def record_directory_structure(directory_path):
    """
    Recursively records the directory structure into a nested dictionary.
    """
    directory_structure = {}

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            # If it's a folder, recurse into it
            directory_structure[item] = record_directory_structure(item_path)
        else:
            # If it's a file, add it to the dictionary
            directory_structure[item] = None

    return directory_structure


def save_structure_to_file(structure, output_file):
    """
    Saves the directory structure to a JSON file.
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(structure, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # Replace 'main_directory_path' with the actual path to your main directory
    main_directory_path = "C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7"
    output_file = "directory_structure.json"

    if os.path.exists(main_directory_path) and os.path.isdir(main_directory_path):
        # Get the directory name to encapsulate everything under it
        main_directory_name = os.path.basename(os.path.abspath(main_directory_path))

        # Record the structure, encapsulating everything under the main folder
        structure = {main_directory_name: record_directory_structure(main_directory_path)}

        # Save to a file
        save_structure_to_file(structure, output_file)
        print(f"Directory structure has been saved to {output_file}")
    else:
        print("Invalid directory path. Please provide a valid path.")
