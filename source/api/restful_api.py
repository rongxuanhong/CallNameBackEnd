import uuid
from datetime import datetime

from flask import Blueprint
from flask import request, jsonify

from base.models import UserInfo, Classes, Colleague, Profession, User, CallName, Role, Permission
from database import db

####   restful 接口       ######
api = Blueprint(
    'api',
    __name__,
)


@api.route('/ajax/api/v1.0/student-query/')
def query_student_list():
    """
    根据学院、专业、班级查询学生
    :return:
    """
    colleague_name = request.args.get('colleague_name', '数计学院')
    profession_name = request.args.get('profession_name', '全部')
    class_name = request.args.get('class_name', '全部')
    sort_name = request.args.get('sort', 'job_number')
    sort_order = request.args.get('sortOrder', 'asc')
    limit = request.args.get('limit', 10, type=int)  ## 一页大小
    offset = request.args.get('offset', 1, type=int)  ## 页码
    pageIndex = (offset / limit) + 1  ## offset 从零开始
    # if sort_order == 'desc':
    #     sort = sort_name.desc()
    # else:
    #     sort = sort_name.asc()
    if sort_name == 'profession_name':
        sort_name = 'prof_name'

    if profession_name == '全部' and class_name == '全部':
        students_query = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                          Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                          UserInfo.last_modify_time, UserInfo.uid).join(
            Colleague.professions).filter(Colleague.colea_name == colleague_name).join(
            Profession.classes).join(Classes.students).order_by(sort_name + " " + sort_order)
    elif profession_name == '全部':
        students_query = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                          Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                          UserInfo.last_modify_time, UserInfo.uid).join(
            Colleague.professions).filter(Colleague.colea_name == colleague_name).join(
            Profession.classes).join(
            Classes.students).filter(Classes.class_name == class_name).order_by(sort_name + " " + sort_order)
    elif class_name == '全部':
        students_query = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                          Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                          UserInfo.last_modify_time, UserInfo.uid).join(
            Colleague.professions).filter(Colleague.colea_name == colleague_name).join(Profession.classes) \
            .filter(Profession.prof_name == profession_name).join(
            Classes.students).order_by(sort_name + " " + sort_order)
    else:
        students_query = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                          Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                          UserInfo.last_modify_time, UserInfo.uid).join(
            Colleague.professions).filter(Colleague.colea_name == colleague_name).join(
            Profession.classes).filter(Profession.prof_name == profession_name).join(
            Classes.students).filter(Classes.class_name == class_name).order_by(sort_name + " " + sort_order)
    students = students_query.limit(limit).offset(
        (pageIndex - 1) * limit).all()
    total = students_query.count()
    students_list = []
    if len(students):
        for student in students:
            s = {'user_name': student[0],
                 'job_number': student[1],
                 'class_name': student[2],
                 'profession_name': student[3],
                 'colleague_name': student[4],
                 'last_modify_time': student[5].strftime('%Y-%m-%d %H:%M:%S'),
                 'student_uuid': student[6],
                 }
            students_list.append(s)
    return jsonify({
        'students': students_list,
        'msg': '1',
        'total': total
    })


def delete_table_or_record(table_or_record):
    db.session.delete(table_or_record)
    db.session.commit()


# @api.route('/ajax/api/v1.0/student-delete/', methods=['DELETE'])
# def student_delete():
#     """
#     学生删除
#     :return:
#     """
#     job_number = request.values.get('job_number')
#     type = request.values.get('type')
#     try:
#         if type == '2':  ## 学生 只删除记录
#             student = UserInfo.query.filter(UserInfo.job_number == job_number).first()
#             delete_table_or_record(student)
#         elif type == '1':
#             teacher_info = UserInfo.query.filter(UserInfo.job_number == job_number).first()
#             teacher_user = User.query.filter(User.id == teacher_info.user_id).first()
#             delete_table_or_record(teacher_info)  ### 删除从表
#             delete_table_or_record(teacher_user)  ### 删除主表
#         return '1'
#     except:
#         return '-1'


