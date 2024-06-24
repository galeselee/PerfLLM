from .client import Client
from .database import Database
from hillm.config import SuiteConfig

import sys
import asyncio
import os
import time
import math
import random
from loguru import logger
import copy
import numpy as np

class Suite(object):
    def __init__(self,
                 client_register=None,
                 limit_client_num:bool=True,
                 max_client_num:int=1,
                 log_dir:str=None,
                 client_configs=None,
                 client_config_probability=None):
        self.client_register = client_register
        self.limit_client_num = limit_client_num
        self.max_client_num = max_client_num
        self.log_dir = log_dir
        self.client_configs = client_configs
        self.client_config_probability = client_config_probability
        
        if client_register == None:
            self._client_register = self.default_client_register

    @classmethod
    def from_config(cls, config:SuiteConfig):
        sui = cls(
            **config.to_dict(),
        )
        return sui

    def default_client_register(self):
        return np.random.exponential(10)

    async def run(self):
        assert len(self.client_configs) != 0

        if self.limit_client_num == True:
            client_count = 0
            while client_count < self.max_client_num:
                _client_config = np.random.choice(self.client_configs, size=None, p=self.client_config_probability)
                _client = Client.from_config(_client_config)
                _client.init_suite_vars(self.log_dir)
                _new_client_wait_time = self.client_register()
                await asyncio.sleep(_new_client_wait_time)
                logger.info("Generate a client")
                asyncio.create_task(_client.run())
                client_count += 1
        else:
            while True:
                _client_config = np.random.choice(self.client_configs, size=None, p=self.client_config_probability)
                _client = Client.from_config(_client_config)
                _client.init_suite_vars(self.log_dir)
                _new_client_wait_time = self.client_register()
                await asyncio.sleep(_new_client_wait_time)
                logger.info("Generate a client")
                asyncio.create_task(_client.run())
        await asyncio.sleep(sys.maxsize)

    def benchmark(self):
        asyncio.run(self.run())

