import json
import argparse
import matplotlib.pyplot as plt 
import numpy as np 
import scipy.stats as stats
import os

# The raw datasets are downloaded from https://github.com/openai/grade-school-math/
def add_parser_arg(parser):
    parser.add_argument('--data', type=str, nargs="?",
                        help='The path the gsm8k path',
                        default="/data/benchmarksuite/math/gsm8k.jsonl")
    parser.add_argument('--output', type=str, nargs="?",
                        help='The path the gsm8k prompt output file',
                        default="/data/benchmarksuite/prompt/gsm8k_prompt.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_parser_arg(parser)
    args = parser.parse_args()
    filepath = args.data
    input_list = []
    output_list = []
    prompt = {}

    with open(filepath, "r") as f:
        for line in f:
            data = json.loads(line)
            input_list.append(data["question"])
            output_list.append(data["answer"])
    
    for idx in range(len(input_list)):
        prompt[idx] = {"input":input_list[idx], "output":output_list[idx]}
    
    with open(args.output, "w") as f:
        json.dump(prompt, f)
    