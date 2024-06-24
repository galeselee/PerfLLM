from dataclasses import dataclass
from typing import Optional
import dataclasses
import numpy as np

class ClientConfig(object):
    def __init__(self,
                 session_start=None,
                 limit_session_num:bool=True,
                 max_session_num:int=1):
        self.session_start = session_start
        self.limit_session_num = limit_session_num
        self.max_session_num = max_session_num
        self.session_configs = []
        self.session_config_probability = []

        if self.session_start == None:
            self.session_start = self.default_session_start

    def default_session_start(self):
        return np.random.exponential(10)

    def to_dict(self):
        return vars(self)

    def _normalization_probability(self):
        _probability = np.array(self.session_config_probability)
        self.session_config_probability = list(_probability / _probability.sum())

    def add_session_config(self, session_config, probability=1):
        self.session_configs.append(session_config)
        self.session_config_probability.append(probability)
        self._normalization_probability()
