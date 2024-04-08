import os.path
import random, json
from typing import Set, Dict

import numpy as np
import csv
from scipy.stats import truncnorm

######################### Hyperparameters ######################################

# Categorical natural language labels
# The name of the classes given for the word classification
CLASSES_NAMES = {
    1: 'totalmente astratta',
    2: 'abbastanza astratta',
    3: 'parzialmente astratta',
    4: 'semiconcreta',
    5: 'parzialmente concreta',
    6: 'abbastanza concreta',
    7: 'totalmente concreta'
}

# The Gaussian Standard Deviation used for sampling of the classes
GAUSSIAN_STD_DEV = 2
# Number of  distractors to create
DISTRACTORS = 3

######################### Settings ######################################


# The dataset classes and the respective benchmark created
# in the format (Dataset,Benchmark)
FILES = [
    ("task-13/CONcreTEXT_trial_IT.tsv", "task-13/CONcreTEXT-train-data.jsonl"),
    ("task-13/CONcreTEXT_test_IT.tsv", "task-13/CONcreTEXT-test-data.jsonl"),

]


##########################################################################

def get_gaussian_samples(center: int, lower_limit: int, upper_limit, num_samples: int, std_dev: float) -> Set[int]:
    """
    Samples some integer numbers using a limited gaussian distrbution. The "center" value is always included in the output.
    :param center: the mean value of the Gaussian.
    :param lower_limit: Lower number to sample ( included ).
    :param upper_limit: Highest number to sample ( included ).
    :param num_samples: Number of samples desired ( center included )
    :param std_dev: Standard Deviation of the Gaussian Distribution,
    :return: Set[int]. A set of sampled values ( center included )
    """
    samples = {center}
    while len(samples) < num_samples:
        items = truncnorm.rvs((lower_limit - center) / std_dev, (upper_limit - center) / std_dev, loc=center,
                              scale=std_dev, size=1)
        number = int(np.round(items)[0])
        if number != center:
            samples.add(number)
    return samples


def is_json_invalid(validated_jason: dict) -> bool:
    """
    Checks wether the dict is valid, by checking if it has any empty strings.
    :param validated_jason:  dict to validate.
    :return: bool. True if there are empty values, False instead.
    """
    return any([key for key, value in validated_jason.items() if value == ""])


def process_text(text: str, target_word: str, avg: float, classes_names: Dict[int, str], record_id: str):
    """
    Processes the input parameters for creating a structured JSON string ( see return type ).
    :param text: str. The text to analyze. It contains the word to classify.
    :param target_word: str. The target word to classify in the text.
    :param avg: float. The average classification value given to the target word in the context.
    :param classes_names: Dict[int,str]. The possible classes names mappings.
    :param record_id: The ID of the given record.
    :return: str. A string json of the following structure:
    {
        "text": str, // The untouched text given in input.
        "target_word": str, // The untouched target word given in input.
        "choices": list[str], // A list of possible classifications for the target word.
        // They're chosen randomly using "get_gaussian_samples" function, and then the orer is
        // shuffled.
        "label": int // The index of the class in "choises" correspondign to the "target_word" class.
    }
    """
    choice = round(avg)
    samples = get_gaussian_samples(center=choice, lower_limit=1,
                                   upper_limit=7, num_samples=DISTRACTORS + 1,
                                   std_dev=GAUSSIAN_STD_DEV)
    samples = list(samples)
    random.shuffle(samples)
    label = samples.index(choice)
    samples = [classes_names[x] for x in samples]

    test = {
        "text": text,
        "target_word": target_word,
        "choices": samples,
        "label": label,
        'id': record_id
    }

    return test


def is_record_valid(target: str, text: str, avg: float, classes_numbers: int) -> bool:
    """
    Checks whether the record in the dataset is valid.
    A record is valid if:
        - 1<avg<=classes_numbers
        - "target" is contained only once inside "text"
        - If "target" and "text" are not empty
    :param text: str. The text to analyze. It contains the word to classify.
    :param target: str. The target word to classify in the text.
    :param avg: float. The average classification value given to the target word in the context.
    :param classes_numbers: int. The max number of classes used for classification of "target".
    :return: bool. True if it's valid, False else.
    """
    words = text.split(' ')
    target_occurrences = len([word for word in words if word == target])
    if target_occurrences > 1:
        return False
    return target != '' and text != '' and 1 < avg <= classes_numbers


def create_benchmark():
    """
    Creates the benchmark by reading data from the datasets, processing
    it and writing it to a created benchmark file.
    """

    for dataset_file_path, benchmark_file_path in FILES:

        print("Creating benchmark: ", benchmark_file_path)

        # Opening benchmark file
        with open(benchmark_file_path, "w") as benchmark:
            # Iterating over all the datasets
            record_id = 0
            # Reading from the dataset tsv_file to process information and write it in benchmark file
            with open(dataset_file_path, "r") as tsv:
                print("Reading data from ", dataset_file_path)
                reader = csv.DictReader(tsv, delimiter='\t')

                file_name = os.path.splitext(os.path.basename(dataset_file_path))[0]
                record_number = 0
                for row in reader:
                    target = row["TARGET"]
                    text = row["TEXT"]
                    avg = row.get("AVG") or row["MEAN"]
                    avg = float(avg)
                    if not is_record_valid(target, text, avg, len(CLASSES_NAMES)):
                        continue
                    task_id = f"{file_name}_task-13_{record_number}"
                    record_number = record_number + 1
                    processed_text = process_text(text, target, avg, CLASSES_NAMES, task_id)
                    if is_json_invalid(processed_text):
                        continue
                    line = json.dumps(processed_text)
                    benchmark.write(line + "\n")

    print("Done")


if __name__ == '__main__':
    create_benchmark()
