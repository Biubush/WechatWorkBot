from flask import Blueprint

# 创建一个蓝图
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def home():
    html = """
    <h1>您成功启动了AGSSM!</h1>
    <p>AHU Graduate Student Schedule Manager</p>
    <p>安徽大学研究生课表管家</p>
    """
    return html
