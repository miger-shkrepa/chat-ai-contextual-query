import json
import os

def extract_messages(main_folder):
  """
  Extracts the 'content' field from 'message_1.json' files within nested folders.

  Args:
    main_folder: The path to the main folder.

  Returns:
    A list of 'content' strings.
  """

  messages = []

  for root, dirs, files in os.walk(main_folder):
    for file in files:
      if file == "message_1.json":
        file_path = os.path.join(root, file)
        try:
          with open(file_path, 'r') as f:
            data = json.load(f)
            if "messages" in data:
              for message in data["messages"]:
                messages.append(message["content"])
                break  # Collect only the first instance
        except (json.JSONDecodeError, FileNotFoundError) as e:
          print(f"Error processing {file_path}: {e}")

  return messages

if __name__ == "__main__":
  main_folder_path = "C:/Users/Miger Shkrepa/Downloads/instagram-miger_shkrepa-2025-01-21-ntf85kwz"  # Replace with the actual path
  extracted_messages = extract_messages(main_folder_path)

  for message in extracted_messages:
    print(message)
