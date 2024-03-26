import json
import xml.etree.ElementTree as ET
from typing import Dict, Tuple, List

######################### Settings #########################################

WIKIPEDIA_FILE = "task-15/PRELEARN_dataset/PRELEARN_training_data/ITA_prereq-pages.xml"

CHOICES_MAPPING = {
    0: 'no',
    1: 'si'
}
FILES = [
    ("task-15/PRELEARN_dataset/PRELEARN_training_data/physics-pairs_train.csv", "PRELEARN-physics-train.jsonl"),

]


##########################################################################

def extract_topics(xml_file_path: str) -> Dict[str, str]:
    extracted_topics = {}
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    for item in root.findall('doc'):

        title = item.find('title').text
        text = item.find('text').text
        text = text.rstrip('\n')
        text = text.lstrip('\n')
        extracted_topics[title] = text
    return extracted_topics


def extract_tasks(file_path: str) -> List[Tuple[str, str, int]]:
    extracted_tasks = []
    with open(file_path, 'r') as file:
        for line in file:
            topic_A, topic_B, value = line.strip().split(',')
            extracted_tasks.append((topic_A, topic_B, int(value)))
    return extracted_tasks


def process_tasks(tasks, topics) -> List[str]:
    processed_tasks = []
    for topic_A, topic_B, value in tasks:
        wikipedia_passage_A = topics[topic_A]
        wikipedia_passage_B = topics[topic_B]
        processed_task = {
            "wikipedia_passage_concept_A": wikipedia_passage_A,
            "concept_A": topic_A,
            "wikipedia_passage_concept_B": wikipedia_passage_B,
            "concept_B": topic_B,
            "choices": [
                CHOICES_MAPPING[0],
                CHOICES_MAPPING[1]
            ],
            "target": value,
        }
        task_json = json.dumps(processed_task)
        processed_tasks.append(task_json)
    return processed_tasks


if __name__ == '__main__':
    print("Extracting wikipedia topics from: ", WIKIPEDIA_FILE)
    topics = extract_topics(WIKIPEDIA_FILE)
    for task_file, benchmark_file in FILES:
        print("Reading data from: ", task_file)
        tasks = extract_tasks(task_file)
        print("Creating benchmark: ", benchmark_file)
        with open(benchmark_file, 'w') as file:
            lines = process_tasks(tasks, topics)
            file.writelines(lines)
        print("Bechmark created")
    print("Done")


# TODO controllare dati invalidi? Tipo stringhe vuote ecc..