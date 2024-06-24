from dataclasses import dataclass
from typing import Optional

import dataclasses
import numpy as np

class RequestConfig(object):
    def __init__(self,
                 database,
                 sample_prompt=None, 
                 server_ip:str="0.0.0.0",
                 server_port:int=8000,
                 server_ignore_eos:bool=False,
                 server_max_token:int=8192,
                 server_stream:bool=True,
                 server_temperature:float=0.0,
                 server_api=None):
        self.database = database
        self.sample_prompt = sample_prompt
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_ignore_eos = server_ignore_eos
        self.server_max_token = server_max_token
        self.server_stream = server_stream
        self.server_temperature = server_temperature
        self.server_api = server_api
        if self.sample_prompt == None:
            self.sample_prompt = self.database.random_choice
        if self.server_api == None:
            self.server_api = self.vllm_api

    def to_dict(self):
        #return vars(self)
        return {
                "database":self.database,
                "sample_prompt":self.sample_prompt,
                "server_api":self.server_api
               }

    def vllm_api(self):
        url = f"http://{self.server_ip}:{self.server_port}/generate"
        prompt_key = "prompt"
        input_json = {
            "prompt": "",
            "stream": self.server_stream,
            "ignore_eos": self.server_ignore_eos,
            "max_tokens": self.server_max_token,
            "temperature": self.server_temperature
        }
        
        return url, input_json, prompt_key
