from flask import Blueprint, render_template
from flask_login import login_required

from base.models import TeachLocation

blueprint = Blueprint(
    'course_blueprint',
    __name__,
    url_prefix='/course_management',
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')


@blueprint.route('/course_arrange')
@login_required
def get_course_arrange():
    teach_locations = TeachLocation.query.all()
    weeks = ['周一', '周二', '周三', '周四', '周五']
    times = ['第1节', '第2节', '第3节', '第4节', '第5节', '第6节', '第7节', '第8节', '第9节', '第10节', '第11节', '第12节', ]
    return render_template('course_arrange.html', teach_locations=teach_locations, weeks=weeks, times=times)
