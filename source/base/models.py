from flask_login import UserMixin  # 管理用户会话的模块
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Float, SmallInteger, Boolean
from database import Base, db
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask import url_for
import hashlib


# 关联表(多对多)
# 用户课程关系表

class UserInfoCourse(Base):
    __tablename__ = 'userinfocourse'
    userinfo_id = Column(Integer, ForeignKey('userinfo.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)

    course = relationship('Course', backref='userinfo_ucourses')


# 角色权限表

class RolePermission(Base):
    __tablename__ = 'rolepermission'
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.id'), primary_key=True)
    alloc = Column(Integer, default=1)
    last_modify_time = Column(DateTime, default=datetime.now)

    permission = relationship('Permission', backref='role_permissions')

    # ## 角色菜单关联表 针对多对多中含额外属性


class RoleMenu(Base):
    __tablename__ = 'rolemenu'
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
    menu_id = Column(Integer, ForeignKey('menu.id'), primary_key=True)
    display = Column(Integer, default=1)
    last_modify_time = Column(DateTime, default=datetime.now)

    menu = relationship("Menu", backref='role_rolemenus')

    # orm对象经历的状态transient, pending, and persistent.


class User(Base, UserMixin):  # 继承UserMixin简便地实现用户类,配合flask-login使用
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 自增作为外键 关联其他表
    # uid = Column(String(40))
    username = Column(String(60))
    password = Column(String(32))
    # is_admin = Column(Boolean, default=False)
    # create_time = Column(DateTime, unique=True, default=datetime.datetime.utcnow())
    last_modify_time = Column(DateTime, unique=True, default=datetime.now)

    role_id = Column(Integer, ForeignKey('role.id'))  # 一个用户一种角色

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return str(self.username)


class UserInfo(Base):
    __tablename__ = 'userinfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(60), unique=True)
    uid = Column(String(40))
    sex = Column(SmallInteger, default=0)  # 0 未知， 1 男 2 女
    avatar = Column(String(150), default='')
    job_number = Column(String(32), unique=True)
    total_grade = Column(Float, default=0)
    type = Column(Integer)  # 0 表示管理员 1 表示教师 2 表示学生
    last_modify_time = Column(DateTime, default=datetime.now)

    # 外键
    class_id = Column(Integer, ForeignKey('classes.id'))  # 定义外键可通过UserInfo实例访问class信息
    userid = Column(Integer, ForeignKey('user.id'))

    # 关系(1vs1) uselist=False
    user = relationship('User', backref=backref("userinfo", uselist=False))
    courses = relationship('UserInfoCourse', backref='userinfo')

    def __init__(self, user_name, job_number, type):
        self.user_name = user_name
        self.job_number = job_number
        self.type = type

    # # 获取用户所有权限
    # @property
    # def permissions(self):
    #     return UserInfo.query.join(role_permission).join(Role).join(UserInfo).filter(UserInfo.id == self.id)

    # 获取用户所有可使用菜单
    # @property
    # def menus(self):
    #     return UserInfo.query.join(role_menu).join(Role).join(UserInfo).filter(UserInfo.id == self.id).order_by(
    #         Base.order)

    def __repr__(self):
        return str(self.user_name)

    def to_json(self):
        if self.job_number is None:
            self.job_number = ''
        if self.total_grade is None:
            self.total_grade = 0
        return {
            'user_name': self.user_name,
            'user_uid': self.uid,
            'sex': self.sex,
            'job_number': self.job_number,
            'total_grade': self.total_grade,
            'type': self.type,
        }


class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(32))
    uuid = Column(String(40))
    last_modify_time = Column(DateTime, default=datetime.now)

    # 外键
    profession_id = Column(Integer, ForeignKey(
        'profession.id'))  # a classes instance refers to one profession,but a profession refers to a list of classes

    # 关系
    students = relationship("UserInfo", backref="classes", lazy="dynamic")  # 一个班级可以有多个学生

    timetables = relationship('ClassTimeTable', backref='classes')  # 一个班级对应多个作息时间

    courses = relationship('CourseArrange', backref='classes')  # 一个班级对应多个课程

    def __init__(self, class_name):
        self.class_name = class_name

    def __repr__(self):
        return str(self.class_name)

    def to_json(self):
        return {
            'id': self.id,
            'class_name': self.class_name,
        }


class Profession(Base):
    __tablename__ = 'profession'
    id = Column(Integer, primary_key=True, autoincrement=True)
    prof_name = Column(String(32), unique=True)
    last_modify_time = Column(DateTime, default=datetime.now)
    uuid = Column(String(40))
    # 外键
    colleague_id = Column(Integer, ForeignKey('colleague.id'))

    # 关系
    classes = relationship("Classes", backref="profession", cascade="all, delete-orphan", single_parent=True,
                           passive_deletes=True,
                           lazy="joined")  # 一个专业多个班级 配置级联删除

    # courses = relationship("Course", backref="profession", lazy="dynamic")  # 一个专业多个课程

    def __init__(self, prof_name):
        self.prof_name = prof_name

    def __repr__(self):
        return str(self.prof_name)

    def to_json(self):
        return {
            'id': self.id,
            'prof_name': self.prof_name,
        }


class Colleague(Base):
    __tablename__ = 'colleague'
    id = Column(Integer, primary_key=True, autoincrement=True)
    colea_name = Column(String(32), unique=True)
    last_modify_time = Column(DateTime, default=datetime.now)
    uuid = Column(String(40))
    # 关系
    professions = relationship("Profession", backref="colleague", cascade="all, delete-orphan",  ##配置级联删除
                               single_parent=True, passive_deletes=True, lazy="joined")  # 一个学院多个专业

    def __init__(self, colea_name):
        self.colea_name = colea_name

    def __repr__(self):
        return str(self.colea_name)

    def to_json(self):
        return {
            'id': self.id,
            'colea_name': self.colea_name,
        }


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(32))
    course_number = Column(String(60))  ##课程编号
    course_week_times = Column(Integer)  # 课程所需周次
    semester = Column(String(32))  # 课程学期
    # course_time = Column(String(32))  # 上课时间
    # position = Column(String(32))  # 课程地点
    course_members = Column(Integer)  # 课程人数
    last_modify_time = Column(DateTime, default=datetime.now)

    # 外键
    profession_id = Column(Integer, ForeignKey('profession.id'))

    # 关系
    callnames = relationship("CallName", backref="course", lazy="dynamic")  # 一门课程多个点名信息

    def __repr__(self):
        return str(self.course_name)

    def to_json(self):
        json_course = {
            'id': self.id,
            'course_name': self.course_name,
            'course_number': self.course_number,
            'course_week_times': self.course_week_times,
            'last_modify_time': self.last_modify_time.strftime('%Y-%m-%d %H:%M:%S'),
            'semester': self.semester,
            # 'position': self.position,
            # 'course_time': self.course_time,
            'course_members': self.course_members,
        }
        return json_course


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(32), unique=True)
    role_desc = Column(String(200))
    last_modify_time = Column(DateTime, default=datetime.utcnow)

    permissions = relationship("RolePermission", backref='role')  # 角色权限多对多
    users = relationship("User", backref="role", lazy="dynamic")  # 每一角色有多个用户信息(此处不考虑用户拥有多角色)

    menus = relationship("RoleMenu", backref="role")

    def __init__(self, role_name, role_desc):
        self.role_name = role_name
        self.role_desc = role_desc

        ############# 创建角色立即分配权限 ##########
        # roles = Role.query.all()
        # if roles is not None:
        #     permissions = Permission.query.join(role_permission).join(Role).all()
        #     self.permissions.append(permissions)

    def __repr__(self):
        return str(self.role_name)

    def to_json(self):
        json_role = {
            'id': self.id,
            'role_name': self.role_name,
            'role_desc': self.role_desc,
            'last_modify_time': self.last_modify_time.strftime('%Y-%m-%d %H:%M:%S'),
            'permission': url_for('api.get_menu_role'),
        }
        return json_role


