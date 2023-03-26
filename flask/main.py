from dotenv import load_dotenv
from flask import Flask, render_template, redirect

# from tg import bot
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.users import User
from forms.loginform import LoginForm
from forms.registerform import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mega_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/home')
def home():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с таким email уже существует")
        if db_sess.query(User).filter(User.name == form.username.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с таким логином уже существует")
        user = User(
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
        user = db_sess.query(User).filter(User.name == form.username.data).first()
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
    return render_template('success.html')


if __name__ == "__main__":
    load_dotenv('.env')
    db_session.global_init()
    db_sess = db_session.create_session()
    # bot.start_bot()
    app.run(host="0.0.0.0", port=3000)
