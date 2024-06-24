from dataclasses import dataclass
from typing import Optional

import dataclasses
import time
import numpy as np

class SuiteConfig(object):
    def __init__(self,
                 client_register=None,
                 limit_client_num:bool=True,
                 max_client_num:int=1,
                 log_dir:str=None):
        self.client_register = client_register
        self.limit_client_num = limit_client_num
        self.max_client_num = max_client_num
        self.log_dir = log_dir
        self.client_configs = []
        self.client_config_probability = []

        if self.client_register == None:
            self.client_register = self.default_client_register

        if self.log_dir == None:
            self.log_dir = "log/suite-" + str(time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime()))

    def default_client_register(self):
        return np.random.exponential(10)

    def to_dict(self):
        return vars(self) 
    
    def _normalization_probability(self):
        _probability = np.array(self.client_config_probability)
        self.client_config_probability = list(_probability / _probability.sum())

    def add_client_config(self, client_config, probability=1):
        self.client_configs.append(client_config)
        self.client_config_probability.append(probability)