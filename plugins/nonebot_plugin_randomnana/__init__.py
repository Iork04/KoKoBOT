import os
import random
from nonebot import on_keyword
from pathlib import Path
from nonebot.adapters.onebot.v11 import MessageSegment

from nonebot.plugin.model import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="随机狗妈",
    description="随机发送一张狗妈表情包",
    usage="[狗/dog] 随机发送一张狗妈表情包。",
    type="application",
)

randomnana = on_keyword({'狗','dog'}, priority=10, block=True)

img_path = os.path.join(os.path.dirname(__file__), "resource")

all_file_name = os.listdir(img_path)


@randomnana.handle()
async def _():
    img_name = random.choice(all_file_name)
    img = Path(img_path) / img_name
    try:
        await randomnana.send(MessageSegment.image(img))
    except:
        await randomnana.send(f"图片文件 {str(img)} 发送失败")
