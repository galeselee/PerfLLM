import json
import random

from pathlib import Path
from transformers import AutoTokenizer
from hillm.config import DBConfig
from typing import Optional

class Database(object):
    def __init__(self, 
                 datafile:str, 
                 seed:Optional[int]=0, 
                 enable_token_num:bool=False,
                 model:str=None):
        self.datafile = datafile
        self.enable_token_num = enable_token_num
        self.model = model
        self.seed = seed

        self.max_key = 0
        self.data = self.load_data()
        self.tokens = None

        if self.enable_token_num and self.model == None:
            raise ValueError("Enable database token num, should provide a tokenizer")

        if self.enable_token_num:
            if not Path(self.model).is_dir():
                raise ValueError("model path must be a local directory")
            self._get_token_num()

        random.seed(self.seed)

    @classmethod
    def from_config(cls, config:DBConfig):
        db = cls(
            **config.to_dict(),
        )
        return db

    def load_data(self):
        data = {}
        if isinstance(self.datafile, str):
            try:
                with open(self.datafile, "r") as f:
                    tmp_data = json.load(f)
                    for key in tmp_data.keys():
                        data[self.max_key] = tmp_data[key]
                        self.max_key += 1
            except:
                raise ValueError(f"Error while load {self.datafile}")
        else:
            assert isinstance(self.datafile, list)
            for file in self.datafile:
                assert Path(file).is_file()
                try:
                    with open(file, "r") as f:
                        tmp_data = json.load(f)
                    for key in tmp_data.keys():
                        data[self.max_key] = tmp_data[key]
                        self.max_key += 1
                except:
                    raise ValueError(f"Error while load {file}")
        return data

    def get_token_num(self):
        if not self.enable_token_num:
            raise ValueError(f"Token num has been disabled")
        return self.tokens

    def get_data(self):
        return self.data

    def _get_token_num(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model)
        if self.tokens != None:
            return self.tokens
        self.tokens = {}
        for key, value in self.data.items():
            self.tokens[key] = {}
            self.tokens[key]["input"] = len(tokenizer(value["input"])["input_ids"])
            self.tokens[key]["output"] = len(tokenizer(value["output"])["input_ids"])
        
        return self.tokens
    
    def random_choice(self):
        random_key = random.randint(0, self.max_key)
        return self.data[random_key]["input"]
        
