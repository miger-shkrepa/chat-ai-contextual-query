import json
import os
from collections import defaultdict
from datetime import datetime


def find_posts_viewed_file(main_directory):
    """Traverse the directory structure to find the posts_viewed.json file."""
    for root, dirs, files in os.walk(main_directory):
        if 'posts_viewed.json' in files:
            return os.path.join(root, 'posts_viewed.json')
    return None


def load_json(file_path):
    """Load and return the JSON data from the specified file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def analyze_posts(data):
    """Analyze the posts data and return daily and weekly post frequencies."""
    daily_frequency = defaultdict(int)  # Posts viewed per day
    weekly_frequency = defaultdict(int)  # Posts viewed per week

    for post in data.get('impressions_history_posts_seen', []):
        timestamp = post.get('string_map_data', {}).get('Time', {}).get('timestamp')
        if timestamp:
            # Convert timestamp to a datetime object
            post_date = datetime.fromtimestamp(timestamp)
            # Extract the date (YYYY-MM-DD) and week (YYYY-WW)
            date_key = post_date.strftime('%Y-%m-%d')
            week_key = post_date.strftime('%Y-%U')  # %U gives the week number of the year

            daily_frequency[date_key] += 1
            weekly_frequency[week_key] += 1

    return daily_frequency, weekly_frequency


def main():
    # Ask the user for the main directory containing Instagram data
    main_directory = "C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7".strip()

    # Check if the directory exists
    if not os.path.isdir(main_directory):
        print(f"Error: The directory '{main_directory}' does not exist.")
        return

    # Find the posts_viewed.json file
    posts_file_path = find_posts_viewed_file(main_directory)

    if not posts_file_path:
        print("Error: Could not find 'posts_viewed.json' in the directory structure.")
        return

    # Load the JSON data
    data = load_json(posts_file_path)

    # Analyze the posts data
    daily_frequency, weekly_frequency = analyze_posts(data)

    # Write the results to a .txt file
    output_file = 'results/posts_frequency_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Post Viewing Frequency Analysis:\n")
        f.write("================================\n\n")

        if daily_frequency:
            f.write("Daily Post Viewing Frequency:\n")
            for date, count in sorted(daily_frequency.items()):
                f.write(f"- {date}: {count} posts\n")

            f.write("\nWeekly Post Viewing Frequency:\n")
            for week, count in sorted(weekly_frequency.items()):
                f.write(f"- Week {week}: {count} posts\n")
        else:
            f.write("No post viewing data found.\n")

    print(f"Results have been saved to '{output_file}'.")


if __name__ == "__main__":
    main()