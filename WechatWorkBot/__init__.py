from flask import Flask
from WechatWorkBot.apis import api_bp
from WechatWorkBot.views import views_bp

app = Flask(__name__)
app.config.from_object('WechatWorkBot.config.Config')  # 加载配置文件

# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(views_bp, url_prefix='/')

def start_server():
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])