import json
import os

def extract_messages(main_folder):
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
          with open(file_path, 'r', encoding='utf-8') as f:
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

def extract_hrefs(main_folder):
  """
  Extracts all 'href' fields from 'liked_posts.json' files within nested folders.

  Args:
    main_folder: The path to the main folder.

  Returns:
    A list of 'href' strings.
  """

  all_hrefs = []

  for root, dirs, files in os.walk(main_folder):
    for file in files:
      if file == "liked_posts.json":
        file_path = os.path.join(root, file)
        try:
          with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "likes_media_likes" in data:
              for post in data["likes_media_likes"]:
                if "string_list_data" in post:
                  for item in post["string_list_data"]:
                    try:
                      href = item["href"]
                      all_hrefs.append(href)
                    except KeyError:
                      print(f"Warning: 'href' key not found in an item in {file_path}")
        except (json.JSONDecodeError, FileNotFoundError) as e:
          print(f"Error processing {file_path}: {e}")

  return all_hrefs

if __name__ == "__main__":
  main_folder_path = "C:/Users/Miger Shkrepa/Downloads/instagram-miger_shkrepa-2025-01-21-ntf85kwz"  # Replace with the actual path

  # Extract messages
  all_messages = extract_messages(main_folder_path)
  with open("../../../collectedData/Gemini - conversation/extracted_messages6.txt", "w", encoding='utf-8') as f:
    for message in all_messages:
      f.write(message + "\n")

  # Extract hrefs
  all_hrefs = extract_hrefs(main_folder_path)
  with open("../../../collectedData/Gemini - conversation/extracted_hrefs6.txt", "w", encoding='utf-8') as f:
    for href in all_hrefs:
      f.write(href + "\n")

  print("All messages extracted and saved to 'extracted_messages.txt'")
  print("All hrefs extracted and saved to 'extracted_hrefs.txt'")