import json
import argparse
import matplotlib.pyplot as plt 
import numpy as np 
import scipy.stats as stats
import os

# The raw datasets are downloaded from https://huggingface.co/datasets/THUDM/LongBench
def add_parser_arg(parser):
    parser.add_argument('--basepath', type=str, nargs="?",
                        help='The path the longbench dir',
                        default="/data/benchmarksuite/longbench/")
    parser.add_argument('--output', type=str, nargs="?",
                        help='The path the longbench prompt output file',
                        default="/data/benchmarksuite/longbench/longbench_prompt.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_parser_arg(parser)
    args = parser.parse_args()
    basepath = args.basepath
    filenames = os.listdir(basepath)
    input_list = []
    output_list = []
    prompt = {}
    for filename in filenames:
        filepath = basepath + filename
        with open(filepath, "r") as f:
            for line in f:
                data = json.loads(line)
                input_list.append(data["context"] + data["input"])
                output_list.append(data["answers"])
    
    for idx in range(len(input_list)):
        prompt[idx] = {"input":input_list[idx], "output":output_list[idx]}
    
    with open(args.output, "w") as f:
        json.dump(prompt, f)
    