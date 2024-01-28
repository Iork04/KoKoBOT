import re
import httpx
import random
import nonebot

from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import ArgStr
from nonebot.permission import SUPERUSER
from nonebot import on_command, on_endswith
from nonebot.plugin.model import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, Bot
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN

from .utils import *

__dog_usages__ = """
[一言]  名人名言。
[讲个笑话]  随机讲个笑话。
[文案/语录]  指定某个主题的文案。
[开启/关闭文案] 开启或者关闭此功能(GROUP_ADMIN)。"""
__plugin_meta__ = PluginMetadata(
    name="舔狗日记",
    description="随机返回舔狗日记和其它文案...",
    usage=__dog_usages__,
    type="application",
    homepage="https://github.com/Reversedeer/nonebot_plugin_dog",
    supported_adapters={"onebot.v11"},
    extra={
        "author": "Reversedeer",
        "version": "0.2.9",
        "priority": 10,
    },
)


openstats = on_endswith("文案",
                        permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
                        priority=10,
                        block=True)

dog_matcher = on_command("舔狗日记", aliases={"舔狗嘤嘤嘤"}, priority=1, block=True)

laugh_matcher = on_command("讲个笑话", aliases={"说个笑话"}, priority=10, block=True)

hitokoto_matcher = on_command("一言", aliases={"一言"}, priority=10, block=True)

wenan_matcher = on_command("文案", aliases={"语录"}, priority=10, block=True)

@dog_matcher.handle()
async def dog(event: GroupMessageEvent, matcher: Matcher):  # 定义异步函数 dog
    if not (await check_group_allow(str(event.group_id))):
        await dog_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()  # 获取用户id
    try:
        cd = event.time - dog_CD_dir[uid]  # 计算cd
    except KeyError:
        cd = dog_cd + 1  # 没有记录则cd为cd_time+1
    if cd > dog_cd:  # 记录cd
        dog_CD_dir.update({uid: event.time})
        urls = [
            "https://api.mxycn.cn/api/tgrj.php",
            "https://api.oick.cn/dog/api.php"
        ]
        url = random.choice(urls)
        try:
            # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response_text = response.text
        except Exception as error:
            await dog_matcher.finish(MessageSegment.text(str(error)))
        await matcher.finish(MessageSegment.text(response_text.strip()),
                             block=True)
    else:
        await dog_matcher.finish(
            MessageSegment.text(f"不要深情了喵，休息{dog_cd - cd:.0f}秒后再找我喵~"),
            at_sender=True,
            block=True)


@laugh_matcher.handle()
async def laugh(event: GroupMessageEvent, matcher: Matcher):  # 定义异步函数 laugh
    if not (await check_group_allow(str(event.group_id))):
        await dog_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()  # 获取用户id
    try:
        cd = event.time - laugh_CD_dir[uid]  # 计算cd
    except KeyError:
        cd = laugh_cd + 1  # 没有记录则cd为cd_time+1
    if cd > laugh_cd:  # 记录cd
        laugh_CD_dir.update({uid: event.time})
        try:
            # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.mxycn.cn/api/qwxh.php"
                                            )
                response_text = response.text
        except Exception as error:
            await laugh_matcher.finish(MessageSegment.text(str(error)))
        response_text = re.sub(r'。。\\n', '\n', response_text)
        response_text = response_text.replace('。。', '')
        await matcher.finish(MessageSegment.text(response_text.strip()),
                             block=True)
    else:
        await laugh_matcher.finish(
            MessageSegment.text(f"我在准备更精彩的笑话喵，等待{laugh_cd - cd:.0f}秒后再找我喵~"),
            at_sender=True,
            block=True)


@hitokoto_matcher.handle()
async def hitokoto(event: GroupMessageEvent,
                   matcher: Matcher):  # 定义异步函数hitokoto
    if not (await check_group_allow(str(event.group_id))):
        await dog_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()  # 获取用户id
    try:
        cd = event.time - hitokoto_CD_dir[uid]  # 计算cd
    except KeyError:
        # 没有记录则cd为cd_time+1
        cd = hitokoto_cd + 1
    if cd > hitokoto_cd:    # 记录cd
        hitokoto_CD_dir.update({uid: event.time})
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=e&c=f&c=j")
        except Exception as error:
            await hitokoto_matcher.finish(MessageSegment.text("获取一言失败"),
                                          at_sender=True,
                                          block=True)
        data = response.json()
        msg = data["hitokoto"]
        add = ""
        if works := data["from"]:
            add += f"《{works}》"
        if from_who := data["from_who"]:
            add += f"{from_who}"
        if add:
            msg += f"\n——{add}"
        await matcher.finish(msg)
    else:
        await laugh_matcher.finish(
            MessageSegment.text(f"休息 {hitokoto_cd - cd:.0f}秒后才能再使用喵~"),
            at_sender=True,
            block=True)


@wenan_matcher.handle()
async def wenan(event: GroupMessageEvent, matcher: Matcher):  # 定义异步函数wenan
    if not (await check_group_allow(str(event.group_id))):
        await wenan_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()  # 获取用户id
    try:
        cd = event.time - wenan_CD_dir[uid]  # 计算cd
    except KeyError:
        cd = wenan_cd + 1  # 没有记录则cd为cd_time+1
    if cd > wenan_cd:  # 记录cd
        wenan_CD_dir.update({uid: event.time})
        try:
            # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.mxycn.cn/api/sgyl.php"
                                            )
                response_text = response.text
        except Exception as error:
            await laugh_matcher.finish(MessageSegment.text(str(error)))
        await matcher.finish(MessageSegment.text(response_text.strip()),
                             block=True)
    else:
        await laugh_matcher.finish(
            MessageSegment.text(f"文案准备中喵，等待{wenan_cd - cd:.0f}秒后再找我喵~"),
            at_sender=True,
            block=True)


@openstats.handle()
async def _(event: GroupMessageEvent):
    gid = str(event.group_id)  # 群号
    # 获取用户输入的参数
    command = event.message.extract_plain_text().replace("文案", "")
    if command == "开启":
        if gid in groupdata:
            groupdata[gid]["allow"] = True
        else:
            groupdata.update({gid: {"allow": True}})
        write_group_data()
        await openstats.finish("功能已开启喵~")
    elif "关闭" in command:
        if gid in groupdata:
            groupdata[gid]["allow"] = False
        else:
            groupdata.update({gid: {"allow": False}})
        write_group_data()
        await openstats.finish("功能已禁用喵~")
    else:
        return