@api.route('/ajax/api/v1.0/student-add/', methods=['POST'])
def add_student():
    """
    添加学生
    :return:
    """
    class_name = request.values.get('class_name')
    job_number = request.values.get('jobnumber')
    user_name = request.values.get('username')

    try:
        c_class = Classes.query.filter(Classes.class_name == class_name).first()
        userinfo = UserInfo(user_name, job_number, 2)
        userinfo.uid = str(uuid.uuid4())
        userinfo.class_id = c_class.id
        addToDb(userinfo)
        return '1'  ### 添加成功
    except Exception as error:
        return error


@api.route('/ajax/api/v1.0/student-modify/', methods=['PUT'])
def modify_student():
    """
    修改学生信息
    :return:
    """
    user_name = request.values.get('username')
    job_number = request.values.get('jobnumber')
    class_name = request.values.get('class_name')
    uid = request.values.get('uid')

    try:
        userinfo = UserInfo.query.filter(UserInfo.uid == uid).first()
        c_class = Classes.query.filter(Classes.class_name == class_name).first()
        userinfo.class_id = c_class.id
        userinfo.user_name = user_name
        userinfo.job_number = job_number
        userinfo.last_modify_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        addToDb(userinfo)
        return '1'
    except:
        return '-1'


@api.route('/ajax/api/v1.0/student-delete/', methods=['DELETE'])
def delete_student():
    """
    修改学生信息
    :return:
    """
    uids = request.values.get('uids')
    split = uids.split(',')
    try:
        for uid in split:
            if uid == '':
                continue
            # try:
            userinfo = UserInfo.query.filter(UserInfo.uid == uid).first()
            delete_table_or_record(userinfo)
            # except:
            #     return '-1'
        return "1"
    except Exception as error:
        return error


@api.route('/ajax/api/login')
def login():
    """
    判断是否学生是否能够登录，检查用户名和密码是否匹配
    :return:
    """
    username = request.args.get('username')
    password = request.args.get('pwd')

    ### 复杂一些 需要验证帐号和密码的规范性
    try:
        user = User.query.filter(User.username == username).first
        if user:
            if user.password == password:
                userinfo = UserInfo.query.filter(UserInfo.userid == user.id).first()
                return userinfo.uid  ##验证登录成功
            else:
                return '1'  ##帐号或密码错误
        else:
            return '0'  ### 该帐号未注册
    except:
        return '-1'  ###数据库异常


@api.route('/ajax/api/register')
def register():
    """
    用户注册
    :return:
    """
    username = request.args.get('username')
    if not str(username).startswith('N'):
        return '0'  ##注册帐号必须以N开头即学号
    password = request.args.get('pwd')
    try:
        user = User.query.filter(User.username == username).first()
        if user:
            return '1'  ##已注册
        else:
            user = User(username)
            user.password = password
            user.role_id = 3
            db.session.add(user)
            db.session.commit()
            userinfo = UserInfo(username, username, 2)
            userinfo.userid = user.id
            userinfo.uid = str(uuid.uuid4())
            db.session.add(userinfo)
            db.session.commit()
            return '2'  ##注册成功
    except:
        return '-1'  ###数据库异常


@api.route('/ajax/api/user_profile')
def get_user_profile():
    """
    获取用户个人中心资料
    :return:
    """
    uid = request.args.get('userid')
    try:
        list = db.session.query(UserInfo, Classes.class_name, Profession.prof_name, Colleague.colea_name).join(
            Colleague.professions).join(
            Profession.classes).join(
            Classes.students).join(UserInfo.user).filter(UserInfo.uid == uid, UserInfo.type == 2).all()
    except:
        return '-1'  ### 数据库查询异常
    userinfo = list[0]
    user_dict = {'username': userinfo.user_name, 'job_number': userinfo.job_number,
                 'sex': userinfo.sex, 'class_name': list[1], 'profession_name': list[2],
                 'colleague_name': list[3]}
    data = {'user_profile': user_dict}
    return jsonify(data)


def requestParameter(parameter):
    return request.args.get(parameter)


def addToDb(table):
    db.session.add(table)
    db.session.commit()


