import json
import argparse
import matplotlib.pyplot as plt 
import numpy as np 
import scipy.stats as stats
import os

# The raw datasets are downloaded from https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/
def add_parser_arg(parser):
    parser.add_argument('--data_part1', type=str, nargs="?",
                        help='The path the shareGPT sg_90k_part1_html_clean json file',
                        default="/data/benchmarksuite/sharegpt/sg_90k_part1_html_cleaned.json")
    parser.add_argument('--data_part2', type=str, nargs="?",
                        help='The path the shareGPT sg_90k_part2_html_clean json file',
                        default="/data/benchmarksuite/sharegpt/sg_90k_part2_html_cleaned.json")
    parser.add_argument('--output', type=str, nargs="?",
                        help='The path the shareGPT conversation output file',
                        default="/data/benchmarksuite/sharegpt/sharegpt_prompt.json")
    parser.add_argument("--answer", type=bool,
                        help="The flag to determined the output if w/o answer", 
                        default=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_parser_arg(parser)
    args = parser.parse_args()
    data_part1 = args.data_part1
    data_part2 = args.data_part2
    with open(data_part1) as json_data:
        sharedGPT_json = json.load(json_data)
        json_data.close()
    
    prompts = []
    answers = []
    for data in sharedGPT_json:
        for message_idx in range(len(data['conversations'])):
            if data['conversations'][message_idx]["from"] == "human":
                try:
                    if data['conversations'][message_idx+1]["from"] == "gpt":
                        prompts.append(data['conversations'][message_idx]["value"])
                except:
                    continue
            elif data['conversations'][message_idx]["from"] == "gpt":
                message_idx_previous = max(message_idx-1, 0)
                try:
                    if data['conversations'][message_idx_previous]["from"] == "human":
                        answers.append(data['conversations'][message_idx]["value"])
                except:
                    continue

    with open(data_part2) as json_data:
        sharedGPT_json = json.load(json_data)
        json_data.close()

    for data in sharedGPT_json:
        for message_idx in range(len(data['conversations'])):
            if data['conversations'][message_idx]["from"] == "human":
                try:
                    if data['conversations'][message_idx+1]["from"] == "gpt":
                        prompts.append(data['conversations'][message_idx]["value"])
                except:
                    continue
            elif data['conversations'][message_idx]["from"] == "gpt":
                message_idx_previous = max(message_idx-1, 0)
                try:
                    if data['conversations'][message_idx_previous]["from"] == "human":
                        answers.append(data['conversations'][message_idx]["value"])
                except:
                    continue

    assert len(answers) == len(prompts)
    json_dict = {}
    for num in range(len(prompts)):
        json_dict[num] = {}
        json_dict[num]["input"] = prompts[num]
        if args.answer:
            json_dict[num]["output"] = answers[num]
    
    with open(args.output, "w") as f:
        json.dump(json_dict, f)