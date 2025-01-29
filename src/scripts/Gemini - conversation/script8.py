import json
import os

def extract_messages(main_folder):
  """
  Extracts 'content' fields from 'message_1.json' files and saves them to JSON.

  Args:
    main_folder: The path to the main folder.
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
                  all_messages.append({"content": content})
                except KeyError:
                  print(f"Warning: 'content' key not found in a message in {file_path}")
        except (json.JSONDecodeError, FileNotFoundError) as e:
          print(f"Error processing {file_path}: {e}")

  with open("../../../collectedData/Gemini - conversation/message_content8.json", "w", encoding='utf-8') as f:
    json.dump({"messages": all_messages}, f, indent=2)

def extract_hrefs(main_folder):
  """
  Extracts 'href' fields from 'liked_posts.json' files and saves them to JSON.

  Args:
    main_folder: The path to the main folder.
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
                      all_hrefs.append({"href": href})
                    except KeyError:
                      print(f"Warning: 'href' key not found in an item in {file_path}")
        except (json.JSONDecodeError, FileNotFoundError) as e:
          print(f"Error processing {file_path}: {e}")

  with open("../../../collectedData/Gemini - conversation/liked_content8.json", "w", encoding='utf-8') as f:
    json.dump({"liked_posts": all_hrefs}, f, indent=2)

if __name__ == "__main__":
  main_folder_path = "C:/Users/Miger Shkrepa/Downloads/instagram-miger_shkrepa-2025-01-21-ntf85kwz"  # Replace with the actual path

  extract_messages(main_folder_path)
  print("Messages extracted and saved to 'message_content.json'")

  extract_hrefs(main_folder_path)
  print("Hrefs extracted and saved to 'liked_content.json'")