@api.route('/ajax/api/call_roll_submit', methods=['POST'])
def post_call_roll():
    """
    提交学生的点名信息
    :return:
    """
    checkin_time = requestParameter('checkin_time')
    checkin_type = requestParameter('checkin_type')
    checkin_notes = requestParameter('checkin_notes')
    checkin_grade = requestParameter('checkin_grade')
    course_id = requestParameter('course_id')

    try:
        callname = CallName(checkin_time, checkin_type, checkin_notes, checkin_grade, course_id)
        addToDb(callname)
    except:
        return '-1'  #### 数据库异常
    return '1'  ### 点名成功提交


@api.route('/ajax/api/v1.0/post_students_from_excel/', methods=['POST'])
def post_students_from_excel():
    """
    从excel导入学生数据
    :return:
    """
    data = request.values.get('student_data')
    if (len(eval(data)) == 0):
        return -1
    ## 检测数据的准确性   规定批量导入同班级同专业同学院的学生
    student_list = eval(data)
    student = student_list[0]
    try:
        colleague = Colleague.query.filter(Colleague.colea_name == student['学院']).first()
        if colleague is None:
            colleague = Colleague(student['学院'])
            addToDb(colleague)
        profession = Profession.query.filter(Profession.prof_name == student['专业']).first()
        if profession is None:
            profession = Profession(student['专业'])
            profession.colleague_id = colleague.id  ## 绑定学院
            addToDb(profession)
        c_class = Classes.query.filter(Classes.class_name == student['班级']).first()
        if c_class is None:
            c_class = Classes(student['班级'])
            c_class.profession_id = profession.id
            addToDb(c_class)

        total = 0
        for student in student_list:
            total += 1
            student.setdefault("last_modify_time", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            c_class = Classes.query.filter(Classes.class_name == student['班级']).first()
            student['user_name'] = student.pop('姓名')
            student['job_number'] = student.pop('学号')
            student['class_name'] = student.pop('班级')
            student['profession_name'] = student.pop('专业')
            student['colleague_name'] = student.pop('学院')
            user_info = UserInfo(student['user_name'], student['job_number'], 2)
            user_info.uid = str(uuid.uuid4())
            user_info.class_id = c_class.id
            db.session.add(user_info)
        db.session.commit()
    except:
        return '-1'
    return '1'


@api.route('/ajax/api/v1.0/get_permission_list/')
def get_permission():
    """
    获取权限列表
    :return:
    """
    action = request.values.get('action')
    if action != 'permission_list':
        return '-1'
    permissions = Permission.query.all()
    if len(permissions):
        return jsonify({
            'permissions': permissions
        })
    else:
        return '-1'


@api.route('/ajax/api/v1.0/get_role_list/')
def get_role_list():
    """
    获取角色列表
    :return:
    """
    action = request.values.get('action')
    if action != 'role_list':
        return '-1'
    roles = Role.query.all()

    if len(roles):
        return jsonify({
            'roles': [role.to_json() for role in roles],
        })
    else:
        return '-1'


@api.route('/ajax/api/v1.0/role-add/', methods=['POST'])
def add_role():
    """
    添加学生
    :return:
    """
    role_name = request.values.get('role_name')
    role_desc = request.values.get('role_desc')

    try:
        role = Role.query.filter(Role.role_name == role_name).first()
        if role is None:
            role = Role(role_name, role_desc)
            addToDb(role)
            return '1'  ### 添加成功
        return '-1'
    except Exception as error:
        return str(error)


@api.route('/ajax/api/v1.0/role-modify/', methods=['PUT'])
def modify_Role():
    """
    修改角色信息
    :return:
    """
    role_id = request.values.get('role_id')
    role_name = request.values.get('role_name')
    role_desc = request.values.get('role_desc')

    try:
        role = Role.query.filter(Role.id == role_id).first()
        role.role_name = role_name
        role.role_desc = role_desc
        addToDb(role)
        return '1'  ### 修改成功
    except Exception as error:
        return str(error)


@api.route('/ajax/api/v1.0/role-delete/', methods=['DELETE'])
def delete_Role():
    """
    修改角色信息
    :return:
    """
    role_id = request.values.get('role_id')
    try:
        role = Role.query.filter(Role.id == role_id).first()
        delete_table_or_record(role)
        return "1"
    except Exception as error:
        return str(error)
