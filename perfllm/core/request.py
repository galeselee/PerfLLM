from .database import Database
from perfllm.config import RequestConfig
from loguru import logger
from perfllm.config import RequestConfig

import aiohttp
import asyncio
import json
import numpy as np
import uuid
import os
import time

class Request(object):
    def __init__(self,
                 database:Database,
                 sample_prompt=None, 
                 server_api=None):
        self.database = database
        self.sample_prompt = sample_prompt
        self.server_api = server_api
        self.name = "request-" + str(uuid.uuid1())
        self.performance_record = {}

        self.log_dir = None
        self.log_path = None
        self.tmp_output = None
        self.session_io_list = None
        self.prompt = ""

    def add_database(self, database):
        self.database = database

    @classmethod
    def from_config(cls, config:RequestConfig):
        req = cls(
            **config.to_dict(),
        )
        return req

    def log_performance(self):
        with open(self.log_path, "w+") as f:
            json.dump(self.performance_record, f)

        os.system(f"rm {self.tmp_output}")

    def init_session_vars(self, log_dir:str, session_io_list):
        self.log_dir = log_dir + "/"
        self.log_path = self.log_dir + self.name +".log"
        self.tmp_output = self.log_dir + self.name + "_output.tmp"
        os.system(f"touch {self.log_path}")
        os.system(f"touch {self.tmp_output}")

        self.session_io_list = session_io_list
        self.prompt = ""
        self.session_io_list.append(self.sample_prompt())
        for text in self.session_io_list:
            self.prompt += text

    async def issue(self):
        if self.log_path == None:
            raise ValueError("Init session related vars is requeired before issue the request")

        timeout = aiohttp.ClientTimeout(total=4*60*60)
        start_time = time.perf_counter()
        self.performance_record["send_time"] = start_time
        self.performance_record["input"] = self.prompt

        with open(self.log_path, "w+") as f:
            f.write(self.prompt + "\n")
            f.write(str(start_time) + "\n")

        first_token_time = None
        complete_time = None
        url, input_json, prompt_key = self.server_api()
        input_json[prompt_key] = self.prompt
        async with aiohttp.ClientSession(timeout = timeout) as session:
            async with session.post(
                url, 
                json=input_json
            ) as resp:
                if resp.status != 200:
                    print(f"Error: {resp.status} {resp.reason}")
                    print(await resp.text())
                    return None, None, None
                
                if True:
                    buffer = b""
                    first_chunk_received = False
                    with open(self.tmp_output, 'wb+') as f:
                        file_write = 11
                        async for chunk in resp.content.iter_any():
                            buffer += chunk
                            if not first_chunk_received:
                                first_token_time = time.perf_counter()
                                self.performance_record["first_token_time"] = first_token_time
                                with open(self.log_path, "a+") as flog:
                                    flog.write(str(first_token_time)+ "\n")
                                first_chunk_received = True
                            while b"\0" in buffer: 
                                json_str, buffer = buffer.split(b"\0", 1)

                            # magic number 3 for vllm
                            f.write(json_str[file_write:len(json_str)-3])
                            file_write = len(json_str) - 3
                        
                    output = json.loads(json_str.decode("utf-8"))  # Decode JSON
                else:
                    output = await resp.json()
                
                complete_time = time.perf_counter()
                self.session_io_list.append(output["text"])
            
            self.performance_record["output"] = output["text"]
            self.performance_record["complete_time"] = complete_time

        self.log_performance()
