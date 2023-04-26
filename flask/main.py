import os
import datetime
from io import BytesIO

import sqlalchemy
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request

import logging
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import update, select

from data import db_session
from data.posts import Posts
from data.tags import Tags
from data.token_link import get_user_implicit_flow_link, get_user_token_link
from data.users import Users
from deviantart_checker.parser import get_tag_last_deviant_id
from forms.loginform import LoginForm
from forms.post_form import PostForm
from forms.registerform import RegisterForm
from VK import vk_main, vk_api
from forms.vk_token_form import VkTokenForm
from images.images import create_byte_image

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mega_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route('/')
@app.route('/home')
def home():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с таким email уже существует")
        if db_sess.query(Users).filter(Users.name == form.username.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с таким логином уже существует")
        user = Users(
            email=form.email.data,
            name=form.username.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        print(
            form.email,
            form.username,
            form.password,
            form.check_password,
            sep="\n"
        )
        return redirect('/success')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        # user = db_sess.query(Users).filter(Users.name == form.username.data).first()
        user = db_sess.execute(select(Users).where(Users.name == form.username.data)).scalars().first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/success')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/success')
def success():
    return render_template('success.html', title='Успех', message="Мы получили этот запрос, значит всё будет классно.")


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    db_sess = db_session.create_session()
    user_id = current_user.id
    user_vk_access_token = db_sess.execute(
        sqlalchemy.select(Users.vk_access_token).where(Users.id == user_id)).scalars().first()
    logging.warning(user_vk_access_token)
    vk = vk_api.VK_Api(user_vk_access_token)
    groups = vk.groups_get(filter=["moder"], count=20)
    groups_ids = groups["response"]["items"]
    form.id.data = groups_ids[0]
    form.id.choices = groups_ids
    if form.validate_on_submit():
        logging.warning(form.data)
        if user_vk_access_token == "" or isinstance(user_vk_access_token, type(None)):
            return redirect("/vk_access_token")
        group_id = "-" + str(form.id.data)
        tag = form.tag.data
        if tag != "":
            entry = db_sess.execute(
                select(Tags).where(Tags.tag == tag)).scalars().first()
            if isinstance(entry, type(None)):
                tags = Tags(
                    tag=tag,
                    last_deviant_id=get_tag_last_deviant_id(tag)
                )
                db_sess.add(tags)
                db_sess.commit()
            else:
                db_sess.execute(update(Tags).values(last_deviant_id=get_tag_last_deviant_id(tag)).where(Tags.tag==tag))
            create_deviantart_posts(group_id, tag, "-1")

        images = list()
        raw_images = form.images.data
        if raw_images[0].filename != "":
            for raw_image in raw_images:
                image = raw_image.stream.read()
                images.append(create_byte_image(image))
            start_on = form.start_on.data
            interval = form.interval.data
            posts = vk_main.create_posts(user_vk_access_token, images, group_id, start_on, interval)
            for post in posts:
                post.post()
            logging.warning("POSTED!!!!")
        if tag == "" and raw_images[0].filename == "":
            return render_template('error.html', title="Ошибка",
                                   message="Вы не выбрали тег и не прикрепили ни одного изображения")
        return render_template('success.html', title='Успех',
                               message="Мы получили этот запрос, значит всё будет классно.")

    return render_template('post.html', title='Пост', form=form)


@app.route('/vk_access_token', methods=['GET', 'POST'])
@login_required
def access_token():
    form = VkTokenForm()
    user_id = current_user.id
    user_vk_access_token = db_sess.execute(
        sqlalchemy.select(Users.vk_access_token).where(Users.id == user_id)).scalars().first()
    if form.validate_on_submit():
        vk_access_token = form.token.data
        logging.warning(vk_access_token)
        db_sess.execute(update(Users).values(vk_access_token=vk_access_token).where(Users.id == user_id))
        db_sess.commit()
        return render_template('success.html', title='Успех',
                               message="Мы получили этот запрос, значит всё будет классно.")
    logging.warning(user_id)
    logging.warning(user_vk_access_token)
    token_link = get_user_token_link(os.environ.get('VK_CLIENT_ID'), os.environ.get('VK_CLIENT_SECRET'),
                                     os.environ.get('SET_FLOW_SITE_LINK') + os.environ.get(
                                         'SET_IMPLICIT_FLOW_PATH'),
                                     ["notify", "friends", "photos", "audio", "video", "pages", "menu",
                                      "status",
                                      "notes", "wall", "ads", "offline", "docs", "groups",
                                      "notifications", "stats", "email", "market", ], user_id)
    return render_template("need_vk_token.html", vk_token_link=token_link, form=form)


# @app.route('/create', methods=["GET", "POST"])
# @login_required
def create_deviantart_posts(group_id, tag, amount):
    db_sess = db_session.create_session()
    user_id = current_user.id
    entry = db_sess.execute(
        select(Posts).where(Posts.user_id == user_id and Posts.tag == tag and Posts.group_id == group_id)).scalars().first()
    if isinstance(entry, type(None)):
        user_posts = Posts(
            user_id=user_id,
            group_id=group_id,
            tag=tag,
            amount=amount
        )
        db_sess.add(user_posts)
    else:
        db_sess.execute(update(Posts).values(amount=amount).where(
            Posts.user_id == user_id and Posts.tag == tag and Posts.group_id == group_id))
    db_sess.commit()

    # return redirect("/success")


if __name__ == "__main__":
    load_dotenv('.env')
    db_session.global_init()
    db_sess = db_session.create_session()
    app.run(host="0.0.0.0", port=3000, debug=True)
