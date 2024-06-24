import argparse
import sys
import os
import json
import asyncio
import perfllm
from loguru import logger
from .util import example_parser_arg

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    example_parser_arg(parser)
    args = parser.parse_args()

    dbcfg = perfllm.DBConfig.from_cli_args(args)
    database = perfllm.Database.from_config(dbcfg)

    requestcfg = perfllm.RequestConfig(database=database, server_port=args.server_port)
    sessioncfg = perfllm.SessionConfig()
    clientcfg = perfllm.ClientConfig()
    suitecfg = perfllm.SuiteConfig()

    sessioncfg.add_request_config(requestcfg)
    clientcfg.add_session_config(sessioncfg)
    suitecfg.add_client_config(clientcfg)
    suite = perfllm.Suite.from_config(suitecfg)
    suite.benchmark()
