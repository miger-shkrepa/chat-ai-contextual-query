import json
import os
from collections import defaultdict


def find_ads_viewed_file(main_directory):
    """Traverse the directory structure to find the ads_viewed.json file."""
    for root, dirs, files in os.walk(main_directory):
        if 'ads_viewed.json' in files:
            return os.path.join(root, 'ads_viewed.json')
    return None


def load_json(file_path):
    """Load and return the JSON data from the specified file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def analyze_ads(data):
    """Analyze the ads data and return a dictionary with ad frequency and topics."""
    ad_frequency = defaultdict(int)  # Count how often each company's ads are seen
    ad_topics = defaultdict(list)  # Store topics associated with each company

    for ad in data.get('impressions_history_ads_seen', []):
        author = ad.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
        ad_frequency[author] += 1

        # If there are additional fields for topics, add them here
        # For example, if the ad has a "Topic" field, you can extract it like this:
        # topic = ad.get('string_map_data', {}).get('Topic', {}).get('value', 'Unknown')
        # ad_topics[author].append(topic)

    return ad_frequency, ad_topics


def main():
    # Ask the user for the main directory containing Instagram data
    main_directory = "C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7".strip()

    # Check if the directory exists
    if not os.path.isdir(main_directory):
        print(f"Error: The directory '{main_directory}' does not exist.")
        return

    # Find the ads_viewed.json file
    ads_file_path = find_ads_viewed_file(main_directory)

    if not ads_file_path:
        print("Error: Could not find 'ads_viewed.json' in the directory structure.")
        return

    # Load the JSON data
    data = load_json(ads_file_path)

    # Analyze the ads data
    ad_frequency, ad_topics = analyze_ads(data)

    # Write the results to a .txt file
    output_file = 'results/ads_analysis_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Advertisement Analysis:\n")
        f.write("=======================\n\n")

        if ad_frequency:
            f.write("Frequency of Ads Viewed (by Company):\n")
            for company, count in ad_frequency.items():
                f.write(f"- {company}: {count} ads\n")

            f.write("\nTopics Associated with Ads (by Company):\n")
            for company, topics in ad_topics.items():
                if topics:
                    f.write(f"- {company}: {', '.join(topics)}\n")
                else:
                    f.write(f"- {company}: No specific topics found.\n")
        else:
            f.write("No advertisement data found.\n")

    print(f"Results have been saved to '{output_file}'.")


if __name__ == "__main__":
    main()