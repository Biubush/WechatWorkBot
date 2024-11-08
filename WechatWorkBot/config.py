import config
import os
import random
import string

class Config:
    try:
        WORK_DIR = config.WORK_DIR or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except AttributeError:
        WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        SECRET_KEY = config.SECRET_KEY or ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    except AttributeError:
        SECRET_KEY = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    os.makedirs(WORK_DIR, exist_ok=True)
    JSON_AS_ASCII = False
    try:
        DEBUG = config.DEBUG or False
    except AttributeError:
        DEBUG = False
    try:
        PORT = config.PORT or 44722
    except AttributeError:
        PORT = 44722

