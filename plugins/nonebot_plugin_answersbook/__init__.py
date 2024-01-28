import random
from pathlib import Path

from nonebot import on_endswith, on_startswith
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.matcher import Matcher
from nonebot.plugin.model import PluginMetadata

import json

__answersbook_usage__ ="""
example:翻看答案 今天怎么样"""
__plugin_meta__ = PluginMetadata(
    name="答案之书",
    description="任何事物都会有答案",
    usage=__answersbook_usage__,
    type="application",
)

answers_path = Path(__file__).parent / "answersbook.json"
answers = json.loads(answers_path.read_text("utf-8"))


def get_answers():
    key = random.choice(list(answers))
    return answers[key]["answer"]


answers_starts = on_startswith("翻看答案")
answers_ends = on_endswith("翻看答案")


@answers_starts.handle()
@answers_ends.handle()
async def answersbook(event: GroupMessageEvent, matcher: Matcher):
    msg = event.message.extract_plain_text().replace("翻看答案", "")
    if not msg:
        await matcher.finish("你想问什么问题呢？")
    answer = get_answers()
    await matcher.send(answer, at_sender=True)
