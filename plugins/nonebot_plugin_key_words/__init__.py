from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Message
import random
from nonebot.rule import keyword
from nonebot import get_driver
from nonebot.plugin.model import PluginMetadata

NICKNAME = get_driver().config.nickname

__plugin_meta__ = PluginMetadata(
    name="key_words",
    description="通过关键词触发相应事件",
    usage="自行摸索",
    type="application",
)

fkxqs = on_keyword(
    {"V我50", "vwo50", "v50", "疯狂星期四", "V50", "v我50"},
    priority=10,
)


@fkxqs.handle()
async def _():
    res = random.choice([
        "本群正在对美实施经济制裁，本周不参加疯狂星期四！",
        f"反诈中心{random.sample(NICKNAME,1)[0]}分部提醒您：以疯狂星期四等名义向您索要钱财的均为诈骗！"
    ])
    await fkxqs.finish(res, at_sender=True)
