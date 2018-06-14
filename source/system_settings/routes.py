from flask import Blueprint, render_template, request
from flask_login import login_required
from database import db
from flask_restful import Resource, Api

from base.models import Colleague, Profession, Classes, UserInfo

blueprint = Blueprint(
    'system_blueprint',
    __name__,
    url_prefix='/system_settings',
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')
