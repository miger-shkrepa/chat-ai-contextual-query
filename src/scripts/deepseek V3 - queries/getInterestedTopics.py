import json
import os


def find_recommended_topics_file(main_directory):
    """Traverse the directory structure to find the recommended_topics.json file."""
    for root, dirs, files in os.walk(main_directory):
        if 'recommended_topics.json' in files:
            return os.path.join(root, 'recommended_topics.json')
    return None


def load_json(file_path):
    """Load and return the JSON data from the specified file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_recommended_topics(data):
    """Extract and return the list of recommended topics from the JSON data."""
    topics = []
    for topic in data.get('topics_your_topics', []):
        topic_name = topic.get('string_map_data', {}).get('Name', {}).get('value')
        if topic_name:
            topics.append(topic_name)
    return topics


def main():
    # Ask the user for the main directory containing Instagram data
    main_directory = "C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7".strip()

    # Check if the directory exists
    if not os.path.isdir(main_directory):
        print(f"Error: The directory '{main_directory}' does not exist.")
        return

    # Find the recommended_topics.json file
    topics_file_path = find_recommended_topics_file(main_directory)

    if not topics_file_path:
        print("Error: Could not find 'recommended_topics.json' in the directory structure.")
        return

    # Load the JSON data
    data = load_json(topics_file_path)

    # Get the recommended topics
    topics = get_recommended_topics(data)

    # Write the results to a .txt file
    output_file = os.path.join(main_directory, 'recommended_topics_output.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        if topics:
            f.write("Topics Instagram determines to be of interest for you:\n")
            for topic in topics:
                f.write(f"- {topic}\n")
            print(f"Results have been saved to '{output_file}'.")
        else:
            f.write("No recommended topics found.\n")
            print("No recommended topics found.")


if __name__ == "__main__":
    main()