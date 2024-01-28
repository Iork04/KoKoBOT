import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OnebotAdapter  # 避免重复命名

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OnebotAdapter)
nonebot.load_all_plugins(
    [
        # 导入插件
        "plugins.nonebot_plugin_randomnana",
        "plugins.nonebot_plugin_longtu",
        "plugins.nonebot_plugin_herocard",
        "plugins.nonebot_plugin_questionmark",
        "plugins.nonebot_plugin_simplemusic",
        "plugins.nonebot_plugin_chatgpt",
        "plugins.nonebot_plugin_russian",
        "plugins.nonebot_plugin_today_waifu",
        "plugins.nonebot_plugin_fakemsg",
        "plugins.nonebot_plugin_tarot",
        "plugins.nonebot_plugin_who_at_me",
        "plugins.nonebot_plugin_today_in_history",
        "plugins.nonebot_plugin_abstract",
        "plugins.nonebot_plugin_key_words",
        "plugins.nonebot_plugin_answersbook",
        "plugins.nonebot_plugin_emojimix",
        "plugins.nonebot_plugin_ddcheck",
        "plugins.nonebot_plugin_dog",
        "plugins.nonebot_plugin_setu_collection",
        "plugins.nonebot_plugin_memes",
        "plugins.nonebot_plugin_fortune",
        "plugins.nonebot_plugin_menu",
    ],
    [
        # 导入文件夹下所有插件
    ])

if __name__ == "__main__":
    nonebot.run()
