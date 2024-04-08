# %pip install replicate
import json
import os
import random
from typing import Dict, List, Any
from jinja2 import Template

import replicate

######################### Settings #########################################

# The JSONL prompt file, in which each line is a prompt
PROMPTS_FILE = "task-15/prompts.jsonl"
# The JSONL benchmark file containing all the contexts to use to parse the prompts
BENCHMARK_FILE = "task-15/benchmarks/PRELEARN-geometry-pairs_test.jsonl"

# The number of parses to be done per each prompt ( using the benchmark )
PARSES_PER_PROMPT = 1
####################### API TOKENS ###########################################à

os.environ["REPLICATE_API_TOKEN"] = "API_TOKEN"
llama2_70b = "llama2_70b"
llama2_13b = "llama2_70b"


############################################################################à


def parse_prompt(prompt: str, context: Dict[str,Any]) -> str:
    """
    It parses a prompt substituting the context in the brackets ( {{context_1}} ).
    For instance if a prompt is "My name is {{name}} {{last_name}})", and the
    context is: { 'name': 'John', 'last_name'='Smith' }, the resulting prompt will be
    "My name is John Smith".
    :param prompt: str. The prompt template to be parsed.
    :param context: Dict[str,Any]. The context used for parsing.
    :return: str. The parsed prompt.
    """
    template = Template(prompt)
    return template.render(**context)


def load_contexts(file_name: str) -> List[Dict[str, Any]]:
    """
    It loads the benchmark values from a JSONL file.
    :param file_name: The name of the file where the contexts are.
    :return: List[Dict[str, Any]]. The list of dicts from the benchmark file,
    each one with a format dict[name] = value.
    """
    contexts = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            dictionary = json.loads(line)
            contexts.append(dictionary)
    return contexts


def load_prompts(file_name: str) -> List[str]:
    """
    It loads the prompts template from a JSONL file, in which each line has the following
    format: { "prompt" : 'prompt temlate' }
    :param file_name:The name of the file where the context is.
    :return: List[str]. A list of prompts template.
    """
    prompts = []
    with open(file_name, 'r') as file:
        for line in file:
            dictionary = json.loads(line)
            prompts.append(
                dictionary["prompt"]
            )
    return prompts


def parse_prompt_randomly(prompt: str, contexts: List[Dict[str, Any]], count: int) -> List[str]:
    """
    It parses the prompt template with [count] random contexts.
    :param prompt: str. The prompt template to be parsed.
    :param contexts: List[Dict[str,Any]]. The list of contexts used for parsing.
    :param count: int. The count of context to sample randomly ( uniformly ) from "contexts".
    :return: List[str]. The list of parsed templates.
    """
    sampled_contexts = random.sample(contexts, count)
    return [parse_prompt(prompt, context) for context in sampled_contexts]


def test_prompt(prompt: str, contexts: List[Dict]):
    """
    NOT COMPLETED! Need a valid access API Token
    It tests a prompt template with a list of contexes with a LLM API,
    showing the accuracy of the model.
    :param prompt: str. The prompt template to be parsed.
    :param contexts: List[Dict[str,Any]]. The list of contexts used for parsing.
    """
    prompt_outputs = []
    for context in contexts:
        parsed_prompt = parse_prompt(prompt, context)
        output = replicate.run(
            "meta/llama-2-70b-chat",
            input={
                "prompt": parsed_prompt
            },
        )
        prompt_outputs.append(''.join(output))

    print(prompt_outputs)
    # TODO -> Complete if you have a valid API access token


def parse_prompts():
    """
    It parses all the prompts with a number [PARSES_PER_PROMPT]
    of contexts chosen randomly, and they're printed on the screen.
    """
    prompts = load_prompts(PROMPTS_FILE)
    contexts = load_contexts(BENCHMARK_FILE)

    for prompt in prompts:
        print("### Parsing prompt: \n", prompt)
        parsed_prompts = parse_prompt_randomly(prompt, contexts, PARSES_PER_PROMPT)
        print('\n'.join(parsed_prompts))
        print("-----------------------------------------------------------------------------")


if __name__ == '__main__':
    parse_prompts()
