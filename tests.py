# %pip install replicate
import json
import os
import random
from typing import Dict, List
from jinja2 import Template

import replicate

PROMPTS_FILE = "task-15/prompts.jsonl"
BENCHMARK_FILE = "task-15/benchmarks/PRELEARN-geometry-pairs_test.jsonl"

os.environ["REPLICATE_API_TOKEN"] = "API_TOKEN"
llama2_70b = "llama2_70b"
llama2_13b = "llama2_70b"


def parse_prompt(prompt, context) -> str:
    print(prompt)
    template = Template(prompt)
    return template.render(**context)


def load_contexts(file_name) -> List[Dict]:
    contexts = []
    with open(file_name, 'r',encoding='utf-8') as file:
        for line in file:
            dictionary = json.loads(line)
            contexts.append(dictionary)
    return contexts


def load_prompts(file_name) -> List[str]:
    prompts = []
    with open(file_name, 'r') as file:
        for line in file:
            dictionary = json.loads(line)
            prompts.append(
                dictionary["prompt"]
            )
    return prompts


def parse_prompt_randomly(prompt: str, contexts: List[Dict], count: int):
    sampled_contexts = random.sample(contexts, count)
    return [parse_prompt(prompt, context) for context in sampled_contexts]


def test_prompt(prompt: str, contexts: List[Dict]):
    prompt_outputs = []
    for context in contexts:
        parsed_prompt = parse_prompt(prompt, context)
        print(parsed_prompt)
        output = replicate.run(
            "meta/llama-2-70b-chat",
            input={
                "prompt": parsed_prompt
            },
        )
        prompt_outputs.append(''.join(output))

    print(prompt_outputs)
    # TODO -> Complete if you have a valid API access token


def evaluate_prompts():
    prompts = load_prompts(PROMPTS_FILE)
    contexts = load_contexts(BENCHMARK_FILE)

    for prompt in prompts:
        parsed_prompts = parse_prompt_randomly(prompt, contexts, 10)
        print('\n'.join(parsed_prompts))


if __name__ == '__main__':
    evaluate_prompts()
