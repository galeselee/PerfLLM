import asyncio
import numpy as np
import copy
import os
import uuid
from loguru import logger
from hillm.config import SessionConfig
from .request import Request

class Session:
    def __init__(self,
                 request_send=None, 
                 limit_request_num:bool=True,
                 max_request_num:int=1,
                 request_configs=None,
                 request_config_probability=None):
        self.max_request_num = max_request_num
        self.request_send = request_send
        self.limit_request_num = limit_request_num

        self.name = "session-" + str(uuid.uuid1())
        self.request_configs = request_configs
        self.request_config_probability = request_config_probability
        self.io_list = []

        self.client_log_dir = None
        self.log_dir = None
        if self.request_send == None:
            self.request_send = self.default_request_send

    @classmethod
    def from_config(cls, config:SessionConfig):
        ses = cls(
            **config.to_dict(),
        )
        return ses

    def default_request_send(self):
        return np.random.exponential(10)

    def init_client_vars(self, client_log_dir:str):
        self.client_log_dir = client_log_dir + "/"
        self.log_dir = self.client_log_dir + self.name
        os.system(f"mkdir -p {self.log_dir}")

    async def run(self):
        assert len(self.request_configs) != 0

        if self.limit_request_num:
            request_count = 0
            while request_count < self.max_request_num:
                _request_config = np.random.choice(self.request_configs, size=None, p=self.request_config_probability)
                _request = Request.from_config(_request_config)
                _request.init_session_vars(self.log_dir, self.io_list)
                _new_request_wait_time = self.request_send()
                await asyncio.sleep(_new_request_wait_time)
                logger.info("New Request")
                asyncio.create_task(_request.issue())
                request_count += 1
        else:
            while True:
                _new_request_wait_time = self.request_send()
                _request_config = np.random.choice(self.request_configs, size=None, p=self.request_config_probability)
                _request = Request.from_config(_request_config)
                _request.init_session_vars(self.log_dir, self.io_list)
                await asyncio.sleep(_new_request_wait_time)
                logger.info("New Request")
                asyncio.create_task(_request.issue())

