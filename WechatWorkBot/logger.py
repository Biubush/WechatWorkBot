from datetime import datetime
import config
from WechatWorkBot.config import Config
import os
import sys

class Logger:
    def __init__(self):
        """
        日志记录器，有四个级别的日志记录：info, error, warning, debug
        """
        self.log_folder = os.path.join(Config.WORK_DIR, "archives","logs")
        
        try:
            CORP_ID = config.CORP_ID
        except AttributeError:
            self.error("CORP_ID not found in config.py")
            sys.exit()
        try:
            TOKEN = config.TOKEN
        except AttributeError:
            self.error("TOKEN not found in config.py")
            sys.exit()
        try:
            ENCODING_AES_KEY = config.ENCODING_AES_KEY
        except AttributeError:
            self.error("ENCODING_AES_KEY not found in config.py")
            sys.exit()
        try:
            AGENT_ID = config.AGENT_ID
        except AttributeError:
            self.error("AGENT_ID not found in config.py")
            sys.exit()
        try:
            CORP_SECRET = config.CORP_SECRET
        except AttributeError:
            self.error("CORP_SECRET not found in config.py")
            sys.exit()

    def _get_log_file_name(self):
        # 获取当前日期
        now = datetime.now()
        year = now.year
        month = now.month

        # 计算本月的第几个星期
        # 获取当前日期是本月第几天
        day_of_month = now.day
        # 计算本月第几个星期
        week_of_month = (day_of_month - 1) // 7 + 1

        # 格式化输出
        file_name = f"{year}_{month}_week{week_of_month}.log"
        file_path = os.path.join(self.log_folder, file_name)
        file_folder = os.path.dirname(file_path)
        os.makedirs(file_folder, exist_ok=True)
        return file_path

    def info(self, msg):
        msg = repr(msg)[1:-1]  # 去掉首尾的引号
        log_file = self._get_log_file_name()
        with open(log_file, "a", encoding="utf-8") as f:
            content=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|[INFO]|{msg}\n"
            f.write(content)
            print(content)

    def error(self, msg):
        msg = repr(msg)[1:-1]  # 去掉首尾的引号
        log_file = self._get_log_file_name()
        with open(log_file, "a", encoding="utf-8") as f:
            content=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|[ERROR]|{msg}\n"
            f.write(content)
            print(content)

    def warning(self, msg):
        msg = repr(msg)[1:-1]  # 去掉首尾的引号
        log_file = self._get_log_file_name()
        with open(log_file, "a", encoding="utf-8") as f:
            content=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|[WARNING]|{msg}\n"
            f.write(content)
            print(content)

    def debug(self, msg):
        msg = repr(msg)[1:-1]  # 去掉首尾的引号
        log_file = self._get_log_file_name()
        with open(log_file, "a", encoding="utf-8") as f:
            content=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|[DEBUG]|{msg}\n"
            f.write(content)
            print(content)
        
if __name__ == "__main__":
    log=Logger()
    log.info("info")
    log.error("error")
    log.warning("warning")
    log.debug("debug")
