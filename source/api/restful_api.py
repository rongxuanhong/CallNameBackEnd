import uuid
from datetime import datetime

from flask import Blueprint
from flask import request, jsonify

from base.models import UserInfo, Classes, Colleague, Profession, User, CallName, Role, Permission, Course, Menu
from database import db
from decorator import allow_cross_domain
from BadRequest import CustomFlaskErr
####   restful 接口       ######
from utils.ERROR_DEFINE import ACTION_INCORRECT, ROLE_ALREADY_EXISTS, ROLE_ALREADY_DELETE, ROLE_ALREADY_NOT_EXISTS, \
    COURSE_ALREADY_EXISTS

api = Blueprint(
    'api',
    __name__,
)


@api.route('/ajax/api/v1.0/student')
@allow_cross_domain
def query_student_list():
    """
    根据学院、专业、班级查询学生
    :return:
    """
    # try:
    try:
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
    except Exception as err:
        return jsonify({'error_msg': str(err),
                        'success': False, })
    return jsonify({
        'result': students_list,
        'success': True,
        'total': total
    })


def delete_table_or_record(table_or_record):
    db.session.delete(table_or_record)
    db.session.commit()


@api.route('/ajax/api/v1.0/student', methods=['POST'])
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

        student = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                   Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                   UserInfo.last_modify_time, UserInfo.uid).join(
            Colleague.professions).join(Profession.classes).join(
            Classes.students).filter(UserInfo.uid == userinfo.uid).first()

        return jsonify({'success': True,
                        'result': {
                            'user_name': student[0],
                            'job_number': student[1],
                            'class_name': student[2],
                            'profession_name': student[3],
                            'colleague_name': student[4],
                            'last_modify_time': student[5].strftime('%Y-%m-%d %H:%M:%S'),
                            'student_uuid': student[6],
                        }})
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/student', methods=['PUT'])
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
        student = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                   Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                   UserInfo.last_modify_time, UserInfo.uid).join(
            Colleague.professions).join(Profession.classes).join(
            Classes.students).filter(UserInfo.uid == userinfo.uid).first()

        return jsonify({'success': True,
                        'result': {
                            'user_name': student[0],
                            'job_number': student[1],
                            'class_name': student[2],
                            'profession_name': student[3],
                            'colleague_name': student[4],
                            'last_modify_time': student[5].strftime('%Y-%m-%d %H:%M:%S'),
                            'student_uuid': student[6],
                        }})
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/student', methods=['DELETE'])
def delete_student():
    """
    删除学生信息
    :return:
    """
    uids = request.values.get('uids')
    split = uids.split(',')
    try:
        for uid in split:
            if uid == '':
                continue
            userinfo = UserInfo.query.filter(UserInfo.uid == uid).first()
            if userinfo is None:
                continue
            delete_table_or_record(userinfo)
        return jsonify({'success': True, })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/login', methods=['POST'])
def login():
    """
    判断是否学生是否能够登录，检查用户名和密码是否匹配
    :return:
    """
    username = requestParameter('username')
    password = requestParameter('pwd')

    ### 复杂一些 需要验证帐号和密码的规范性
    try:
        user = User.query.filter(User.username == username).first()
        if user:
            if user.password == password:
                # userinfo = UserInfo.query.filter(UserInfo.userid == user.id).first()
                return jsonify({'success': True, })
            else:
                error_msg = '帐号或密码错误'
        else:
            error_msg = '该帐号未注册'
        return jsonify({'error_msg': str(error_msg),
                        'success': False, })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


# @api.route('/ajax/api/register')
# def register():
#     """
#     用户注册
#     :return:
#     """
#     username = request.args.get('username')
#     if not str(username).startswith('N'):
#         return '0'  ##注册帐号必须以N开头即学号
#     password = request.args.get('pwd')
#     try:
#         user = User.query.filter(User.username == username).first()
#         if user:
#             return '1'  ##已注册
#         else:
#             user = User(username)
#             user.password = password
#             user.role_id = 3
#             db.session.add(user)
#             db.session.commit()
#             userinfo = UserInfo(username, username, 2)
#             userinfo.userid = user.id
#             userinfo.uid = str(uuid.uuid4())
#             db.session.add(userinfo)
#             db.session.commit()
#             return '2'  ##注册成功
#     except:
#         return '-1'  ###数据库异常


@api.route('/ajax/api/user_profile')
def get_user_profile():
    """
    获取用户个人中心资料
    :return:
    """
    uid = requestParameter('user_uid')
    try:
        list = db.session.query(UserInfo, Classes.class_name, Profession.prof_name, Colleague.colea_name).join(
            Colleague.professions).join(
            Profession.classes).join(
            Classes.students).join(UserInfo.user).filter(UserInfo.uid == uid, UserInfo.type == 2).all()
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })
    userinfo = list[0]
    user_dict = {'username': userinfo.user_name, 'job_number': userinfo.job_number,
                 'sex': userinfo.sex, 'class_name': list[1], 'profession_name': list[2],
                 'colleague_name': list[3]}
    data = {'user_profile': user_dict}
    return jsonify({
        'result': data,
        'success': True,
    })


def requestParameter(parameter):
    return request.values.get(parameter)


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
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })
    return jsonify({'result': callname.to_json(),
                    'success': False, })


@api.route('/ajax/api/v1.0/post_students_from_excel', methods=['POST'])
def post_students_from_excel():
    """
    从excel导入学生数据
    :return:
    """
    data = requestParameter('student_data')
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
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })
    return jsonify({
        'success': True
    })


