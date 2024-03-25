# CONcreTEXT

Homepage: https://lablita.github.io/CONcreTEXT/

Download Link: https://osf.io/j4dz3/

Use only the italian part.

Given a sentence along with a target word, we ask participants to propose a system able to assess the concreteness of the target word according to a [1-7] concreteness scale, where 1 stands for fully abstract (e.g., ‘idempotence’) and 7 for maximally concrete (e.g., ‘car’).

## Data

The data come in several `.tsv` files.

## Expected output

Create ```CONcreTEXT-trial.jsonl```, ```CONcreTEXT-test.jsonl```.

Since the correcteness come as an average in [1-7] range, we ask you to take the *floor* or the *ceiling* and thread them [0, 1, 2, 3, 4, 5, 6, 7] as classes, choosing the floor|cealing(avg) as the correct class and take other three as distractors.

If you can you have to rephrase each numerical class in a natural language as indicated by the task descr 1 = "abstract" and 7 = "maximal concrete", try to find out a possible mapping. Try to motivate your choices.

NOTE: this is not a word level task, in the sense present on the slides, here you have to classify a single word for each input sample, given by the task itself.

Each line in your output file must be a JSON object like the one below:

```JSON
{
    "text": str,
    "target_word": str,
    "choices": list[str],
    "label": int
}
```

### Prompts

Create ```prompt.jsonl```

In this file you have to report the prompts you designed for the task. 
Each line in your output file (1 line per prompt) must be a JSON object like the one below (max 5 lines in this file):

```JSON
{
    "prompt": str
}
```

## Deliver format

You have to format your data using JSON Lines standard.

## License

Creative Commons Attribution Non Commercial Share Alike 4.0 International