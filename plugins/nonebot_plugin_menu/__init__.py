from nonebot import on_command
from nonebot import logger
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageSegment, Message

from .func import *

_help = on_command("help", aliases={"帮助", "菜单", "功能"}, priority=0, block=True)

@_help.handle()
async def _(describe: Message = CommandArg()):
    describe = describe.extract_plain_text().strip()
    if describe:
        res = await get_info(describe)
    else:
        res = await get_menu()

    await _help.finish(MessageSegment.image(res))

import nonebot

driver = nonebot.get_driver()

@driver.on_startup
async def startup():
    get_plugin_info()