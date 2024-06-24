from dataclasses import dataclass
from typing import Optional
import dataclasses
import numpy as np

class SessionConfig(object):
    def __init__(self,
                 request_send=None,
                 limit_request_num:bool=True,
                 max_request_num:int=1):
        self.request_send = request_send
        self.limit_request_num = limit_request_num
        self.max_request_num = max_request_num
        self.request_configs = []
        self.request_config_probability = []

        if self.request_send == None:
            self.request_send = self.default_request_send

    def default_request_send(self):
        return np.random.exponential(10)

    def to_dict(self):
        return vars(self)

    def _normalization_probability(self):
        _probability = np.array(self.request_config_probability)
        self.request_config_probability = list(_probability / _probability.sum())

    def add_request_config(self, request_config, probability=1):
        self.request_configs.append(request_config)
        self.request_config_probability.append(probability)
        self._normalization_probability()

