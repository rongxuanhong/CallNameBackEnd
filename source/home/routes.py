from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix='/home',# 配置当前模块功能下的视图函数自动加上前缀
    template_folder='templates', #用以指定蓝图的模版文件所在的文件夹 /home/templates/index.html
    static_folder='static' #用以指定蓝图的静态文件所在的文件夹 /home/static
)

# 此类型统称视图函数
@blueprint.route('/index')
@login_required
def index():
    return render_template('index.html')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')
