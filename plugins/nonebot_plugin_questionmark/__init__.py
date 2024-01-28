import random

from nonebot import on_regex, get_driver
from nonebot.plugin import PluginMetadata
from nonebot.params import RegexStr

from .config import *

from nonebot.adapters.onebot.v11 import GroupMessageEvent as Event

__plugin_meta__ = PluginMetadata(
    name="反转符号?",
    description="反转？！i",
    usage="自行摸索",
    homepage="",
    type="application",
    supported_adapters={"~onebot.v11"},
)

cfg = Config.parse_obj(get_driver().config.dict())


async def trigger_rule(event: Event) -> bool:
    if event.group_id not in cfg.qm_enable_groups and "all" not in cfg.qm_enable_groups:
        return False
    return random.random() <= cfg.qm_trigger_rate


question = on_regex(r"^([?？¿!！¡\s]+)$",
                    priority=10,
                    block=True,
                    rule=trigger_rule)


@question.handle()
async def _(rgx: str = RegexStr()):
    mark = rgx \
        .replace("¿", "d").replace("?", "¿").replace("？", "¿").replace("d", "?") \
        .replace("¡", "d").replace("!", "¡").replace("！", "¡").replace("d", "!")
    await question.finish(mark)
