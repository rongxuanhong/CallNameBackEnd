from base.models import Colleague, Profession, Classes, UserInfo, User, Role, Permission, Course, Menu, RoleMenu, \
    RolePermission, Timetable, ClassTimeTable, TeachLocation, CourseArrange, DataDictTable, CallName
from database import db, Base
from flask import jsonify
import uuid
from sqlalchemy import and_, text


def route_colleague0():
    colleagues = ['数计学院', '经管学院', '空间中心', '电气学院', '土木学院', '物信学院']
    for item in list(colleagues):
        colleague = Colleague(colea_name=item)
        db.session.add(colleague)
    db.session.commit()


def route_colleague1():
    colleagues = ['外国语学院', '环境工程学院', '化工学院']
    for item in list(colleagues):
        colleague = Colleague(colea_name=item)
        db.session.add(colleague)
    db.session.commit()


def route_profession1():
    professions = ['计算机技术', '软件工程', '离散中心', '应用数学']
    colleague = Colleague.query.filter_by(colea_name='数计学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_profession2():
    professions = ['通信工程', '电子信息工程', '电子科学与技术', '光电信息工程', '微电子', '物理学', '数字媒体与网络工程', '物联网工程']
    colleague = Colleague.query.filter_by(colea_name='物信学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_profession4():
    professions = ['建筑学', '城乡规划', '风景园林']
    colleague = Colleague.query.filter_by(colea_name='建筑学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_profession5():
    professions = ['电气工程', '电力工程', '应用电子', '自动化']
    colleague = Colleague.query.filter_by(colea_name='电气学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_profession6():
    professions = ['建筑工程', '道路与桥梁工程', '市政工程', '交通运输工程']
    colleague = Colleague.query.filter_by(colea_name='土木学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_profession7():
    professions = ['英语', '日语', '德语', ]
    colleague = Colleague.query.filter_by(colea_name='外国语学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_profession3():
    professions = ['管理科学与工程', '工商管理', '信息管理与信息系统', '物流管理', '金融工程', '会计学', '旅游管理', '经济与产业系统管理']
    colleague = Colleague.query.filter_by(colea_name='经管学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_profession10():
    professions = ['科技与教育管理']
    colleague = Colleague.query.filter_by(colea_name='经管学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_class():
    profesion1 = Profession.query.filter_by(prof_name='计算机技术').first()
    profesion2 = Profession.query.filter_by(prof_name='软件工程').first()
    data = [('17专硕1班', profesion1), ('17专硕2班', profesion2)]
    for item1, item2 in list(data):
        cla = Classes(item1)
        cla.profession_id = item2.id
        db.session.add(cla)
    db.session.commit()


def route_class2():
    profesion1 = Profession.query.filter_by(prof_name='英语').first()
    profesion2 = Profession.query.filter_by(prof_name='德语').first()
    profesion3 = Profession.query.filter_by(prof_name='日语').first()
    data = [('17英语1班', profesion1), ('17德语1班', profesion2), ('17英语2班', profesion1), ('17德语2班', profesion2),
            ('17日语1班', profesion3), ('17日语2班', profesion3), ]
    for item1, item2 in list(data):
        cla = Classes(item1)
        cla.profession_id = item2.id
        db.session.add(cla)
    db.session.commit()


def route_class3():
    profesion1 = Profession.query.filter_by(prof_name='电子科学与技术').first()
    profesion2 = Profession.query.filter_by(prof_name='光电信息工程').first()
    data = [('17电子1班', profesion1), ('17光电1班', profesion2), ('17电子2班', profesion1), ('17光电2班', profesion2)]
    for item1, item2 in list(data):
        cla = Classes(item1)
        cla.profession_id = item2.id
        db.session.add(cla)
    db.session.commit()


def route_student1():
    data = [('鲍尔', 'N170427094', 2), ('库兹马', 'N170427096', 2), ('哈特', 'N170427097', 2), ('兰德尔', 'N1704270100', 2),
            ('波普', 'N170427095', 2), ('威尔', 'N170427098', 2), ('托马斯', 'N170427099', 2), ('卡鲁索', 'N1704270101', 2),
            ('祖巴茨', 'N170427093', 2), ('哈登', 'N170427092', 2), ('保罗', 'N170427091', 2), ('克莱汤普森', 'N170427090', 2)]
    for item1, item2, item3 in list(data):
        user_info = UserInfo(item1, item2, item3)
        user_info.class_id = 3
        db.session.add(user_info)
    db.session.commit()


def route_student3():
    data = [('科比', 'N170327094', 2), ('詹姆斯', 'N170327096', 2), ('奥拉迪波', 'N170327097', 2), ('库里', 'N1703270100', 2)]
    for item1, item2, item3 in list(data):
        user_info = UserInfo(item1, item2, item3)
        user_info.class_id = 2
        db.session.add(user_info)
    db.session.commit()


def route_student2():
    data = [('杜兰特', 'N170327020', 2), ('格林', 'N1703270120', 2), ('米切尔', 'N170327001', 2), ('尼克杨', 'N170327099', 2),
            ('欧文', 'N170327019', 2), ('韦德', 'N1703270110', 2), ('沃顿', 'N170327002', 2), ('英格拉姆', 'N170327098', 2), ]
    for item1, item2, item3 in list(data):
        user_info = UserInfo(item1, item2, item3)
        user_info.class_id = 2
        db.session.add(user_info)
    db.session.commit()


def route_student4():
    data = [('布莱德索', 'N170527094', 2), ('帕克', 'N170527096', 2), ('邓肯', 'N170527097', 2), ('奥拉朱旺', 'N1705270100', 2),
            ('姚明', 'N170527095', 2), ('巴特勒', 'N170527098', 2), ('唐斯', 'N170527099', 2), ('维金斯', 'N1705270101', 2),
            ('雷迪克', 'N170527093', 2), ('恩比德', 'N170527092', 2), ('本西蒙斯', 'N170527091', 2), ('乔西蒙斯', 'N170527090', 2)]
    for item1, item2, item3 in list(data):
        user_info = UserInfo(item1, item2, item3)
        user_info.class_id = 4
        db.session.add(user_info)
    db.session.commit()


def route_relation():
    students = db.session.query(UserInfo.user_name, UserInfo.job_number,
                                Classes.class_name, Profession.prof_name, Colleague.colea_name,
                                UserInfo.last_modify_time, UserInfo.id).join(
        Colleague.professions).filter(Colleague.colea_name == '数计学院').join(
        Profession.classes).join(
        Classes.students).filter(Classes.class_name == '17专硕2班').all()
    studentss = []
    for student in students:
        s = {'user_name': student[0],
             'job_number': student[1],
             'class_name': student[2],
             'profession_name': student[3],
             'colleague_name': student[4],
             'last_modify_time': student[5],
             'userinfo_id': student[6], }
        studentss.append(s)
    print(jsonify({
        'students': studentss
    }))


def route_role():
    role1 = Role('管理员', '管理员角色')
    role2 = Role('教师', '教师角色')
    role3 = Role('学生', '学生角色')
    db.session.add(role1)
    db.session.add(role2)
    db.session.add(role3)
    db.session.commit()


def op():
    permission = Permission()
    permission.action = '/student_management/'
    permission.name = '学生管理'
    permission.perm_desc = '学生管理'
    db.session.add(permission)
    db.session.commit()


def course():
    cours = Course()
    cours.position = '东二 2#506'
    cours.course_name = '工程训练'
    cours.course_week_times = '10'
    cours.semester = '2017-2018学年第二学期'
    cours.course_number = 'UCREEUEUEEEE'
    cours.course_time = '周一'
    cours.profession_id = 5
    db.session.add(cours)
    db.session.commit()


def op1():
    student = db.session.query(UserInfo.user_name, UserInfo.job_number,
                               Classes.class_name, Profession.prof_name, Colleague.colea_name,
                               UserInfo.last_modify_time, UserInfo.uid).join(
        Colleague.professions).join(Profession.classes).join(
        Classes.students).filter(UserInfo.uid == '1e88f6f8-4cb0-40e5-894a-3c244e191c04').first()
    return student


def addToDb(table):
    db.session.add(table)
    db.session.commit()


def set_menu():
    role = Role.query.filter(Role.role_name == '管理员').first()

    rolemenu = RoleMenu(display=1)  ## 创建关联记录
    menu1 = Menu()  ## 创建菜单
    menu1.name = '学生管理'
    menu1.icon = 'fa fa-table'
    menu1.menu_type = 1
    menu1.order = 1
    rolemenu.menu = menu1  ## 关联表存菜单
    role.menus.append(rolemenu)
    addToDb(role)
    rolemenu = RoleMenu(display=1)
    menu = Menu()
    menu.name = '学生列表'
    menu.icon = 'fa fa-table'
    menu.menu_type = 2
    menu.order = 11
    menu.parent_id = menu1.id
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)
    rolemenu = RoleMenu(display=1)
    menu2 = Menu()
    menu2.name = '教师管理'
    menu2.icon = 'fa fa-table'
    menu2.menu_type = 1
    menu2.order = 2
    rolemenu.menu = menu2
    role.menus.append(rolemenu)
    addToDb(role)
    rolemenu = RoleMenu(display=1)
    menu = Menu()
    menu.name = '教师列表'
    menu.icon = 'fa fa-table'
    menu.menu_type = 2
    menu.order = 21
    menu.parent_id = menu2.id
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)
    rolemenu = RoleMenu(display=1)
    menu3 = Menu()
    menu3.name = '课程管理'
    menu3.icon = 'fa fa-table'
    menu3.menu_type = 1
    menu3.order = 3
    rolemenu.menu = menu3
    role.menus.append(rolemenu)
    addToDb(role)
    rolemenu = RoleMenu(display=1)
    menu = Menu()
    menu.name = '课程列表'
    menu.icon = 'fa fa-table'
    menu.menu_type = 2
    menu.order = 31
    menu.parent_id = menu3.id
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)
    rolemenu = RoleMenu(display=1)
    menu4 = Menu()
    menu4.name = '数据权限管理'
    menu4.icon = 'fa fa-table'
    menu4.menu_type = 1
    menu4.order = 4
    rolemenu.menu = menu4
    role.menus.append(rolemenu)
    addToDb(role)
    rolemenu = RoleMenu(display=1)
    menu = Menu()
    menu.name = '组织管理'
    menu.icon = 'fa fa-table'
    menu.menu_type = 2
    menu.order = 41
    menu.parent_id = menu4.id
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)
    rolemenu = RoleMenu(display=1)
    menu = Menu()
    menu.name = '权限管理'
    menu.icon = 'fa fa-table'
    menu.menu_type = 2
    menu.order = 42
    menu.parent_id = menu4.id
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)
    rolemenu = RoleMenu(display=1)
    menu = Menu()
    menu.name = '角色管理'
    menu.icon = 'fa fa-table'
    menu.menu_type = 2
    menu.order = 43
    menu.parent_id = menu4.id
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)


def set_menu1():
    role = Role.query.filter(Role.role_name == '教师').first()

    menu = Menu.query.filter(Menu.name == '学生管理').first()
    rolemenu = RoleMenu(display=1)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '学生列表').first()
    rolemenu = RoleMenu(display=1)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '教师管理').first()
    rolemenu = RoleMenu(display=0)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '教师列表').first()
    rolemenu = RoleMenu(display=0)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '课程管理').first()
    rolemenu = RoleMenu(display=1)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '课程列表').first()
    rolemenu = RoleMenu(display=1)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '数据权限管理').first()
    rolemenu = RoleMenu(display=0)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '组织管理').first()
    rolemenu = RoleMenu(display=0)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '权限管理').first()
    rolemenu = RoleMenu(display=0)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '角色管理').first()
    rolemenu = RoleMenu(display=0)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)


