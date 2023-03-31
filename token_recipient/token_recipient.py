import os
import sys

directory = os.getcwd()

print(directory)
print(os.listdir())
import flask
import requests
from flask import request, jsonify, render_template
from sqlalchemy import update

sys.path.append('../app')
from data import db_session
from data.users import Users

blueprint = flask.Blueprint(
    'token_recipient_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/set_authorization_code_flow_token', methods=["GET"])
def set_authorization_code_flow_token():
    code = request.args.get("code")
    state = request.args.get("state")
    print(request, code)
    url = "https://oauth.vk.com/access_token"
    params = {
        "client_id": os.environ.get('VK_CLIENT_ID'),
        "client_secret": os.environ.get('VK_CLIENT_SECRET'),
        "redirect_uri": os.environ.get('SET_TOKEN_SITE_LINK') + os.environ.get('SET_TOKEN_PATH'),
        "code": code
    }
    response = requests.get(url, params=params).json()
    print(response)
    # return response
    db_sess = db_session.create_session()
    db_sess.execute(update(Users).values(vk_access_token=response["access_token"]).where(Users.id == state))
    db_sess.commit()
    # return render_template('success.html', title='Успех')
    return "success"


@blueprint.route('/api/set_implicit_flow_token', methods=["GET"])
def set_implicit_flow_token():

    access_token = request.args.get("access_token")
    state = request.args.get("state")
    db_sess = db_session.create_session()
    db_sess.execute(update(Users).values(vk_access_token=access_token).where(Users.id == state))
    db_sess.commit()
    # return render_template('success.html', title='Успех')
    return "success"


@blueprint.route('/api/get_token/<int:user_id>', methods=["GET"])
def get_token(user_id):
    return "token"
