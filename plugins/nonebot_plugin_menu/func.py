from nonebot import require, logger

from nonebot.plugin import get_available_plugin_names, get_plugin


require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import text_to_pic

_plugins_info = {}

def get_plugin_info():
    global _plugins_info
    _loader_plugin_names = sorted(list(get_available_plugin_names()))

    for _name in _loader_plugin_names:
            
            item = get_plugin(_name)
          
            if item and item.metadata and item.metadata.type == "application":
                _plugins_info[item.metadata.name] = item.metadata


async def get_menu():
    _content = "功能列表(部分功能仅限群聊,详情/help 插件名)：\n"

    for _name in _plugins_info:
        _content += f"[{_name}]\n"

    return await text_to_pic(_content)

async def get_info(_name: str = '') -> str:
    if _name in _plugins_info:
        _content=f"插件名称：{_name}\n描述：{ _plugins_info[_name].description}\n用法：{_plugins_info[_name].usage}"
    else:
        _content = '404'
   
    return await text_to_pic(_content)