def route_class5():
    profesion1 = Profession.query.filter_by(prof_name='离散中心').first()
    profesion2 = Profession.query.filter_by(prof_name='应用数学').first()
    profesion3 = Profession.query.filter_by(prof_name='通信工程').first()
    profesion4 = Profession.query.filter_by(prof_name='电子信息工程').first()
    profesion5 = Profession.query.filter_by(prof_name='管理科学与工程').first()
    profesion6 = Profession.query.filter_by(prof_name='工商管理').first()
    profesion7 = Profession.query.filter_by(prof_name='会计学').first()
    profesion8 = Profession.query.filter_by(prof_name='建筑学').first()
    profesion9 = Profession.query.filter_by(prof_name='城乡规划').first()
    profesion10 = Profession.query.filter_by(prof_name='风景园林').first()
    profesion11 = Profession.query.filter_by(prof_name='电力工程').first()
    profesion12 = Profession.query.filter_by(prof_name='应用电子').first()
    profesion13 = Profession.query.filter_by(prof_name='自动化').first()
    profesion14 = Profession.query.filter_by(prof_name='建筑工程').first()
    profesion15 = Profession.query.filter_by(prof_name='道路与桥梁工程').first()
    profesion16 = Profession.query.filter_by(prof_name='市政工程').first()
    profesion17 = Profession.query.filter_by(prof_name='交通运输工程').first()
    data = [('17离散1班', profesion1), ('17应数1班', profesion2), ('17离散2班', profesion1), ('17应数2班', profesion2),
            ('17通信1班', profesion3), ('17通信2班', profesion3),
            ('17电信1班', profesion4), ('17电信2班', profesion4),
            ('17管科1班', profesion5), ('17管科2班', profesion5),
            ('17工管1班', profesion6), ('17工管2班', profesion6),
            ('17会计1班', profesion7), ('17会计2班', profesion7),
            ('17建筑1班', profesion8), ('17建筑2班', profesion8),
            ('17城规1班', profesion9), ('17城规2班', profesion9),
            ('17风圆1班', profesion10), ('17风圆2班', profesion10),
            ('17电工1班', profesion11), ('17电工2班', profesion11),
            ('17应电1班', profesion12), ('17应电2班', profesion12),
            ('17自动1班', profesion13), ('17自动2班', profesion13),
            ('17建工1班', profesion14), ('17建工2班', profesion14),
            ('17道桥1班', profesion15), ('17道桥2班', profesion15),
            ('17市政1班', profesion16), ('17市政2班', profesion16),
            ('17交通1班', profesion17), ('17交通2班', profesion17), ]
    for item1, item2 in list(data):
        cla = Classes(item1)
        cla.profession_id = item2.id
        db.session.add(cla)
    db.session.commit()


