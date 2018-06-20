import uuid
from datetime import datetime

from flask import Blueprint
from flask import request, jsonify

from base.models import UserInfo, Classes, Colleague, Profession, User, CallName, Role, Permission, Course, Menu, \
    CourseArrange, TeachLocation, Timetable, ClassTimeTable, DataDictTable
from database import db
from decorator import allow_cross_domain
from BadRequest import CustomFlaskErr
####   restful 接口       ######
from utils.ERROR_DEFINE import ACTION_INCORRECT, ROLE_ALREADY_EXISTS, ROLE_ALREADY_DELETE, ROLE_ALREADY_NOT_EXISTS, \
    COURSE_ALREADY_EXISTS, ORGANIZATION_TYPE_NOT_EXISTS, PARENT_ORGANIZATION_NAME_NOT_EXITS, ORGANIZATION_NAME_EXITS, \
    TEACH_TIME_DUPLICATION, COURSE_ALREADY_ARRANGE, NOT_CALL_ROLL_INFO, SITE_ALREADY_EXIST

api = Blueprint(
    'api',
    __name__,
)


@api.route('/ajax/api/v1.0/student')
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
                Profession.classes).join(Classes.students).filter(UserInfo.type == 2).order_by(
                sort_name + " " + sort_order)
        elif profession_name == '全部':
            students_query = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                              Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                              UserInfo.last_modify_time, UserInfo.uid).join(
                Colleague.professions).filter(Colleague.colea_name == colleague_name).join(
                Profession.classes).join(
                Classes.students).filter(Classes.class_name == class_name).filter(UserInfo.type == 2).order_by(
                sort_name + " " + sort_order)
        elif class_name == '全部':
            students_query = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                              Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                              UserInfo.last_modify_time, UserInfo.uid).join(
                Colleague.professions).filter(Colleague.colea_name == colleague_name).join(Profession.classes) \
                .filter(Profession.prof_name == profession_name).join(
                Classes.students).filter(UserInfo.type == 2).order_by(sort_name + " " + sort_order)
        else:
            students_query = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                              Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                              UserInfo.last_modify_time, UserInfo.uid).join(
                Colleague.professions).filter(Colleague.colea_name == colleague_name).join(
                Profession.classes).filter(Profession.prof_name == profession_name).join(
                Classes.students).filter(Classes.class_name == class_name).filter(UserInfo.type == 2).order_by(
                sort_name + " " + sort_order)
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
                userinfo = UserInfo.query.filter(UserInfo.userid == user.id).first()
                if userinfo.class_id is not None:
                    classes = Classes.query.filter(Classes.id == userinfo.class_id).first()
                    return jsonify({'success': True,
                                    'class_name': classes.class_name,
                                    'uid': userinfo.uid})
                else:
                    error_msg = '未设定所属班级'
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
    uid = requestParameter('uid')
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


@api.route('/ajax/api/call_roll_range')
def get_call_roll_range():
    location = requestParameter('loc_name')
    try:
        data_dict = DataDictTable.query.filter(DataDictTable.dict_item == '签到范围').first()
        teach_location = TeachLocation.query.filter(TeachLocation.loc_name == location).first()
        return jsonify({'result': {'radius': data_dict.dict_value,
                                   'refer_loc': teach_location.location}, 'success': True, })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/call_roll_submit', methods=['POST'])
def post_call_roll():
    """
    学生提交的点名信息
    :return:
    """
    checkin_time = requestParameter('checkin_time')
    checkin_type = requestParameter('checkin_type')  # 考勤类型 0:缺席 1:请假 2:出席
    checkin_uid = requestParameter('checkin_uid')
    checkin_grade = requestParameter('checkin_grade')
    course_name = requestParameter('course_name')
    try:
        callname = CallName(checkin_time, checkin_type, checkin_uid, course_name,checkin_grade)
        course = Course.query.filter(Course.course_name == course_name).first()
        callname.course_id = course.id
        addToDb(callname)
        return jsonify(
            {'result': callname.to_json(),
             'success': True, })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/call_roll_state')
