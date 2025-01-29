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
          content_div = message_div.find_all('div')[1]  # Get the second div
          content = content_div.text.strip()
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

  with open("../../../collectedData/Gemini - conversation/message_content12.json", "w", encoding='utf-8') as f:
    json.dump({"messages": all_messages}, f, indent=2)
  print("Messages extracted and saved to 'message_content.json'")

def extract_hrefs_from_json(file_path):
  """
  Extracts 'href' fields from a single liked_posts.json file.

  Args:
    file_path: Path to the liked_posts.json file.

  Returns:
    A list of dictionaries, each containing an 'href' key.
  """

  hrefs = []
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      data = json.load(f)
      if "likes_media_likes" in data:
        for post in data["likes_media_likes"]:
          if "string_list_data" in post:
            for item in post["string_list_data"]:
              try:
                href = item["href"]
                hrefs.append({"href": href})
              except KeyError:
                print(f"Warning: 'href' key not found in an item in {file_path}")
  except (json.JSONDecodeError, FileNotFoundError) as e:
    print(f"Error processing {file_path}: {e}")
  return hrefs

def extract_hrefs_from_html(file_path):
  """
  Extracts 'href' fields from a single liked_posts.html file.

  Args:
    file_path: Path to the liked_posts.html file.

  Returns:
    A list of dictionaries, each containing an 'href' key.
  """

  hrefs = []
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      soup = BeautifulSoup(f, 'html.parser')
      for link_tag in soup.find_all('a', href=True):  # Find all anchor tags
        href = link_tag['href']
        hrefs.append({"href": href})
  except FileNotFoundError as e:
    print(f"Error processing {file_path}: {e}")
  return hrefs

def extract_hrefs(main_folder):
  """
  Extracts 'href' fields from 'liked_posts.json' or 'liked_posts.html' files.

  Args:
    main_folder: The path to the main folder.
  """

  all_hrefs = []

  for root, dirs, files in os.walk(main_folder):
    for file in files:
      if file.startswith("liked_posts."):
        file_path = os.path.join(root, file)
        if file.endswith(".json"):
          hrefs = extract_hrefs_from_json(file_path)
        elif file.endswith(".html"):
          hrefs = extract_hrefs_from_html(file_path)
        else:
          print(f"Warning: Unsupported file type: {file_path}")
          continue
        all_hrefs.extend(hrefs)

  with open("../../../collectedData/Gemini - conversation/liked_content12.json", "w", encoding='utf-8') as f:
    json.dump({"liked_posts": all_hrefs}, f, indent=2)
  print("Hrefs extracted and saved to 'liked_content.json'")

if __name__ == "__main__":
  main_folder_path = "C:/Users/Miger Shkrepa/Downloads/instagram-miger_shkrepa-2025-01-21-VvWLuxCS"  # Replace with the actual path

  extract_messages(main_folder_path)
  extract_hrefs(main_folder_path)