def addUUID():
    colleagues = Colleague.query.all()
    for colleague in colleagues:
        colleague.uuid = str(uuid.uuid4())
        db.session.add(colleague)
    professions = Profession.query.all()
    for profession in professions:
        profession.uuid = str(uuid.uuid4())
        db.session.add(profession)
    classes = Classes.query.all()
    for cla in classes:
        cla.uuid = str(uuid.uuid4())
        db.session.add(cla)
    db.session.commit()


def addPermission():
    role = Role.query.filter(Role.role_name == '教师').first()
    permission = Permission()
    permission.name = '注册'
    permission.perm_desc = '注册权限'

    role_permission = RolePermission()
    role_permission.permission = permission
    role_permission.alloc = 0
    role.permissions.append(role_permission)
    addToDb(permission)
    addToDb(role_permission)


def add_menu():
    role = Role.query.filter(Role.role_name == '管理员').first()

    menu = Menu.query.filter(Menu.name == '授课安排').first()
    rolemenu = RoleMenu(display=1)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '课表查询').first()
    rolemenu = RoleMenu(display=1)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)


def createClassTimeTable(item, str, weeks):
    timetable = Timetable.query.filter(Timetable.period == str).first()
    for week in weeks:
        classtime = ClassTimeTable()
        classtime.week = week
        classtime.timetable = timetable
        item.timetables.append(classtime)
        addToDb(item)


