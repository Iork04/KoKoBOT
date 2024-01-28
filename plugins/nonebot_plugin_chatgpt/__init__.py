import requests
import codecs

from nonebot.adapters.onebot.v11 import Bot, Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, PrivateMessageEvent, GroupMessageEvent
from nonebot import on_command, on_message
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.plugin.model import PluginMetadata

from .func import *

__chatgpt_usage__ = """
[#] 使用#来和ai聊天。
[showmemory] 展示ai的记忆。
[showbalance] 查询key余额。
[clearmemory] 重置记忆。
[setmemory] 给ai重新写入身份。"""
__plugin_meta__ = PluginMetadata(
    name="ai聊天",
    description="一个用额度每天刷新的聊天ai(因为是白嫖的 所以有额度)",
    usage=__chatgpt_usage__,
    type="application",
)

chat = on_message(rule=to_me(), priority=10, block=True)

show_balance = on_command("showbalance",
                          priority=9,
                          aliases={"gpt余额查询"},
                          block=True)

show_memory = on_command("showmemory",
                         priority=8,
                         aliases={"查看记忆", "记忆"},
                         block=True)

memory_clear = on_command("clearmemory",
                          priority=8,
                          aliases={"清除记忆"},
                          block=True)

set_memory = on_command("setmemory",
                        priority=8,
                        aliases={"gpt", "初始记忆", "memory"},
                        block=True)


@chat.handle()
async def _(bot: Bot, event: MessageEvent):
    global cfg, memory

    if isinstance(event, GroupMessageEvent):
        id = event.group_id
    else:
        id = event.user_id

    city = str(event.get_message())
    if 'CQ:image' in city or 'CQ:face' in city:
        await chat.finish("GPT无法识别图片与表情！", at_sender=True)
    try:
        city = f'{str(event.reply.sender.nickname)}:"{event.reply.message}"' + city
    except Exception as e:
        pass

    try:
        response = requests.post(cfg.url,
                                 headers=cfg.headers,
                                 data=make_data(thisinput=city,
                                                thisuser_id=id),
                                 stream=True,
                                 verify=False)
        msg = ""
        decoder = codecs.getincrementaldecoder('utf-8')()
        for chunk in response.iter_content(chunk_size=1):
            try:
                decoded_chunk = decoder.decode(chunk, final=False)
                msg += decoded_chunk
            except UnicodeDecodeError:
                pass  # 解码错误，继续等待后续数据到达

        msg = msg[:-6]
    except Exception as e:
        msg = f"error:{e}"
        chat.finish(msg, at_sender=True)
    memory[id].append(fm("user", city))
    memory[id].append(fm("assistant", msg))
    save()
    await chat.finish(message=(msg), at_sender=True)


@show_balance.handle()
async def _():
    res = get_balance()
    await show_balance.finish(res)


@show_memory.handle()
async def _(event: MessageEvent):
    res = "\n"

    if isinstance(event, GroupMessageEvent):
        id = event.group_id
    else:
        id = event.user_id

    if id in memory and len(memory[id]) > 1:
        for i in range(1, len(memory[id])):
            res += str(memory[id][i]['role']) + ":" + str(
                memory[id][i]['content']) + "\n"
    else:
        await show_memory.finish("我们还没聊过天哦~", at_sender=True)
    await show_memory.finish(res, at_sender=True)


@memory_clear.handle()
async def _(event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        id = event.group_id
    else:
        id = event.user_id

    if id in memory:
        del memory[id]
    await memory_clear.finish(f"id:{id}已清空记忆！")


@set_memory.handle()
async def _(event: MessageEvent, describe: Message = CommandArg()):

    if isinstance(event, GroupMessageEvent):
        id = event.group_id
    else:
        id = event.user_id

    if describe.extract_plain_text().strip():

        memory[id] = [fm("system", describe.extract_plain_text().strip())]
        save()
        await set_memory.finish(f"id:{id}的新身份已经准备好，请at我开始聊天。")
