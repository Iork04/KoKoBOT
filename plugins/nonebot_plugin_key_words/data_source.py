import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Tuple

from nonebot.adapters.onebot.v11 import MessageSegment


async def fkxqs(keyword: str) -> Optional[MessageSegment]:
    res = random.choice(
        ["本群正在对美实施经济制裁，本周不参加疯狂星期四！", '反诈中心CoCo分部提醒您：以疯狂星期四等名义向您索要钱财的均为诈骗！'])

    return MessageSegment.text(res)


class Func(Protocol):

    async def __call__(self, keyword: str) -> Optional[MessageSegment]:
        ...


@dataclass
class Source:
    name: str
    keywords: Tuple[str, ...]
    func: Func


sources = [Source("疯狂星期四", ("vwo50", "v50", "V我50", "V50", "v我50"), fkxqs)]
