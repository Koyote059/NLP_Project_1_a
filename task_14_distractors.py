import json

from typing import Any, Dict, List, Tuple

FILE_NAME = "task-14/dataset.json"


def load_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Load a file containing a list of JSON objects into memory.
    :param file_path: str. The path of the file to load.
    Returns: List[Dict[str, Any]]: A list of dictionaries if loading is successful.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return data
        else:
            raise TypeError("The file does not contain a list of JSON dictionaries.")


def count_common_words(first_dict: Dict[str, Any], second_dict: Dict[str, Any]) -> int:
    count = 0
    for first_elem in first_dict.values():
        for second_elem in second_dict.values():
            if first_elem == second_elem:
                count += 1
    return count


def extract_similar_solutions(element: Dict[str, Any], dataset: List[Dict[str, Any]]) -> List[Tuple[str, int]]:
    """
    Extracts similair solutions to a given word. A solution is considered "similair" if
    in the same Dataset if the two records containing those are similair.
    We deem two records as "similar" if they share at least one hint word.
    Also, the degree of similarity is the number of the common hint words the two
    records have.
    :return List[Tuple[str, int]]. A list of tuple in the following
     format: (similair solution, degree of similarity)
    """
    possible_solutions: List[Tuple[str, int]] = []
    for item in dataset:
        if item == element:
            continue
        common_words = count_common_words(item, element)
        if common_words > 0:
            possible_solutions.append((item["solution"], common_words))
    return possible_solutions


"""
Initially, we've tried to extract distractors by trying to extrapolate similarity of two
solutions from the same dataset. 
We consider two solutions "similair" if the records containing them are also similari.
We deem two records as "similar" if they share at least one hint word.
Also, the degree of similarity is the number of the common hint words the two
records have.
Unfortunately all of the similair solutions didn't have a degree of similarity greater than 1, 
probably due to the very limited size of the dataset ( only 300 records ).
So we've opted to try different alternatives.
"""


def check_distractors():
    """
    Trying to extrapolate distractors by looking for similair words,
    trying to measure similarity from the same Dataset.
    :return:
    """
    print("Loading dataset: ", FILE_NAME)
    dataset = load_json(FILE_NAME)
    print("The dataset has ", len(dataset), " elements.")
    for element in dataset:
        solution = element["solution"]
        similar_solutions = extract_similar_solutions(element, dataset)
        if len(similar_solutions) == 0:
            print("There are no similair solution for: ", solution)
        else:
            print("Some similair solutions for: '", solution, "' are:\n", similar_solutions)


if __name__ == '__main__':
    check_distractors()
