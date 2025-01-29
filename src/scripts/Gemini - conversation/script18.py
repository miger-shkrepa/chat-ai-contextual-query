import json
import os
from bs4 import BeautifulSoup

def extract_messages_from_json(file_path):
  """
  Extracts 'content' fields from a single message_1.json file.

  Args:
    file_path: Path to the message_1.json file.

  Returns:
    A list of dictionaries, each containing a 'content' key.
  """

  messages = []
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      data = json.load(f)
      if "messages" in data:
        for message in data["messages"]:
          try:
            content = message["content"]
            if content.strip():  # Skip empty strings
              messages.append({"content": content})
          except KeyError:
            print(f"Warning: 'content' key not found in a message in {file_path}")
  except (json.JSONDecodeError, FileNotFoundError) as e:
    print(f"Error processing {file_path}: {e}")
  return messages

def extract_messages_from_html(file_path):
  """
  Extracts 'content' fields from a single message_1.html file.

  Args:
    file_path: Path to the message_1.html file.

  Returns:
    A list of dictionaries, each containing a 'content' key.
  """

  messages = []
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      soup = BeautifulSoup(f, 'html.parser')
      for message_div in soup.find_all('div', class_="_3-95 _a6-p"):
        try:
          nested_divs = message_div.find_all('div')
          if len(nested_divs) >= 3:  # Ensure there are at least 3 nested divs
            content_div = nested_divs[2]
            content = content_div.text.strip()
            if content:  # Skip empty strings
              messages.append({"content": content})
        except (IndexError, AttributeError):
          print(f"Warning: Could not extract content from message in {file_path}")
  except FileNotFoundError as e:
    print(f"Error processing {file_path}: {e}")
  return messages

def extract_messages(main_folder):
  """
  Extracts 'content' fields from 'message_1.json' or 'message_1.html' files.

  Args:
    main_folder: The path to the main folder.
  """

  all_messages = []

  for root, dirs, files in os.walk(main_folder):
    for file in files:
      if file.startswith("message_1."):
        file_path = os.path.join(root, file)
        if file.endswith(".json"):
          messages = extract_messages_from_json(file_path)
        elif file.endswith(".html"):
          messages = extract_messages_from_html(file_path)
        else:
          print(f"Warning: Unsupported file type: {file_path}")
          continue
        all_messages.extend(messages)

  with open("message_content.json", "w", encoding='utf-8') as f:
    json.dump({"messages": all_messages}, f, indent=2)
  print("Messages extracted and saved to 'message_content.json'")

# ... (rest of the code for extract_hrefs remains the same)

if __name__ == "__main__":
  main_folder_path = "/path/to/your/main/folder"  # Replace with the actual path

  extract_messages(main_folder_path)
  extract_hrefs(main_folder_path)