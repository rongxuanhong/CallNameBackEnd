from flask import Blueprint, render_template, request
from flask_login import login_required
from database import db
from flask_restful import Resource, Api

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


@blueprint.route('/student_list/')
@login_required
def get_student_list():
    colleagues = Colleague.query.all()
    colleague = colleagues[0]
    professions = Profession.query.filter_by(colleague_id=colleague.id).all()
    profession = Profession(prof_name='全部')
    profession.id = 0
    professions.insert(0, profession)
    classes = Classes.query.join(
        Colleague.professions).filter_by(colleague_id=colleague.id).join(Profession.classes).all()
    cclass = Classes(class_name='全部')
    cclass.id = 0
    classes.insert(0, cclass)

    students = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                UserInfo.last_modify_time, UserInfo.id).join(
        Colleague.professions).filter_by(colleague_id=colleague.id).join(Profession.classes).join(
        Classes.students).all()

    return render_template('student_list.html', colleagues=colleagues, professions=professions, classes=classes,
                           students=students)