def get_call_roll_state():
    """
    查看学生点名列表
    :return:
    """
    course_name = requestParameter('course_name')

    # 下发签到范围
    try:
        callnames = CallName.query.filter(CallName.course_name == course_name).all()
        if len(callnames):
            return jsonify({'result': [callname.to_json() for callname in callnames],
                            'success': True, })
        else:
            raise CustomFlaskErr(NOT_CALL_ROLL_INFO, 400)
    except Exception as error:
        if isinstance(error, CustomFlaskErr):
            return jsonify({'error_msg': str(error.return_code),
                            'success': False, })
        return jsonify({'error_msg': str(error),
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


@api.route('/ajax/api/v1.0/role_menu', methods=['PUT'])
def modify_role_menu_display():
    """
    修改角色的菜单权限
    :return:
    """
    selected = requestParameter('selected') ### 为啥父节点没返回？？？有选中啊
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


@api.route('/ajax/api/v1.0/user_menu')
def get_role_menu():
    """
    获取角色的可显示菜单
    :return:
    """
    try:
        role_name = requestParameter('role_name')
        role = Role.query.filter(Role.role_name == role_name).first()
        if role:
            role_ids = [menu.menu_id for menu in role.menus if menu.display]
            menus = Menu.query.filter(Menu.id.in_(role_ids)).order_by('id').all()
            data = dict()
            result = list()
            for menu in menus:
                if menu.parent_id == 0:
                    menu.url = ''
                    data[menu.id] = {'id': menu.id, 'name': menu.name, 'icon': menu.icon, 'url': menu.url,
                                     'children': []}
                else:
                    data[menu.parent_id]['children'].append(
                        {'id': menu.id, 'name': menu.name, 'icon': menu.icon, 'url': menu.url,
                         'children': []})

            for item in data.values():
                result.append(item)
            return jsonify({
                'result': result,
                'success': True
            })

    except Exception as error:
        return jsonify({
            'error_msg': str(error),
            'success': False,
        })


@api.route('/ajax/api/v1.0/role', methods=['POST'])
def add_role():
    """
    添加角色
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


@api.route('/ajax/api/v1.0/role')
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
            role.last_modify_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
    course_name = request.values.get('course_name', '')
    action = request.values.get('action')
    sort_name = request.values.get('sort', 'course_number')
    sort_order = request.values.get('sortOrder', 'asc')
    limit = request.values.get('limit', 10, type=int)  ## 一页大小
    offset = request.values.get('offset', 1, type=int)  ## 页码
    pageIndex = (offset / limit) + 1  ## offset 从零开始
    if action != 'course_list':
        raise CustomFlaskErr(ACTION_INCORRECT, 400)

    try:
        if course_name == '':
            courses_query = Course.query.order_by(sort_name + " " + sort_order)
        else:  ## 配合搜索框的模糊查询
            courses_query = Course.query.filter(Course.course_name.like('%' + course_name + '%')).order_by(
                sort_name + " " + sort_order)
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
    course_week_times = requestParameter('course_weeks')
    # position = requestParameter('course_position')
    semester = requestParameter('course_semester')
    # course_time = requestParameter('course_time')
    course_members = requestParameter('course_members')
    try:
        course = Course()
        course.course_name = course_name
        course.course_number = course_number
        course.semester = semester
        # course.position = position
        course.course_week_times = course_week_times
        # course.course_time = course_time
        course.course_members = course_members
        addToDb(course)
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
    修改课程
    :return:
    """
    course_number = requestParameter('course_number')  ## 课程编号
    course_name = requestParameter('course_name')
    course_week_times = requestParameter('course_weeks')
    # position = requestParameter('course_position')
    semester = requestParameter('course_semester')
    # course_time = requestParameter('course_time')
    course_members = requestParameter('course_members')
    try:
        course = Course.query.filter(Course.course_number == course_number).first()
        if course:
            course.course_name = course_name
            course.course_number = course_number
            course.semester = semester
            # course.position = position
            course.course_week_times = course_week_times
            # course.course_time = course_time
            course.course_members = course_members
            course.last_modify_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            addToDb(course)
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
    course_number = requestParameter('course_number')
    try:
        course = Course.query.filter(Course.course_number == course_number).first()
        if course:
            delete_table_or_record(course)
            return jsonify({'success': True, })
        else:
            raise CustomFlaskErr(COURSE_ALREADY_EXISTS, 400)
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/course-query')
def query_course_by_course_name():
    try:
        course_name = requestParameter('course_name')
        courses = Course.query.filter(Course.course_name.like('%' + course_name + '%')).all()
        return jsonify({
            'result': [course.to_json() for course in courses],
            'success': True
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/organization')
def get_organization_data():
    """
    获取所有组织关系数据
    :return:
    """
    try:
        colleagues = Colleague.query.all()
        result = list()
        for index1, colleague in enumerate(colleagues):
            profession_list = list()
            for index2, profession in enumerate(colleague.professions):
                class_list = list()
                for index3, classes in enumerate(profession.classes):
                    class_list.append({
                        'id': classes.uuid + ',class',
                        'text': classes.class_name,
                        'icon': 'glyphicon glyphicon-ice-lolly-tasted',
                        'children': []
                    })
                profession_list.append({
                    'id': profession.uuid + ',profession',
                    'text': profession.prof_name,
                    'icon': 'glyphicon glyphicon-scale',
                    'children': class_list,
                })
            result.append({
                'id': colleague.uuid + ',colleague',
                'text': colleague.colea_name,
                'icon': 'glyphicon glyphicon-education',
                'children': profession_list
            })

        return jsonify({
            'result': result,
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/colleague', methods=['PUT'])
def modifyColleague():
    """
    修改学院名
    :return:
    """
    uid = requestParameter('uuid')
    colea_name = requestParameter('colea_name')
    try:
        colleague = Colleague.query.filter(Colleague.uuid == uid).first()
        if colleague:
            colleague.colea_name = colea_name
            colleague.last_modify_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            addToDb(colleague)
            return jsonify({
                'result': colleague.to_json(),
                'success': True,
            })

    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/colleague', methods=['DELETE'])
def deleteColleague():
    """
    删除学院名
    :return:
    """
    uid = requestParameter('uuid')
    try:
        colleague = Colleague.query.filter(Colleague.uuid == uid).first()
        if colleague:
            delete_table_or_record(colleague)
            return jsonify({
                'success': True,
            })

    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/profession', methods=['PUT'])
def modifyProfession():
    """
    修改专业名
    :return:
    """
    uid = requestParameter('uuid')
    prob_name = requestParameter('prob_name')
    try:
        profession = Profession.query.filter(Profession.uuid == uid).first()
        if profession:
            profession.prof_name = prob_name
            profession.last_modify_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            addToDb(profession)
            return jsonify({
                'result': profession.to_json(),
                'success': True,
            })

    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/profession', methods=['DELETE'])
def deleteProfession():
    """
    删除专业名
    :return:
    """
    uid = requestParameter('uuid')
    try:
        profession = Profession.query.filter(Profession.uuid == uid).first()
        if profession:
            delete_table_or_record(profession)
            return jsonify({
                'success': True,
            })

    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/class', methods=['PUT'])
def modifyClass():
    """
    修改班级名
    :return:
    """
    uid = requestParameter('uuid')
    class_name = requestParameter('class_name')
    try:
        classes = Classes.query.filter(Classes.uuid == uid).first()
        if classes:
            classes.class_name = class_name
            classes.last_modify_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            addToDb(classes)
            return jsonify({
                'result': classes.to_json(),
                'success': True,
            })

    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/class', methods=['DELETE'])
def deleteClass():
    """
    删除班级名
    :return:
    """
    uid = requestParameter('uuid')
    try:
        classes = Classes.query.filter(Classes.uuid == uid).first()
        if classes:
            delete_table_or_record(classes)
            return jsonify({
                'success': True,
            })

    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/organization', methods=['POST'])
def organization_add():
    organization_name = requestParameter('organization_names')
    organization_type = requestParameter('organization_types')
    parents_organization_names = requestParameter('parent_organization_names')
    if organization_type not in ['学院', '专业', '班级']:
        raise CustomFlaskErr(ORGANIZATION_TYPE_NOT_EXISTS, 400)
    result = list()
    try:
        if organization_type == '学院':
            colleague = Colleague.query.filter(Colleague.colea_name == organization_name).first()
            if colleague is None:
                colleague = Colleague(organization_name)
                colleague.uuid = str(uuid.uuid4())
                addToDb(colleague)
                result.append(colleague)
            else:
                raise CustomFlaskErr(ORGANIZATION_NAME_EXITS, 400)
        elif organization_type == '专业':
            colleague = Colleague.query.filter(Colleague.colea_name == parents_organization_names).first()
            if colleague:
                profession = Profession.query.filter(Profession.prof_name == organization_name).first()
                if profession is None:
                    profession = Profession(organization_name)
                    profession.uuid = str(uuid.uuid4())
                    profession.colleague_id = colleague.id
                    addToDb(profession)
                    result.append(profession)
                else:
                    raise CustomFlaskErr(ORGANIZATION_NAME_EXITS, 400)
            else:
                raise CustomFlaskErr(PARENT_ORGANIZATION_NAME_NOT_EXITS, 400)
        else:
            profession = Profession.query.filter(Profession.prof_name == parents_organization_names).first()
            if profession:
                classes = Classes.query.filter(Classes.class_name == organization_name).first()
                if classes is None:
                    classes = Classes(organization_name)
                    classes.uuid = str(uuid.uuid4())
                    classes.profession_id = profession.id
                    addToDb(classes)
                    result.append(classes)
                else:
                    raise CustomFlaskErr(ORGANIZATION_NAME_EXITS, 400)
            else:
                raise CustomFlaskErr(PARENT_ORGANIZATION_NAME_NOT_EXITS, 400)

        return jsonify({
            'result': [re.to_json() for re in result],
            'success': True,
        })
    except Exception as error:
        if isinstance(error, CustomFlaskErr):
            return jsonify({'error_msg': str(error.return_code),
                            'success': False, })
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/course_arrange')
def get_course_arrange():
    limit = request.args.get('limit', 10, type=int)  ## 一页大小
    offset = request.args.get('offset', 1, type=int)  ## 页码
    pageIndex = (offset / limit) + 1
    class_query = Classes.query
    classes = class_query.limit(limit).offset(
        (pageIndex - 1) * limit).all()
    number = list()
    time = list()
    for cla in classes:
        query = CourseArrange.query.filter(CourseArrange.classes_id == cla.id).filter(
            CourseArrange.class_timetable_id != None)
        course_arrange = query.all()
        size = len(course_arrange)
        if size > 0:
            time.append(course_arrange[size - 1].last_modify_time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            time.append('尚未更新')
        number.append(query.count())

    result = list()
    for cla, num, t in zip(classes, number, time):
        json = {
            'course_arrange_class': cla.class_name,
            'course_arrange_number': num,
            'last_modify_time': t,
            'class_id': cla.id,
        }
        result.append(json)

    return jsonify({
        'result': result,
        'success': True,
        'total': class_query.count()
    })


@api.route('/ajax/api/v1.0/teach_location')
def get_teach_location():
    try:
        teach_locations = TeachLocation.query.all()
        return jsonify({
            'result': [teach_location.to_json() for teach_location in teach_locations],
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/course_arrange', methods=['POST'])
def post_course_arrange():
    course_name = requestParameter('course_name')  # 添加课程名
    week = requestParameter('course_weeks')  # 周次
    time_start = requestParameter('course_arrange_time1')  # 起始节
    time_end = requestParameter('course_arrange_time2')  # 终止节
    location = requestParameter('course_arrange_site')  # 教学场所
    class_id = requestParameter('class_id')
    try:
        timetable = Timetable.query.filter(Timetable.period == time_start).first()
        timetable_end = Timetable.query.filter(Timetable.period == time_end).first()
        course = Course.query.filter(Course.course_name == course_name).first()
        teach_location = TeachLocation.query.filter(TeachLocation.loc_name == location).first()
        class_timetable = ClassTimeTable.query.filter(ClassTimeTable.classes_id == class_id).filter(
            ClassTimeTable.time_table_id == timetable.id).filter(ClassTimeTable.week == week).first()

        class_timetable.time_table_id_end = timetable_end.id  ## 添加终止节的id
        addToDb(class_timetable)
        course_arrange = CourseArrange.query.filter(CourseArrange.classes_id == class_id).all()
        for item in course_arrange:
            if item.course_id == course.id:
                raise CustomFlaskErr(COURSE_ALREADY_ARRANGE, 400)
        if class_timetable.check == 0:  # 未排课的时段
            class_timetable.check = 1
            addToDb(class_timetable)
            # 已排课的课程加入班级
            course_arrange = CourseArrange()
            course_arrange.classes_id = class_id
            course_arrange.class_timetable_id = class_timetable.id
            course_arrange.course_id = course.id
            course_arrange.course_location_id = teach_location.id
            addToDb(course_arrange)
            return jsonify({
                'success': True,
            })
        else:
            raise CustomFlaskErr(TEACH_TIME_DUPLICATION, 400)
    except Exception as error:
        if isinstance(error, CustomFlaskErr):
            return jsonify({'error_msg': str(error.return_code),
                            'success': False, })
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/course_time_table')
def get_class_course_arrange():
    class_name = requestParameter('class_name')
    try:
        classes = Classes.query.filter(Classes.class_name == class_name).first()
        course_arranges = CourseArrange.query.filter(CourseArrange.classes_id == classes.id).all()
        result = list()
        for course_arrange in course_arranges:
            course = Course.query.filter(Course.id == course_arrange.course_id).first()
            course_location = TeachLocation.query.filter(TeachLocation.id == course_arrange.course_location_id).first()
            class_timetable = ClassTimeTable.query.filter(
                ClassTimeTable.id == course_arrange.class_timetable_id).first()
            section1 = Timetable.query.filter(Timetable.id == class_timetable.time_table_id).first()
            section2 = Timetable.query.filter(Timetable.id == class_timetable.time_table_id_end).first()
            result.append({
                'semester': course.semester,
                'course_number': course.course_number,
                'course_name': course.course_name,
                'time_site': class_timetable.week + ' ' + section1.period + '至 ' + section2.period + ' ' + course_location.loc_name,
                'last_modify_time': course_arrange.last_modify_time.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return jsonify({
            'result': result,
            'success': True,
            'total': len(course_arranges),
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/get_colleague')
def get_Colleague():
    try:
        colleagues = Colleague.query.all()
        return jsonify({
            'result': [colleague.to_json() for colleague in colleagues],
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/get_profession')
def get_profession():
    collea_id = requestParameter('collea_id')
    try:
        professions = Profession.query.filter(Profession.colleague_id == collea_id).all()
        return jsonify({
            'result': [profession.to_json() for profession in professions],
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/get_class')
def get_class():
    prof_id = requestParameter('prof_id')
    try:
        classess = Classes.query.filter(Classes.profession_id == prof_id).all()
        return jsonify({
            'result': [classes.to_json() for classes in classess],
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/get_course_students')
def get_students_by_class():
    try:
        class_name = requestParameter('class_name')
        classes = Classes.query.filter(Classes.class_name == class_name).first()
        userinfos = UserInfo.query.filter(UserInfo.class_id == classes.id).all()
        return jsonify({
            'result': [userinfo.to_json() for userinfo in userinfos],
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/teachers')
def get_teacher_list():
    limit = request.args.get('limit', 10, type=int)  ## 一页大小
    offset = request.args.get('offset', 1, type=int)  ## 页码
    pageIndex = (offset / limit) + 1
    try:
        userinfo_query = UserInfo.query.filter(UserInfo.type == 1)
        userinfos = userinfo_query.limit(limit).offset(
            (pageIndex - 1) * limit).all()
        return jsonify({
            'result': [userinfo.to_json() for userinfo in userinfos],
            'success': True,
            'total': userinfo_query.count(),
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/teachers', methods=['DELETE'])
def delete_teacher():
    user_uid = requestParameter('user_uid')
    try:
        userinfo = UserInfo.query.filter(UserInfo.uid == user_uid).first()
        user = User.query.filter(User.id == userinfo.userid).first()
        delete_table_or_record(user)
        delete_table_or_record(userinfo)
        return jsonify({
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/teachers', methods=['PUT'])
def modify_teacher():
    user_name = requestParameter('teacher_name')
    job_number = requestParameter('teacher_jobnumber')
    uid = requestParameter('teacher_uid')
    try:
        userinfo = UserInfo.query.filter(UserInfo.uid == uid).first()
        userinfo.user_name = user_name
        userinfo.job_number = job_number
        userinfo.last_modify_time= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        addToDb(userinfo)
        user = User.query.filter(User.id == userinfo.userid).first()
        user.username = user_name
        user.last_modify_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        addToDb(user)
        return jsonify({
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/daily_schedule')
def daily_schedule():
    try:
        timetables = Timetable.query.all()
        return jsonify({
            'result': [timetable.to_json() for timetable in timetables],
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/daily_schedule', methods=['PUT'])
def modify_daily_schedule():
    id = requestParameter('daily_schedule_id')
    start_time = requestParameter('start_time')
    end_time = requestParameter('end_time')
    try:
        timetable = Timetable.query.filter(Timetable.id == id).first()
        timetable.start = start_time
        timetable.end = end_time
        timetable.last_modify_time= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        addToDb(timetable)
        return jsonify({
            'result': timetable.to_json(),
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/teach_site')
def teach_site():
    try:
        teachsites = TeachLocation.query.all()
        return jsonify({
            'result': [teachsite.to_json() for teachsite in teachsites],
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/teach_site', methods=['PUT'])
def modify_teach_site():
    id = requestParameter('teach_site_id')
    loc_name = requestParameter('loc_name')
    location = requestParameter('location')
    try:
        teach_site = TeachLocation.query.filter(TeachLocation.id == id).first()
        teach = TeachLocation.query.filter(TeachLocation.loc_name == loc_name).first()
        if teach is None:
            teach_site.loc_name = loc_name
            teach_site.location = location
            teach_site.last_modify_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            addToDb(teach_site)
            return jsonify({
                'result': teach_site.to_json(),
                'success': True,
            })
        else:
            raise CustomFlaskErr(SITE_ALREADY_EXIST, 400)
    except Exception as error:
        if isinstance(error, CustomFlaskErr):
            return jsonify({'error_msg': str(error.return_code),
                            'success': False, })
        return jsonify({'error_msg': str(error),
                        'success': False, })


@api.route('/ajax/api/v1.0/teach_site', methods=['DELETE'])
def delete_teach_site():
    id = requestParameter('teach_site_id')
    try:
        teach_site = TeachLocation.query.filter(TeachLocation.id == id).first()
        delete_table_or_record(teach_site)
        return jsonify({
            'success': True,
        })
    except Exception as error:
        return jsonify({'error_msg': str(error),
                        'success': False, })
