import os
import sys
import time
import json
import numpy as np
import asyncio
import aiohttp
import random
import copy
import uuid

from loguru import logger
from datetime import datetime
from hillm.config import ClientConfig
from .session import Session

class Client(object):
    def __init__(self,
                 session_start=None,
                 limit_session_num:bool=True,
                 max_session_num:int=1,
                 session_configs=None,
                 session_config_probability=None):
        self.session_start = session_start
        self.limit_session_num = limit_session_num
        self.max_session_num = max_session_num
        if session_start == None:
            self.session_start = self.default_session_start
        
        self.session_configs = session_configs
        self.session_config_probability = session_config_probability

        self.name = "client-" + str(uuid.uuid1())

        self.suite_log_dir = None
        self.log_dir = None
        
    @classmethod
    def from_config(cls, config:ClientConfig):
        cli = cls(
            **config.to_dict(),
        )
        return cli

    def default_session_start(self):
        return np.random.exponential(10)

    def init_suite_vars(self, suite_log_dir):
        self.suite_log_dir = suite_log_dir + "/"
        self.log_dir = self.suite_log_dir + self.name
        os.system(f"mkdir -p {self.log_dir}")

    async def run(self):
        assert len(self.session_configs) != 0

        if self.limit_session_num:
            session_count = 0
            while session_count < self.max_session_num:
                _session_config = np.random.choice(self.session_configs, size=None, p=self.session_config_probability)
                _session = Session.from_config(_session_config)
                _session.init_client_vars(self.log_dir)
                _new_session_wait_time = self.session_start()
                await asyncio.sleep(_new_session_wait_time)
                logger.info("New session")
                asyncio.create_task(_session.run()) 
                session_count += 1
        else:
            while True:
                _session_config = np.random.choice(self.session_configs, size=None, p=self.session_config_probability)
                _session = Session.from_config(_session_config)
                _session.init_client_vars(self.log_dir)
                _new_session_wait_time = self.session_start()
                await asyncio.sleep(_new_session_wait_time)
                logger.info("New session")
                asyncio.create_task(_session.run()) 
   

        