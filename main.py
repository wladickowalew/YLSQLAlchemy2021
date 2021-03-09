from flask import Flask, render_template, redirect, \
                  request, make_response, session
from data import db_session
from data.user import User
from data.news import News
from forms.user import RegisterForm
from forms.login import LoginForm
from flask_login import LoginManager, login_user
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res

@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")

@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

def add_users():
    for i in range(17):
        user = User()
        user.name = "Пользователь " + str(i)
        user.about = "биография пользователя " + str(i)
        user.email = "email@email" + str(i) + ".ru"
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()

def main():
    db_session.global_init("db/blogs.db")
    app.run()
    # for user in db_sess.query(User).filter((User.id > 4) | (User.email.notilike("%1%"))):
    #     print(user)

    #user = db_sess.query(User).filter(User.id == 1).first()
    #print(user)
    # user.name = "Никифор"
    # user.created_date = datetime.datetime.now()
    # db_sess.commit()

    #add_users()

    # db_sess.query(User).filter(3 <= User.id, User.id <= 7).delete()
    # db_sess.commit()
    # for user in db_sess.query(User).all():
    #     print(user)

    # news = News(title="Первая новость", content="Привет блог!", 
    #         user_id=1, is_private=False)
    # db_sess.add(news)
    # db_sess.commit()

    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Вторая новость", content="Уже вторая запись!", 
    #             user=user, is_private=False)
    # db_sess.add(news)
    # db_sess.commit()

    # user = db_sess.query(User).filter(User.id == 8).first()
    # news = News(title="Личная запись", content="Эта запись личная", 
    #             is_private=True)
    # user.news.append(news)
    # db_sess.commit()

if __name__ == '__main__':
    main()