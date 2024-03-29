import random

from httpx import AsyncClient, ReadTimeout, ConnectError

from nonebot import on_keyword
from nonebot.exception import FinishedException
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot.log import logger

__version__ = "0.1.0.post4"
__plugin_meta__ = PluginMetadata(
    name="随机龙图",
    description="2024年是龙年...我都准备好了",
    usage="[龙/dragon] 当检测到'龙'or'dragon'的时候发送龙图",
    homepage="https://github.com/Perseus037/nonebot_plugin_longtu",
    type="application",
    config=None,
    supported_adapters={"~onebot.v11"},
)

dragon = on_keyword({"dragon", "龙"}, priority=10, block=True)


@dragon.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent):
    base_url = "https://git.acwing.com/Est/dragon/-/raw/main/"
    extensions = ['.jpg', '.png', '.gif']

    batch_choice = random.choice(['batch1/', 'batch2/', 'batch3/'])

    if batch_choice == 'batch1/':
        selected_image_number = random.randint(1, 500)

    elif batch_choice == 'batch2/':
        selected_image_number = random.randint(501, 1000)

    else:
        selected_image_number = random.randint(1001, 1516)

    for ext in extensions:
        image_url = f"{base_url}{batch_choice}dragon_{selected_image_number}_{ext}"
        try:
            async with AsyncClient() as client:
                resp = await client.get(image_url, timeout=5.0)

            if resp.status_code == 200:
                await dragon.finish(MessageSegment.image(resp.content))

        except FinishedException:
            raise

        except ConnectError:
            logger.error(f"连接错误：无法访问 {image_url}")
            continue

        except ReadTimeout:
            logger.error(f"读取超时：{image_url}")
            continue

        except Exception as e:
            logger.error(f"输出异常：{e}")
            if ext == extensions[-1]:
                await dragon.send("龙龙现在出不来了，稍后再试试吧~")
            break
