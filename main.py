from flask import Flask, render_template, redirect
from data import db_session
from data.user import User
from data.news import News
from forms.user import RegisterForm
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)

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