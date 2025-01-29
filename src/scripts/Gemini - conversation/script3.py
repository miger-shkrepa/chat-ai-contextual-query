import json
import os

def extract_all_messages(main_folder):
  """
  Extracts all 'content' fields from 'message_1.json' files within nested folders.

  Args:
    main_folder: The path to the main folder.

  Returns:
    A list of 'content' strings.
  """

  all_messages = []

  for root, dirs, files in os.walk(main_folder):
    for file in files:
      if file == "message_1.json":
        file_path = os.path.join(root, file)
        try:
          with open(file_path, 'r') as f:
            data = json.load(f)
            if "messages" in data:
              for message in data["messages"]:
                try:
                  content = message["content"]
                  all_messages.append(content)
                except KeyError:
                  print(f"Warning: 'content' key not found in a message in {file_path}")
        except (json.JSONDecodeError, FileNotFoundError) as e:
          print(f"Error processing {file_path}: {e}")

  return all_messages

if __name__ == "__main__":
  main_folder_path = "C:/Users/Miger Shkrepa/Downloads/instagram-miger_shkrepa-2025-01-21-ntf85kwz"  # Replace with the actual path
  all_messages = extract_all_messages(main_folder_path)

  with open("../../../collectedData/Gemini - conversation/extracted_messages.txt", "w") as f:
    for message in all_messages:
      f.write(message + "\n")

  print("All messages extracted and saved to 'extracted_messages.txt'")