import json
import requests
import pickle
import os

from nonebot.log import logger
from nonebot import get_driver

from .config import *

file_name = "/memory.pkl"
cfg = Config.parse_obj(get_driver().config.dict())
fm = lambda role, content: {"role": role, "content": content}
memory = {}
try:
    with open(cfg.path_chatgpt + file_name, 'rb') as file:
        memory = pickle.load(file)
except Exception:
    memory['默认'] = [
        fm("system", cfg.gpt_identity),
    ]
    try:
        os.makedirs(cfg.path_chatgpt)
    except:
        pass
    with open(cfg.path_chatgpt + file_name, 'wb') as file:
        pickle.dump(memory, file)
memory['默认'] = [
    fm("system", cfg.gpt_identity),
]


def check_len(thisuser_id: str = "") -> bool:

    if (len(memory[thisuser_id]) > cfg.max_massage_len):
        memory[thisuser_id] = memory['默认'].copy()
        return True
    return False


def make_data(thisinput: str = "", thisuser_id: int = None):

    global memory

    if thisuser_id not in memory:
        memory[thisuser_id] = memory['默认'].copy()

    _temp = memory[thisuser_id].copy()
    _temp.append(fm("user", thisinput))
    logger.debug(_temp)
    return {
        "session_id":
        "19c87184-0aba-42df-8e5d-0d3e0e732cbd",  # 改左边
        "content":
        json.dumps(_temp),
        "max_context_length":
        "5",
        "params":
        json.dumps({
            "model": "gpt-3.5-turbo",
            "temperature": 1,
            "max_tokens": 2048,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "max_context_length": 5,
            "voiceShortName": "zh-CN-XiaoxiaoNeural",
            "rate": 1,
            "pitch": 1
        })
    }


def get_balance():
    global cfg
    NowUrl = 'https://x.dogenet.win/api/v1/user/balance'
    response = requests.post(NowUrl, headers=cfg.headers).json()

    logger.info(
        f"'balance', {response['data']['balance']}     'free_balance', {response['data']['free_balance']}"
    )

    return f"balance:{response['data']['balance']}\nfree_balance:{response['data']['free_balance']}"


def save():
    try:
        os.makedirs(cfg.path_chatgpt)
    except:
        pass
    with open(cfg.path_chatgpt + file_name, 'wb') as file:
        pickle.dump(memory, file)
