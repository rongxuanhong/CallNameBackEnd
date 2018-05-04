from flask import Blueprint, render_template, redirect, request, url_for
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
from .models import User


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


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'login' in request.form: # 登录
        username = str(request.form['username'])
        password = str(request.form['password'])
        user = db.session.query(User).filter_by(username=username).first()
        if user and password == user.password:
            login_user(user) #允许登入用户
            # next = request.args.get('next')
            # # next_is_valid should check if the user has valid
            # # permission to access the `next` url
            # if not next_is_valid(next):
            #     return flask.abort(400)
            return redirect(url_for('base_blueprint.route_default'))
        return render_template('errors/page_403.html')
    elif 'create_account' in request.form: # 注册
        login_form = LoginForm(request.form)
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('base_blueprint.login'))
    if not current_user.is_authenticated:# 用户未通过验证返回登录页面
        return render_template(
            'login/login.html',
            login_form=login_form,
            create_account_form=create_account_form
        )
    return redirect(url_for('home_blueprint.index'))


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