import sys
import os
import json


def read_config():
    """"读取配置"""
    with open("data.json") as json_file:
        config = json.load(json_file)
    return config

print(read_config())