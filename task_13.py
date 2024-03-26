import random, json

import numpy as np
import csv
from scipy.stats import truncnorm

######################### Settings #########################################
CHOICES_MAPPING = {
    1: '1',
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7"
}

GAUSSIAN_STD_DEV = 2
TSV_FILE_PATH = "task-13/CONcreTEXT_trial_IT.tsv"
BENCHMARK_FILE_PATH = "task-13/benchmark.jsonl"
APPEND = True
DISTRACTORS = 3


##########################################################################

def get_gaussian_samples(center: int, lower_limit: int, upper_limit, num_samples: int, std_dev: float):
    samples = {center}
    while len(samples) < num_samples:
        items = truncnorm.rvs((lower_limit - center) / std_dev, (upper_limit - center) / std_dev, loc=center,
                              scale=std_dev, size=1)
        number = int(np.round(items)[0])
        if number != center:
            samples.add(number)
    return samples


def process_test(target: str, text: str, avg: float):
    """
    :param target:
    :param text:
    :param avg:
    :return:

    {
        "text": str,
        "target_word": str,
        "choices": list[str],
        "label": int
    }
    """
    choice = round(avg)
    samples = get_gaussian_samples(center=choice, lower_limit=0,
                                   upper_limit=7, num_samples=DISTRACTORS + 1,
                                   std_dev=GAUSSIAN_STD_DEV)
    samples = list(samples)
    random.shuffle(samples)
    label = samples.index(choice)

    test = {
        "text": text,
        "target_word": target,
        "choices": samples,
        "label": label
    }

    return json.dumps(test)


if __name__ == '__main__':
    print("Creating benchmark: ", BENCHMARK_FILE_PATH)
    if APPEND:
        writing_mode = 'a'
        print("Using 'append' mode")
    else:
        writing_mode = 'w'
        print("Using 'overwrite' mode")

    print("Reading data from ", TSV_FILE_PATH)
    with open(TSV_FILE_PATH, 'r') as tsv, open(BENCHMARK_FILE_PATH, writing_mode) as benchmark:
        # Create a reader object using the DictReader class to read TSV file
        reader = csv.DictReader(tsv, delimiter='\t')
        # Iterate through each row in the TSV file
        for row in reader:
            target = row["TARGET"]
            text = row["TEXT"]
            avg = row.get("AVG") or row["MEAN"]
            line = process_test(target, text, float(avg))
            benchmark.write(line + "\n")

    print("Done")
