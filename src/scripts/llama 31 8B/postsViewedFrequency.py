import json
import os
import datetime

def get_post_frequency(directory):
    post_frequency = {'daily': 0, 'weekly': 0, 'monthly': 0}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'posts_viewed.json':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for impression in data['impressions_history_posts_seen']:
                            string_map_data = impression['string_map_data']
                            timestamp = string_map_data['Time']['timestamp']
                            date = datetime.datetime.fromtimestamp(timestamp / 1000)
                            today = datetime.date.today()
                            yesterday = today - datetime.timedelta(days=1)
                            last_week = today - datetime.timedelta(days=7)
                            last_month = today - datetime.timedelta(days=30)
                            if date.date() == today.date():
                                post_frequency['daily'] += 1
                            elif date.date() == yesterday.date():
                                post_frequency['daily'] += 1
                            elif last_week <= date.date() <= today.date():
                                post_frequency['weekly'] += 1
                            elif last_month <= date.date() <= today.date():
                                post_frequency['monthly'] += 1
                except FileNotFoundError:
                    print(f"File not found: {file_path}")
    return post_frequency

def write_post_frequency_to_file(frequency, output_file):
    with open(output_file, 'w') as f:
        f.write("Post Frequency:\n")
        f.write(f"Daily: {frequency['daily']}\n")
        f.write(f"Weekly: {frequency['weekly']}\n")
        f.write(f"Monthly: {frequency['monthly']}\n")

if __name__ == '__main__':
    directory = "C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7"
    output_file = "results/post_frequency.txt"
    frequency = get_post_frequency(directory)
    write_post_frequency_to_file(frequency, output_file)
    print(f"Post frequency written to {output_file}")
