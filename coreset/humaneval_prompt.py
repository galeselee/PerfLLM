import json
import argparse
import matplotlib.pyplot as plt 
import numpy as np 
import scipy.stats as stats
import os

# The raw datasets are downloaded from https://github.com/openai/human-eval/tree/master/data
def add_parser_arg(parser):
    parser.add_argument('--data', type=str, nargs="?",
                        help='The path the human eval ',
                        default="/data/benchmarksuite/code/HumanEval.jsonl")
    parser.add_argument('--output', type=str, nargs="?",
                        help='The path the humaneval prompt output file',
                        default="/data/benchmarksuite/prompt/humaneval_prompt.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_parser_arg(parser)
    args = parser.parse_args()
    input_list = []
    output_list = []
    prompt = {}

    filepath = args.data
    with open(filepath, "r") as f:
        for line in f:
            data = json.loads(line)
            input_list.append(data["prompt"])
            output_list.append(data["canonical_solution"])
    
    for idx in range(len(input_list)):
        prompt[idx] = {"input":input_list[idx], "output":output_list[idx]}
    
    
    with open(args.output, "w") as f:
        json.dump(prompt, f)