class Permission(Base):  ## 手动创建
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), )  # func.__doc__作为名字
    action = Column(String(60))  # 由func.__module__ 和 func.__name__组成
    perm_desc = Column(String(100))  # 具体权限描述
    last_modify_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return str(self.name)

    def to_json(self):
        json_permission = {
            'id': self.id,
            'name': self.name,
            'perm_desc': self.perm_desc,
            'last_modify_time': self.last_modify_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return json_permission


class Menu(Base):  ## 手动创建
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    icon = Column(String(50))
    url = Column(String(100))
    order = Column(SmallInteger, default=0)
    parent_id = Column(Integer, default=0)
    menu_type = Column(Integer)
    # display = Column(Integer)
    create_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return str(self.name)

    def to_json(self):
        if self.url is None:
            self.url = ''
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'url': self.url,
            'order': self.order,
            'parent_id': self.parent_id,
            'menu_type': self.menu_type,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class CallName(Base):
    __tablename__ = 'callname'
    id = Column(Integer, primary_key=True, autoincrement=True)
    checkin_time = Column(DateTime, default=False)  # 签到时间
    checkin_type = Column(Integer, default=0)  # 考勤类型 0:缺席 1:请假 2:出席
    checkin_uid = Column(String(60))  # 点名学生的uid
    course_name = Column(String(20))  # 点名的课程名
    checkin_grade = Column(Float)  # 考勤得分
    last_modify_time = Column(DateTime, default=datetime.now)

    # 外键
    course_id = Column(Integer, ForeignKey('course.id'))

    def __init__(self, checkin_time, checkin_type, checkin_uid, course_name, checkin_grade):
        self.checkin_time = checkin_time
        self.checkin_type = checkin_type
        self.checkin_uid = checkin_uid
        self.course_name = course_name
        self.checkin_grade = checkin_grade

    def __repr__(self):
        return str(self.checkin_grade)

    def to_json(self):
        return {
            'checkin_time': self.checkin_time,
            'checkin_type': self.checkin_type,
            'checkin_uid': self.checkin_uid,
            'course_name': self.course_name,
            'checkin_grade': self.checkin_grade,
            'last_modify_time': self.last_modify_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class Admin(Base):  # 管理员管理表
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    absent_std = Column(Integer, default=0)
    absent_level_warn = Column(Integer, default=0)  # 缺课达到课程时长的一半
    late_absent = Column(DateTime)  # 迟到时长达到旷课的标准
    notice = Column(String(200))  # 公告

    last_modify_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return str(self.absent_std)


class Timetable(Base):  # 作息时间表
    __tablename__ = 'timetable'
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(String(10))  # 节次
    start = Column(String(40))  # 上课时间
    end = Column(String(40))  # 下课时间
    last_modify_time = Column(DateTime, default=datetime.now)

    def __init__(self, period, start, end):
        self.period = period
        self.start = start
        self.end = end

    def to_json(self):
        return {
            'period': self.period,
            'start': self.start,
            'end': self.end,
            'last_modify_time': self.last_modify_time.strftime('%Y-%m-%d %H:%M:%S')
        }


class ClassTimeTable(Base):  # 班级作息关系表
    __tablename__ = 'class_timetable'
    id = Column(Integer, primary_key=True, autoincrement=True)
    classes_id = Column(Integer, ForeignKey('classes.id'), primary_key=True)
    time_table_id = Column(Integer, ForeignKey('timetable.id'), primary_key=True)  # 起始节id
    time_table_id_end = Column(Integer, default=-1)  # 终止节id
    week = Column(String(10))
    check = Column(Integer, default=0)

    timetable = relationship('Timetable', backref='timetables')  # 关联的每一个时间表对象 child  Classes 类似Parent


class TeachLocation(Base):
    __tablename__ = 'teach_location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    loc_name = Column(String(40))
    location = Column(String(20))

    def to_json(self):
        return {
            'id': self.id,
            'loc_name': self.loc_name,
            'location': self.location,
        }


class CourseArrange(Base):
    __tablename__ = 'course_arrange'
    classes_id = Column(Integer, ForeignKey('classes.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)
    class_timetable_id = Column(Integer, ForeignKey('class_timetable.id'), primary_key=True)  ## 授课时间
    course_location_id = Column(Integer, ForeignKey('teach_location.id'), primary_key=True)  # 授课地点

    last_modify_time = Column(DateTime, default=datetime.now)
    # course = relationship('Course', backref='course_arranges')


class DataDictTable(Base):  ## 数据字典表
    __tablename__ = 'data_dict_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dict_item = Column(String(20))  # 字典项
    dict_value = Column(String(20))  # 字典值
    last_modify_time = Column(DateTime, default=datetime.now)
