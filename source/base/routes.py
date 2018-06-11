from datetime import datetime
from flask import Blueprint, render_template, redirect, request, url_for, g, flash, send_from_directory, jsonify
import uuid
import hashlib
from flask_login import (
    current_user,
    LoginManager,
    login_required,
    login_user,
    logout_user
)

from .forms import LoginForm, CreateAccountForm

# start the login system 登录管理类
login_manager = LoginManager()
# 使用Flask 蓝图
blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)

from database import db
from .models import User, UserInfo, Role, Colleague


def route_colleague():
    a = ['数计学院', '经管学院', '空间中心', '电气学院', '土木学院', '物信学院']
    for item in list(a):
        colleague = Colleague(colea_name=item)
        db.session.add(colleague)
    db.session.commit()


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')


@blueprint.route('/fixed_<template>')
@login_required
def route_fixed_template(template):
    return render_template('fixed/fixed_{}.html'.format(template))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))


## Login & Registration process


def allocateRole(user, role_name):
    role = Role.query.filter_by(role_name=role_name).first()
    if role:
        user.role_id = role.id  # 用户注册时分配管理员角色
    return user
    # teacher_role = Role.query.filter_by(role_name='教师').first()
    # if teacher_role:
    #     user.role_id = teacher_role.id  # 用户注册时分配教师角色


def register(role_name, type):
    login_form = LoginForm(request.form)
    username = str(request.form['username'])
    password = str(request.form['password'])

    if role_name == '管理员':
        if not username.startswith('A'):
            flash('管理员账户必须以A开头')
            return redirect(url_for('base_blueprint.login'))
    elif role_name == '教师':
        if not username.startswith('T'):
            flash('教师账户必须以T开头')
            return redirect(url_for('base_blueprint.login'))
    else:
        return render_template('errors/page_403.html')
    if len(username) == 0 and len(password) == 0:
        return render_template('errors/page_403.html')
    user = User.query.filter_by(username=username).first()
    if user:  ##防止重复注册
        return render_template('errors/page_403.html')
    # user = User(**request.form)
    user = User(username)
    # md5=hashlib.md5()
    # user.password=md5.update(password.encode('utf-8'))
    user.password = password
    # 分配角色
    user = allocateRole(user, role_name)
    # 创建用户信息表
    db.session.add(user)
    db.session.commit()
    userinfo = UserInfo(username, None, type)
    userinfo.userid = user.id
    # userinfo.type = type
    userinfo.uid = str(uuid.uuid4())  # 利用uuid生成唯一标识字符串作为id
    # userinfo.user_name = username
    db.session.add(userinfo)
    db.session.commit()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'login' in request.form:  # 登录
        username = str(request.form['username'])
        password = str(request.form['password'])
        user = db.session.query(User).filter_by(username=username).first()
        # md5=hashlib.md5()
        if user and password == user.password:
            login_user(user)  # 允许登入用户
            # next = request.args.get('next')
            # # next_is_valid should check if the user has valid
            # # permission to access the `next` url
            # if not next_is_valid(next):
            #     return flask.abort(400)
            return redirect(url_for('base_blueprint.route_default'))
        flash('帐号密码错误')
        return redirect(url_for('base_blueprint.login'))
    elif 'admin_create_account' in request.form:  # 注册
        return register("管理员", 0)
    elif 'teacher_create_account' in request.form:  # 教师注册
        return register("教师", 1)
    if not current_user.is_authenticated:  # 用户未通过验证返回登录页面
        return render_template(
            'login/login.html',
            login_form=login_form,
            create_account_form=create_account_form
        )
    return redirect(url_for('student_blueprint.get_student_list'))

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


## Errors pages


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500

