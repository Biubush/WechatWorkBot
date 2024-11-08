from WechatWorkBot.msg_decorator import *

"""
你可以在这里定义你的消息处理函数
有两种方式定义消息处理函数：
1. 正则表达式方式：使用@re_method装饰器，传入一个正则表达式，当用户发送的消息匹配该正则表达式时，将调用该函数处理消息
2. 包含方式：使用@contain_method装饰器，传入一个字符串，当用户发送的消息包含该字符串时，将调用该函数处理消息
"""

@re_method(r'你好|hi')
def handle_greeting(msg):
    user = msg['from_user']
    return f"你好，{user}!"

@contain_method("帮助")
def handle_help(msg):
    user = msg['from_user']
    return f"{user}，需要帮助吗？我在这里为你提供帮助！"