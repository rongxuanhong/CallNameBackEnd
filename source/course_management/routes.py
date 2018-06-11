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
    times = ['第一节', '第二节', '第三节', '第四节', '第五节', '第六节', '第七节', '第八节', '第九节', '第十节', '第十一节', '第十二节', ]
    return render_template('course_arrange.html', teach_locations=teach_locations, weeks=weeks, times=times)
