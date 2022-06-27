from flask import Flask, render_template, redirect, request, abort, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import csv
from forms.news import NewsForm
from forms.user import *
from googlemail import mail
from data.news import News
from data.users import User
from data import db_session
import random
import os

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/blogs.db?check_same_thread=False'

app.config['SECRET_KEY'] = 'b0-sdb-0sbdfb0-bgf0sb-db0vf'
db_session.global_init("db/blogs.db")


# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("Портал Сбора Медицинских Данных.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    return render_template("Page 3.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('Page 2.html')


#
# @app.route('/createord/<id_user>/<doc>', methods=['GET', 'POST'])
# def createord(id_user, doc):
#     form = CreateOrd()
#     if form.validate_on_submit():
#         with open(f'static/doc/{doc}', 'a', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow([form.name.data, form.count.data, form.art.data, form.price.data])
#         return redirect(f"/ord/{id_user}/{doc}")
#     # print(234523535354)
#     # flash('Тест_LALALALALALALALALALALALALALALALALALALALALALALAL34')
#     return render_template('ФормированиеЗаказа.html', title='Авторизация', form=form, add=f"/warehouse/{id_user}",
#                            create=f"/create/{id_user}",
#                            myorder=f"/myorders/{id_user}",
#                            items=f"/transport/{id_user}",
#                            face=f"/face/{id_user}")
#
#
# @app.route('/del_file/<id_user>/<doc>', methods=['GET', 'POST'])
# def delit(id_user, doc):
#     db_sess = db_session.create_session()
#     email = str(db_sess.query(User).filter(User.id_user == id_user).first()).split()[-1]
#     mail(doc + " был закрыт.", email)
#
#     #  user = db_sess.query(User).filter(User.id_user == id_user).first()
#     #  print(user)
#     os.remove(f'static/doc/{doc}')
#     return redirect(f"/myorders/{id_user}")
#
#
# @app.route('/ord/<id_user>/<doc>/<role>', methods=['GET', 'POST'])
# def look(id_user, doc, role=None):
#     v = 'Заказ - ' + doc.replace('_', '').replace('done', '').replace('delivered', '').replace('got', '').replace(id_user,
#                                                                                                      '').replace('.csv',
#                                                                                                                  '')
#     form = Ord()
#     with open(f'static/doc/{doc}', "r", encoding='utf-8') as file1:
#         # list_ord = ['   '.join(line.strip().split(',')) for line in file1]
#         head = file1.readlines()[1:]
#         list_ord = [line.strip().split(',') for line in head]
#     return render_template('Просмотр.html', title='Авторизация', form=form, user=id_user, add=f"/warehouse/{id_user}",
#                            create=f"/create/{id_user}",
#                            myorder=f"/myorders/{id_user}",
#                            items=f"/transport/{id_user}", list_ord=list_ord,
#                            createord=f"/createord/{id_user}/{doc}",
#                            delite=f"/del_file/{id_user}/{doc}",
#                            face=f"/face/{id_user}", doc=v)
#
#
# @app.route('/ord/<id_user>/<doc>', methods=['GET', 'POST'])
# def myorder(id_user, doc, role=None):
#     v = 'Заказ - ' + doc.replace('_', '').replace('done', '').replace('delivered', '').replace('got', '').replace(id_user,
#                                                                                                      '').replace('.csv',
#                                                                                                                  '')
#     form = Ord()
#     with open(f'static/doc/{doc}', "r", encoding='utf-8') as file1:
#         head = file1.readlines()[1:]
#         list_ord = [line.strip().split(',') for line in head]
#         # list_ord = [line.strip().split(',') for line in file1]
#
#     if 'done' not in doc and role is None:
#         return render_template('Заказ.html', title='Авторизация', form=form, user=id_user, add=f"/warehouse/{id_user}",
#                                create=f"/create/{id_user}",
#                                myorder=f"/myorders/{id_user}",
#                                items=f"/transport/{id_user}", list_ord=list_ord,
#                                createord=f"/createord/{id_user}/{doc}",
#                                delite=f"/del_file/{id_user}/{doc}",
#                                face=f"/face/{id_user}", doc=v)
#
#     elif role is None:
#         return render_template('Собрано.html', title='Авторизация', user=id_user, add=f"/warehouse/{id_user}",
#                                create=f"/create/{id_user}",
#                                myorder=f"/myorders/{id_user}",
#                                items=f"/transport/{id_user}",
#                                delite=f"/del_file/{id_user}/{doc}",
#                                face=f"/face/{id_user}", list_ord=list_ord, doc=v)
#
#
# @app.route('/myorders/<id_user>', methods=['GET', 'POST'])
# def myorders(id_user):
#     form = Ord()
#     list_ord, ss = view(id_user, 'any')
#     return render_template('МоиЗаказы.html', title='Авторизация', form=form, add=f"/warehouse/{id_user}",
#                            create=f"/create/{id_user}",
#                            createord=f"/ord/{id_user}/",
#                            myorder=f"/myorders/{id_user}",
#                            items=f"/transport/{id_user}",
#                            face=f"/face/{id_user}", list_ord=list_ord, a=dict(pairs=zip(list_ord, ss)))
#
#
# @app.route('/warehouse/<id_user>', methods=['GET', 'POST'])
# def warehouse(id_user):
#     form = Ord()
#     list_ord, ss = view(id_user, 1)
#     return render_template('Склад.html', title='Авторизация', form=form, add=f"/warehouse/{id_user}",
#                            create=f"/create/{id_user}",
#                            myorder=f"/myorders/{id_user}",
#                            items=f"/transport/{id_user}",
#                            delite=f"/carrier/{id_user}/",
#                            ord=f"/ord/{id_user}/",
#                            face=f"/face/{id_user}", list_ord=list_ord, a=dict(pairs=zip(list_ord, ss)))
#
#
# @app.route('/face/<id_user>', methods=['GET', 'POST'])
# def face(id_user):
#     form = Ord()
#     list_ord, ss = view(id_user, 3)
#     return render_template('Лицо.html', title='Авторизация', form=form, add=f"/warehouse/{id_user}",
#                            create=f"/create/{id_user}",
#                            myorder=f"/myorders/{id_user}",
#                            items=f"/transport/{id_user}",
#                            delite=f"/carrier/{id_user}/",
#                            ord=f"/ord/{id_user}/",
#                            face=f"/face/{id_user}",
#                            fd=f"/last/{id_user}/",
#                            ls=f"/last/{id_user}/", list_ord=list_ord, a=dict(pairs=zip(list_ord, ss)))
#
#
# @app.route('/transport/<id_user>', methods=['GET', 'POST'])
# def transport(id_user):
#     form = Ord()
#     list_ord, ss = view(id_user, 2)
#     return render_template('Экспидитор.html', title='Авторизация', form=form, add=f"/warehouse/{id_user}",
#                            create=f"/create/{id_user}",
#                            myorder=f"/myorders/{id_user}",
#                            items=f"/transport/{id_user}",
#                            dd=f"/delivered/{id_user}/",
#                            ord=f"/ord/{id_user}/",
#                            face=f"/face/{id_user}", list_ord=list_ord, a=dict(pairs=zip(list_ord, ss)))
#
#
# @app.route('/delivered/<id_user>/<doc>', methods=['GET', 'POST'])
# def delivered(id_user, doc):
#     db_sess = db_session.create_session()
#     email = str(db_sess.query(User).filter(User.id_user == id_user).first()).split()[-1]
#     mail(doc + " был доставлен.", email)
#
#     id_user_r = str(doc.split('.')[:-1][0])
#     os.rename('static/doc/' + doc, f'static/doc/{id_user_r}_delivered.csv')
#     return redirect('/transport/' + id_user)
#
#
# @app.route('/carrier/<id_user>/<doc>', methods=['GET', 'POST'])
# def carrier(id_user, doc):
#     db_sess = db_session.create_session()
#     email = str(db_sess.query(User).filter(User.id_user == id_user).first()).split()[-1]
#     mail(doc + " был собран и теперь ожидает доставки", email)
#
#     id_user_r = str(doc.split('.')[:-1][0])
#     os.rename('static/doc/' + doc, f'static/doc/{id_user_r}_done.csv')
#     return redirect('/warehouse/' + id_user)
#
#
# @app.route('/last/<id_user>/<doc>', methods=['GET', 'POST'])
# def last(id_user, doc):
#     db_sess = db_session.create_session()
#     email = str(db_sess.query(User).filter(User.id_user == id_user).first()).split()[-1]
#     mail(doc + " был получен.", email)
#
#     id_user_r = str(doc.split('.')[:-1][0])
#     os.rename('static/doc/' + doc, f'static/doc/{id_user_r}_got.csv')
#     return redirect('/face/' + id_user)
#
#
# @app.route('/create/<id_user>', methods=['GET', 'POST'])
# def create(id_user):
#     form = Add()
#     if form.validate_on_submit():
#         with open(f'static/doc/{id_user}_{form.name.data}.csv', 'w', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(['Наименование товара', 'Количество', 'Артикул', 'Цена'])
#
#         return redirect(f'/myorders/{id_user}')  # redirect(f"/create/{form.name.data}")
#     return render_template('СозданиеЗаказа.html', title='Авторизация', form=form, add=f"/warehouse/{id_user}",
#                            create=f"/create/{id_user}",
#                            myorder=f"/myorders/{id_user}",
#                            items=f"/transport/{id_user}",
#                            face=f"/face/{id_user}")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