def addTimeTable():
    classes = Classes.query.all()
    weeks = ['周一', '周二', '周三', '周四', '周五']
    for item in classes[:10]:
        createClassTimeTable(item, '第一节', weeks)
        createClassTimeTable(item, '第二节', weeks)
        createClassTimeTable(item, '第三节', weeks)
        createClassTimeTable(item, '第四节', weeks)
        createClassTimeTable(item, '第五节', weeks)
        createClassTimeTable(item, '第六节', weeks)
        createClassTimeTable(item, '第七节', weeks)
        createClassTimeTable(item, '第八节', weeks)
        createClassTimeTable(item, '第九节', weeks)
        createClassTimeTable(item, '第十节', weeks)
        createClassTimeTable(item, '第十一节', weeks)
        createClassTimeTable(item, '第十二节', weeks)


def addTimeTable2():
    timetable = Timetable('第一节', '8:20', '9:05')
    addToDb(timetable)
    timetable = Timetable('第二节', '9:15', '10:00')
    addToDb(timetable)
    timetable = Timetable('第三节', '10:20', '11:05')
    addToDb(timetable)
    timetable = Timetable('第四节', '11:15', '12:00')
    addToDb(timetable)
    timetable = Timetable('第五节', '14:00', '14:45')
    addToDb(timetable)
    timetable = Timetable('第六节', '14:55', '15:40')
    addToDb(timetable)
    timetable = Timetable('第七节', '15:50', '16:35')
    addToDb(timetable)
    timetable = Timetable('第八节', '16:45', '17:30')
    addToDb(timetable)
    timetable = Timetable('第九节', '18:00', '18:45')
    addToDb(timetable)
    timetable = Timetable('第十节', '18:55', '19:40')
    addToDb(timetable)
    timetable = Timetable('第十一节', '19:50', '20:35')
    addToDb(timetable)
    timetable = Timetable('第十二节', '20:45', '21:30')
    addToDb(timetable)


