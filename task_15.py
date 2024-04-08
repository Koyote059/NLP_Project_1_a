import json
import os
import xml.etree.ElementTree as ET
from typing import Dict, Tuple, List

######################### Hyperparameters #########################################
# The name of the binary classes
CLASSES_NAMES = {
    0: 'no',
    1: 'si'
}
##############################à Settings ##############################################

# The file containing the wikipedia definitions of the words
WIKIPEDIA_FILE = "task-15/PRELEARN_dataset/PRELEARN_training_data/ITA_prereq-pages.xml"

# The dataset classes and the respective benchmark created
# in the format (Dataset,Benchmark)
FILES = [
    ("task-15/PRELEARN_dataset/PRELEARN_training_data/data_mining-pairs_train.csv",
     "task-15/benchmarks/PRELEARN-data_mining-pairs_train.jsonl"),
    ("task-15/PRELEARN_dataset/PRELEARN_training_data/physics-pairs_train.csv",
     "task-15/benchmarks/PRELEARN-physics-train.jsonl"),
    ("task-15/PRELEARN_dataset/PRELEARN_training_data/geometry-pairs_train.csv",
     "task-15/benchmarks/PRELEARN-geometry-pairs_train.jsonl"),
    ("task-15/PRELEARN_dataset/PRELEARN_training_data/precalculus-pairs_train.csv",
     "task-15/benchmarks/PRELEARN-precalculus-pairs_train.jsonl"),

    ("task-15/PRELEARN_dataset/PRELEARN_test-data/data_mining-pairs_test.txt",
     "task-15/benchmarks/PRELEARN-data_mining-pairs_test.jsonl"),
    ("task-15/PRELEARN_dataset/PRELEARN_test-data/physics-pairs_test.txt",
     "task-15/benchmarks/PRELEARN-physics-test.jsonl"),
    ("task-15/PRELEARN_dataset/PRELEARN_test-data/geometry-pairs_test.txt",
     "task-15/benchmarks/PRELEARN-geometry-pairs_test.jsonl"),
    ("task-15/PRELEARN_dataset/PRELEARN_test-data/precalculus-pairs_test.txt",
     "task-15/benchmarks/PRELEARN-precalculus-pairs_test.jsonl"),

]


##########################################################################

def extract_topics(xml_file_path: str) -> Dict[str, str]:
    """
    Extract the words description from a XML-based file.
    :param xml_file_path: the path to the XML file containing the words description.
    :return: Dict[str,str]. A mapping between a word and its description ( topics[word] = description ).
    """
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
    """
    Parses information from a csv style path in which each line is organized in the following way: text,text,number\n.
    :param file_path: the file to read.
    :return: List[Tuple[str, str, int]]. A list of tuple each of the following structure: (text,text,number)
    """

    extracted_tasks = []
    with open(file_path, 'r') as file:
        for line in file:
            topic_A, topic_B, value = line.strip().split(',')
            extracted_tasks.append((topic_A, topic_B, int(value)))
    return extracted_tasks


def is_json_invalid(validated_jason: dict):
    """
    It checks if a dict is ivalid.
    A dict is invalid if it has empty values inside.
    :param validated_jason: dict. The dict to validate.
    :return: bool. True if there are empty values, False instead.
    """
    return any([key for key, value in validated_jason.items() if value == ""])


def process_tasks(tasks: List[Tuple[str, str, int]], topics: Dict[str, str], file_name: str) -> List[str]:
    """
    Processes the tasks into a list of JSON-like strings.
    :param tasks: List[Tuple[str, str, int]]. The list of tasks to process ( each one in the form of (text,text,number) ).
    :param topics: Dict[str, str]. The mapping between each word to its meaning (in the form of topics[word] = meaning ).
    :param file_name: str. The file in which the dataset is stored. Used for ID generation.
    :return: List[str]. A list of JSON-style strings.
    Each JSON-style string has the following structure:
    {
        "wikipedia_passage_concept_A": str. wikipedia_passage_A,
        "concept_A": str. topic_A,
        "wikipedia_passage_concept_B": str. wikipedia_passage_B,
        "concept_B": str. topic_B,
        "choices": [
            CLASSES_NAMES[0], str
            CLASSES_NAMES[1] str
        ],
        "target": int. index of right element in choices ( either 0 or 1 ),
        "id": "{file_name}_task-15_{unique_id}"
    }

    """
    processed_tasks = []
    record_id = 0
    for topic_A, topic_B, value in tasks:
        wikipedia_passage_A = topics[topic_A]
        wikipedia_passage_B = topics[topic_B]
        processed_task = {
            "wikipedia_passage_concept_A": wikipedia_passage_A,
            "concept_A": topic_A,
            "wikipedia_passage_concept_B": wikipedia_passage_B,
            "concept_B": topic_B,
            "choices": [
                CLASSES_NAMES[0],
                CLASSES_NAMES[1]
            ],
            "target": value,
            "id": f"{file_name}_task-15_{record_id}"
        }
        if is_json_invalid(processed_task):
            continue
        record_id = record_id + 1
        task_json = json.dumps(processed_task)
        processed_tasks.append(task_json + '\n')
    return processed_tasks


def create_benchmark():
    """
    Creates the benchmark by reading data from the datasets, processing
    it and writing it to the created benchmark file.
    """
    print("Extracting wikipedia topics from: ", WIKIPEDIA_FILE)
    topics = extract_topics(WIKIPEDIA_FILE)
    for task_file, benchmark_file in FILES:
        print("Reading data from: ", task_file)
        tasks = extract_tasks(task_file)
        print("Creating benchmark: ", benchmark_file)
        with open(benchmark_file, 'w') as file:
            file_name = os.path.splitext(os.path.basename(task_file))[0]
            lines = process_tasks(tasks, topics, file_name)
            file.writelines(lines)
        print("Bechmark created")
    print("Done")


if __name__ == '__main__':
    create_benchmark()
