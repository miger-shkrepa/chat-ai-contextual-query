import json
import os


def get_topics_of_interest(directory):
    topics = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'recommended_topics.json':
                file_path = os.path.join(root, file)
    with open(file_path, 'r') as f:
        data = json.load(f)
    for topic in data['topics_your_topics']:
        topics.append(topic['string_map_data']['Name']['value'])
    return topics


def write_topics_to_file(topics, output_file):
    with open(output_file, 'w') as f:
        for topic in topics:
            f.write(topic + '\n')


if __name__ == '__main__':
    directory = "C:\\Users\\Miger Shkrepa\\Desktop\\python\\runScript\\data\\instagram-miger_shkrepa-2025-01-25-9eXjs0P7"
    output_file = "results/topics_of_interest.txt"
    topics = get_topics_of_interest(directory)
    write_topics_to_file(topics, output_file)
    print(f"Topics of interest written to {output_file}")
