from flask import Blueprint, jsonify,request
import urllib
import hashlib
import base64
import struct
import xml.etree.ElementTree as ET
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import requests
import time
from WechatWorkBot.msg_handler import handle_message
from WechatWorkBot.logger import Logger
import sys

# 创建一个蓝图
api_bp = Blueprint('api', __name__)

# 缓存access_token
ACCESS_TOKEN = None
EXPIRES_AT = 0

logger=Logger()
try:
    from config import TOKEN, ENCODING_AES_KEY, CORP_ID, CORP_SECRET, AGENT_ID
except ImportError:
    logger.error("Key variables not found in config.py")
    sys.exit()

def get_access_token():
    global ACCESS_TOKEN, EXPIRES_AT

    # 检查是否已经获取过access_token且未过期
    current_time = time.time()
    if ACCESS_TOKEN and current_time < EXPIRES_AT:
        return ACCESS_TOKEN

    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    params = {
        'corpid': CORP_ID,
        'corpsecret': CORP_SECRET
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result.get('errcode') == 0:
            ACCESS_TOKEN = result.get('access_token')
            EXPIRES_AT = current_time + result.get('expires_in') - 600
            return ACCESS_TOKEN
        else:
            raise Exception(f"Failed to get access_token: {result.get('errmsg')}")
    else:
        raise Exception(f"Request failed with status code {response.status_code}")

def check_signature(token, timestamp, nonce, echostr, signature):
    # 生成签名并验证
    sort_str = ''.join(sorted([token, timestamp, nonce, echostr]))
    generated_signature = hashlib.sha1(sort_str.encode('utf-8')).hexdigest()
    return generated_signature == signature

def decrypt_message(echostr, encoding_aes_key):
    # Base64解码
    decoded_echostr = base64.b64decode(echostr)
    
    # Base64解码EncodingAESKey
    aes_key = base64.b64decode(encoding_aes_key + '===')

    # AES解密
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_key[:16])
    decrypted_data = unpad(cipher.decrypt(decoded_echostr), AES.block_size)
    
    # 去除16字节随机字符串和4字节的消息长度
    pad_len = 16
    msg_len = struct.unpack('>I', decrypted_data[pad_len:pad_len+4])[0]
    msg = decrypted_data[pad_len+4:pad_len+4+msg_len]
    return msg.decode('utf-8')

def decrypt_post_data(data, encoding_aes_key):
    try:
        # 解析XML请求数据
        root = ET.fromstring(data)
        encrypt = root.find('Encrypt').text

        # Base64解码
        encoded_encrypt = base64.b64decode(encrypt)

        # Base64解码EncodingAESKey
        aes_key = base64.b64decode(encoding_aes_key + '===')

        # AES解密
        cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_key[:16])
        decrypted_data = unpad(cipher.decrypt(encoded_encrypt), AES.block_size)
        
        # 去除16字节随机字符串和4字节的消息长度
        pad_len = 16
        msg_len = struct.unpack('>I', decrypted_data[pad_len:pad_len+4])[0]
        msg = decrypted_data[pad_len+4:pad_len+4+msg_len]
        return msg.decode('utf-8')
    except Exception as e:
        raise ValueError('Decryption failed') from e

def send_text_message(to_user, content):
    """
    发送文本消息到企业微信
    """
    access_token = get_access_token()  # 使用获取到的access_token
    url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
    headers = {'Content-Type': 'application/json'}
    data = {
        "touser": to_user,
        "msgtype": "text",
        "agentid": AGENT_ID,
        "text": {
            "content": content
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    response = requests.post(url, headers=headers, json=data)
    res_json = response.json()
    if res_json.get('errcode') != 0:
        if "from ip" in res_json.get('errmsg'):
            ip = res_json.get('errmsg').split("from ip: ")[1].split(", more")[0]
            raise Exception(f"IP whitelist needs to be configured, please write the following IP to your APP IP whitelist: {ip}")
        else:
            raise Exception(f"Failed to send message: {res_json.get('errmsg')}")
    return response.json()

def parse_message(decrypted_message):
    # 解析XML消息
    root = ET.fromstring(decrypted_message)
    to_user = root.find('ToUserName').text
    from_user = root.find('FromUserName').text
    msg_type = root.find('MsgType').text
    content = root.find('Content').text if root.find('Content') is not None else ''
    return {'to_user': to_user, 'from_user': from_user, 'msg_type': msg_type, 'content': content}

@api_bp.route('/hello', methods=['GET'])
def hello_api():
    return jsonify(message="Hello, API!")

@api_bp.route('/wechat', methods=['GET'])
def verify_url_get():
    query = request.args
    msg_signature = query.get('msg_signature', '')
    timestamp = query.get('timestamp', '')
    nonce = query.get('nonce', '')
    echostr = query.get('echostr', '')
    
    # URL解码
    echostr = urllib.parse.unquote(echostr)

    # 验证签名
    if not check_signature(TOKEN, timestamp, nonce, echostr, msg_signature):
        return 'Verification failed', 403

    # 解密echostr
    decrypted_echostr = decrypt_message(echostr, ENCODING_AES_KEY)

    # 返回解密后的明文
    return decrypted_echostr

@api_bp.route('/wechat', methods=['POST'])
def verify_url_post():
    data = request.data
    query = request.args
    msg_signature = query.get('msg_signature')
    timestamp = query.get('timestamp')
    nonce = query.get('nonce')

    try:
        # 验证输入参数
        if not all([ msg_signature, timestamp, nonce, data ]):
            return jsonify({'error': 'Missing parameters'}), 400

        # 解密消息体
        decrypted_message = decrypt_post_data(data, ENCODING_AES_KEY)

        # 解析消息并回复发信人
        msg = parse_message(decrypted_message)
        logger.info(f"Received message from '{msg['from_user']}': {msg['content']}")
        if msg['msg_type'] == 'text':
            response = handle_message(msg)
            if response:
                send_text_message(msg['from_user'],response)
                logger.info(f"Sent message to '{msg['from_user']}': {response}")
            return jsonify({'msg': 'success'}), 200
        else:
            return jsonify({'error': 'Unsupported message type'}), 400
    except Exception as e:
        logger.error(f"Failed to handle message: {e}")
        return jsonify({'error': str(e)}), 500