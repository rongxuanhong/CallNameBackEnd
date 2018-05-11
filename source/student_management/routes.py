from flask import Blueprint, render_template
from flask_login import login_required
from database import db
from sqlalchemy import and_

from base.models import Colleague, Profession, Classes, UserInfo

blueprint = Blueprint(
    'student_blueprint',
    __name__,
    url_prefix='/student_management',
    template_folder='templates',
    static_folder='static'
)


# @blueprint.route('/<template>')
# @login_required
# def route_template(template):
#     return render_template(template + '.html')


@blueprint.route('/student_list/<int:id>')
@login_required
def get_student_list(id):
    colleagues = Colleague.query.all()
    colleague = colleagues[id - 1]
    professions = Profession.query.filter_by(colleague_id=colleague.id)
    profession = professions[0]
    classes = Classes.query.filter_by(profession_id=profession.id)
    students = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                UserInfo.last_modify_time,UserInfo.id).join(
        Colleague.professions).join(Profession.classes).join(Classes.students).filter(
        UserInfo.class_id == 2).all()
    return render_template('student_list.html', colleagues=colleagues, professions=professions, classes=classes,
                           students=students)
