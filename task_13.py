import os.path
import random, json
from typing import Set, Dict

import numpy as np
import csv
from scipy.stats import truncnorm

######################### Settings #########################################

# The name of the classes given for the word classification
CLASSES_NAMES = {
    1: 'totalmente astratta',
    2: "abbastanza astratta",
    3: "parzialmente astratta",
    4: "semiconcreta",
    5: "parzialmente concreta",
    6: "abbastanza concreta",
    7: "totalmente concreta"
}

# The Gaussian Standard Deviation used for sampling of the classes
GAUSSIAN_STD_DEV = 2
# Number of  distractors to create
DISTRACTORS = 3

# Files of the Datasets To Process
TSV_FILE_PATHS = [
    "task-13/CONcreTEXT_trial_IT.tsv",
    "task-13/CONcreTEXT_test_IT.tsv",

]

# File of the benchmark to create
BENCHMARK_FILE_PATH = "task-13/benchmark.jsonl"


##########################################################################

def get_gaussian_samples(center: int, lower_limit: int, upper_limit, num_samples: int, std_dev: float) -> Set[int]:
    """
    Samples some integer numbers using a gaussian distrbution. The "center" value is always included in the output.
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

def is_json_invalid(validated_jason: dict):
    """
    :param validated_jason: Checks for empty values.
    :return: bool. True if there are empty values, False instead.
    """
    return any([key for key, value in validated_jason.items() if value == ""])

def process_text(text: str, target_word: str, avg: float, classes_names: Dict[int, str], record_id: str):
    """
    Processes a single text line from the dataset, creating a JSON string with the important values.
    :param text: str. The text to analyze. It contains the word to classify.
    :param target_word: str. The target word to classify in the text.
    :param avg: float. The average classification value given to the target word in the context.
    :param classes_names: Dict[int,str]. The possible classes names mappings.
    :param record_id: The ID of the given record.
    :return: str. A string json of the following structure.

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


def is_record_valid(target: str, text: str, avg: float, classes_numbers: int):
    return target != '' and text != '' and 1 < avg <= classes_numbers


def create_benchmark():
    """
    Creates the benchmark by reading data from the datasets, processing
    it and writing it to the benchmark file.
    """
    print("Creating benchmark: ", BENCHMARK_FILE_PATH)

    # Opening benchmark file
    with open(BENCHMARK_FILE_PATH, "w") as benchmark:
        # Iterating over all the datasets
        record_id = 0
        for tsv_file in TSV_FILE_PATHS:
            # Reading from the dataset tsv_file to process information and write it in benchmark file
            with open(tsv_file, "r") as tsv:
                print("Reading data from ", tsv_file)
                reader = csv.DictReader(tsv, delimiter='\t')

                file_name = os.path.splitext(os.path.basename(tsv_file))[0]
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