@api.route('/ajax/api/v1.0/role_menu')
def get_menu_role():
    """
    获取角色菜单列表
    :return:
    """
    role_name = requestParameter('role_name')
    try:
        role = Role.query.filter(Role.role_name == role_name).first()
        if role:
            menus = [item.menu for item in role.menus]
            displays = [item.display for item in role.menus]
            result = list()
            for (menu, display) in zip(menus, displays):
                dict = menu.to_json()
                dict['display'] = display
                result.append(dict)

            return jsonify({
                'result': result,
                'success': True
            })
        else:
            raise CustomFlaskErr(ROLE_ALREADY_NOT_EXISTS, 400)

    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/role_menu', methods=['POST'])
def modify_role_menu_display():
    selected = requestParameter('selected')
    role_name = requestParameter('role_name')
    try:
        split = selected.split(',')
        role = Role.query.filter(Role.role_name == role_name).first()
        if role:
            for menu in role.menus:  ## role.menus 是关系记录列表
                if str(menu.menu_id) in split:
                    menu.display = 1
                else:
                    menu.display = 0
            db.session.add(role)
            db.session.commit()
            return jsonify({
                'success': True
            })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/role', methods=['GET'])
def get_role_list():
    """
    获取角色列表
    :return:
    """
    action = request.values.get('action')
    if action != 'role_list':
        raise CustomFlaskErr(ACTION_INCORRECT, 400)
    try:
        roles = Role.query.all()
        if len(roles):
            return jsonify({
                'result': [role.to_json() for role in roles],
                'success': True,
            })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/role', methods=['POST'])
def add_role():
    """
    添加学生
    :return:
    """
    role_name = requestParameter('role_name')
    role_desc = requestParameter('role_desc')

    try:
        role = Role.query.filter(Role.role_name == role_name).first()
        if role is None:
            role = Role(role_name, role_desc)
            addToDb(role)
            return jsonify({
                'result': role.to_json(),
                'success': True
            })
        else:
            raise CustomFlaskErr(ROLE_ALREADY_EXISTS, 400)
    except Exception as error:
        return str(error)


@api.route('/ajax/api/v1.0/role', methods=['PUT'])
def modify_role():
    """
    修改学生
    :return:
    """
    role_name = requestParameter('role_name')
    role_id = requestParameter('role_id')
    role_desc = requestParameter('role_desc')

    try:
        role = Role.query.filter(Role.id == role_id).first()
        if role:
            role.role_name = role_name
            role.role_desc = role_desc
            addToDb(role)
            return jsonify({
                'result': role.to_json(),
                'success': True
            })
        else:
            raise CustomFlaskErr(ROLE_ALREADY_NOT_EXISTS, 400)
    except Exception as error:
        return str(error)


@api.route('/ajax/api/v1.0/role', methods=['DELETE'])
def delete_Role():
    """
    修改角色信息
    :return:
    """
    role_id = requestParameter('role_id')
    try:
        role = Role.query.filter(Role.id == role_id).first()
        if role is None:
            raise CustomFlaskErr(ROLE_ALREADY_DELETE, 400)
        delete_table_or_record(role)
        return jsonify({
            'success': True
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/course')
def getCourse():
    action = request.values.get('action')
    sort_name = request.values.get('sort', 'course_number')
    sort_order = request.values.get('sortOrder', 'asc')
    limit = request.values.get('limit', 10, type=int)  ## 一页大小
    offset = request.values.get('offset', 1, type=int)  ## 页码
    pageIndex = (offset / limit) + 1  ## offset 从零开始
    if action != 'course_list':
        raise CustomFlaskErr(ACTION_INCORRECT, 400)

    try:
        courses_query = Course.query.order_by(sort_name + " " + sort_order)
        courses = courses_query.limit(limit).offset((pageIndex - 1) * limit).all()
        total = courses_query.count()
        return jsonify({
            'result': [course.to_json() for course in courses],
            'success': True,
            'total': total
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/course', methods=['POST'])
def addCourse():
    """
    添加课程
    :return:
    """
    course_number = requestParameter('course_number')  ## 课程编号
    course_name = requestParameter('course_name')
    course_week_times = requestParameter('course_week_times')
    position = requestParameter('position')
    semester = requestParameter('semester')
    course_time = requestParameter('course_time')
    try:
        course = Course()
        course.course_name = course_name
        course.course_number = course_number
        course.semester = semester
        course.position = position
        course.course_week_times = course_week_times
        course.course_time = course_time

        return jsonify({
            'result': course.to_json(),
            'success': True
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/course', methods=['PUT'])
def modifyCourse():
    """
    添加课程
    :return:
    """
    course_number = requestParameter('course_number')  ## 课程编号
    course_name = requestParameter('course_name')
    course_week_times = requestParameter('course_week_times')
    position = requestParameter('position')
    semester = requestParameter('semester')
    course_time = requestParameter('course_time')
    try:
        course = Course.query.filter(Course.course_number == course_number).first
        if course:
            course.course_name = course_name
            course.course_number = course_number
            course.semester = semester
            course.position = position
            course.course_week_times = course_week_times
            course.course_time = course_time
        else:
            raise CustomFlaskErr(COURSE_ALREADY_EXISTS, 400)

        return jsonify({
            'result': course.to_json(),
            'success': True
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/course', methods=['DELETE'])
def deleteCourse():
    course_numbers = requestParameter('course_number')
    split = course_numbers.split(',')
    try:
        for course_number in split:
            if course_number == '':
                continue
            course = Course.query.filter(Course.course_number == course_number)
            if course is None:
                continue
            delete_table_or_record(course)
        return jsonify({'success': True, })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })
