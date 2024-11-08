import re
from functools import wraps

# 处理消息回复的装饰器字典，分别存储两种处理方法
re_handlers = {}
contain_handlers = {}

def re_method(regex):
    """
    装饰器：用于处理匹配指定正则表达式的消息
    :param regex: 正则表达式
    """
    def decorator(func):
        # 将函数保存到re_handlers字典中
        re_handlers[regex] = func
        @wraps(func)
        def wrapper(msg):
            return func(msg)
        return wrapper
    return decorator

def contain_method(keyword):
    """
    装饰器：用于处理包含指定关键词的消息
    :param keyword: 关键词字符串
    """
    def decorator(func):
        # 将函数保存到contain_handlers字典中
        contain_handlers[keyword] = func
        @wraps(func)
        def wrapper(msg):
            return func(msg)
        return wrapper
    return decorator

def handle_message(msg):
    """
    处理接收到的消息，根据正则或包含装饰器提供的条件匹配消息并触发回复。
    :param msg: 接收到的消息内容
    :return: 返回回复的消息
    """
    # 正则匹配
    for regex, handler in re_handlers.items():
        if re.match(regex, msg['content']):
            return handler(msg)
    
    # 关键词包含匹配
    for keyword, handler in contain_handlers.items():
        if keyword in msg['content']:
            return handler(msg)
    
    # 如果没有匹配任何消息，返回None
    return None