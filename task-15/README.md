# PRELEARN (Prerequisite Relation Learning)

Homepage: https://sites.google.com/view/prelearn20
Datasets: https://live.european-language-grid.eu/catalogue/corpus/8084/download/

PRELEARN (Prerequisite Relation Learning) is a shared task on concept prerequisite learning which consists of classifying prerequisite relations between pairs of concepts distinguishing between prerequisite pairs and non-prerequisite pairs. For the purposes of this task, prerequisite relation learning is proposed as a problem of binary classification between two distinct concepts (i.e. a concept pair).

## Data

- *PRELEARN_DATASET*: A dataset built upon the AL-CPL dataset (Liang et al. 2018), a collection of binary-labelled concept pairs extracted from textbooks on four domains: data mining, geometry, physics and precalculus. 
- *ITA_prereq-pages*: a “Wikipedia pages file” containing the raw text of the Wikipedia pages referring to the concepts extracted using WikiExtractor on a Wikipedia dump of Jan. 2020.

You will find *-pairs* files where there are different pairs of concepts and a binary label that indicate the causality.

The data comes splitted in a train and test sets, for each task you have to mantain those splits.
The *prereq* contains wikipedia passages relative to the concepts in the *-pairs* files.

## Expected output

We ask you to create four different datasets, one for each domain, *data_mining*, *geometry*, *physics*, and *precalculus*.

### Subtask A - PRELEARN-data_mining

Create ```PRELEARN-data_mining-train.jsonl``` and ```PRELEARN-data_mining-test.jsonl```

Each line in your output file must be a JSON object like the one below:

```JSON
{
    "wikipedia_passage_concept_A": str,
    "concept_A": str,
    "wikipedia_passage_concept_B": str,
    "concept_B": str,
    "choices": list[str]
    "target": int,
}
```

### Subtask A - PRELEARN-geometry

Create ```PRELEARN-geometry-train.jsonl``` and ```PRELEARN-geometry-test.jsonl```

Each line in your output file must be a JSON object like the one below:

```JSON
{
    "wikipedia_passage_concept_A": str,
    "concept_A": str,
    "wikipedia_passage_concept_B": str,
    "concept_B": str,
    "choices": list[int]
    "target": int,
}
```

### Subtask A - PRELEARN-physics

Create ```PRELEARN-physics-train.jsonl``` and ```PRELEARN-physics-test.jsonl```

Each line in your output file must be a JSON object like the one below:

```JSON
{
    "wikipedia_passage_concept_A": str,
    "concept_A": str,
    "wikipedia_passage_concept_B": str,
    "concept_B": str,
    "choices": list[int]
    "target": int,
}
```

### Subtask A - PRELEARN-precalculus

Create ```PRELEARN-precalculus-train.jsonl``` and ```PRELEARN-precalculus-test.jsonl```

Each line in your output file must be a JSON object like the one below:

```JSON
{
    "wikipedia_passage_concept_A": str,
    "concept_A": str,
    "wikipedia_passage_concept_B": str,
    "concept_B": str,
    "choices": list[int]
    "target": int,
}
```

### Prompts

Create ```prompt-data_mining.jsonl```, ```prompt-geometry.jsonl```, ```prompt-physics.jsonl``` and ```prompt-precalculus.jsonl```.

In this file you have to report the prompts you designed for the task. 
Each line in your output file (1 line per prompt) must be a JSON object like the one below (max 5 lines in this file):

```JSON
{
    "prompt": str
}
```

## Deliver format

You have to format your data using JSON Lines standard.