def addTeachLocation():
    locations = ['东三202', '东三102', '东二505', '东二203']

    for location in locations:
        a = TeachLocation()
        a.location = location
        addToDb(a)


def course_arrange():
    class_timetable = ClassTimeTable.query.filter(ClassTimeTable.classes_id == 1).filter(
        ClassTimeTable.time_table_id == 1).filter(ClassTimeTable.week == '周一').first()

    print(class_timetable.id)


def user():
    user = User.query.filter(User.username == 'student').first()
    userinfo = UserInfo(user.username, 'N140327098', 2)
    userinfo.uid = str(uuid.uuid4())
    userinfo.userid = user.id
    userinfo.class_id = 1
    addToDb(userinfo)


def addDataDict():
    data = DataDictTable()
    data.dict_item = '签到范围'
    data.dict_value = '10m'
    addToDb(data)


def add_menu_1():
    role = Role.query.filter(Role.role_name == '教师').first()
    menu = Menu.query.filter(Menu.name == '系统设置').first()
    rolemenu = RoleMenu(display=1)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)


def add_menu_2():
    role = Role.query.filter(Role.role_name == '管理员').first()
    rolemenu = RoleMenu(display=1)
    menu = Menu()
    menu.name = '作息时间设置'
    menu.icon = 'fa fa-table'
    menu.menu_type = 2
    menu.order = 51
    # menu.parent_id = menu4.id
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)
    rolemenu = RoleMenu(display=1)
    menu = Menu()
    menu.name = '教学场所设置'
    menu.icon = 'fa fa-table'
    menu.menu_type = 2
    menu.order = 52
    # menu.parent_id = menu4.id
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)


def add_menu_3():
    role = Role.query.filter(Role.role_name == '教师').first()
    menu = Menu.query.filter(Menu.name == '作息时间设置').first()
    rolemenu = RoleMenu(display=1)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)

    menu = Menu.query.filter(Menu.name == '教学场所设置').first()
    rolemenu = RoleMenu(display=1)
    rolemenu.menu = menu
    role.menus.append(rolemenu)
    addToDb(role)


def get_teach_site():
    role = Role.query.filter(Role.role_name == '管理员').first()
    sites = TeachLocation.query.all()
    for site in sites:
        site.last_modify_time = role.last_modify_time
        addToDb(site)


def add_call_name():
    import re
    a='(119.131,26.150)'
    a=re.split('[,()]',a)
    print(a)


if __name__ == '__main__':
    add_call_name()
