import json
import os

def get_advertisement_frequency_and_topics(directory):
    advertisement_frequency = {}
    advertisement_topics = {}
    for root, dirs, files in os.walk(directory):
        if 'ads_and_topics' in dirs:
            ads_and_topics_dir = os.path.join(root, 'ads_and_topics')
            for file in os.listdir(ads_and_topics_dir):
                if file == 'ads_viewed.json':
                    file_path = os.path.join(ads_and_topics_dir, file)
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            for impression in data['impressions_history_ads_seen']:
                                for string_map_data in impression['string_map_data'].values():
                                    if 'value' in string_map_data:
                                        author = string_map_data['value']
                                        if author not in advertisement_frequency:
                                            advertisement_frequency[author] = 0
                                        advertisement_frequency[author] += 1
                                        if author not in advertisement_topics:
                                            advertisement_topics[author] = []
                                        if 'Time' in string_map_data and 'timestamp' in string_map_data['Time']:
                                            timestamp = string_map_data['Time']['timestamp']
                                            topic = author
                                            advertisement_topics[author].append((timestamp, topic))
                    except FileNotFoundError:
                        print(f"File not found: {file_path}")
    return advertisement_frequency, advertisement_topics

def write_advertisement_frequency_and_topics_to_file(frequency, topics, output_file):
    with open(output_file, 'w') as f:
        f.write("Advertisement Frequency:\n")
        for author, count in frequency.items():
            f.write(f"{author}: {count}\n")
        f.write("\nAdvertisement Topics:\n")
        for author, topic_list in topics.items():
            f.write(f"{author}:\n")
            for timestamp, topic in topic_list:
                f.write(f" {timestamp}: {topic}\n")

if __name__ == '__main__':
    directory = "C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7"
    output_file = "results/advertisement_frequency_and_topics.txt"
    frequency, topics = get_advertisement_frequency_and_topics(directory)
    write_advertisement_frequency_and_topics_to_file(frequency, topics, output_file)
    print(f"Advertisement frequency and topics written to {output_file}")
