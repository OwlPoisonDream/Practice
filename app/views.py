#Обработчик ссылок
import email
from flask import Flask, render_template, request, redirect, url_for #для работы с интернетом
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user,current_user,logout_user
from app import app
from app import models,db

#print("[log] обработка страниц запущена")



@app.route('/',methods = ['POST', 'GET'])
def index():
    message = ''
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')
        q = models.User.query.filter_by(email = email).first()

        if email == q.email and check_password_hash(password,q.password_hash):
            message = "Вы вошли"
            login_user(q)
            return redirect(url_for('cabinet'))
        else:
            message = "Неправельно ввели логин или пароль"
    return render_template('index.html',message = message)

@app.route('/register',methods = ['POST', 'GET']) # регестрация 
def register():
    message = ''
    if request.method == 'POST':
        print(request.form)# смотрим, что вводит пользователь 

        email = request.form.get('email') # почта в переменной
        password = generate_password_hash(request.form.get('password')) #хеш пароля в переменной

        q = models.User.query.filter_by(email = email).first() #запрос в БД на поиск пользователя

        if q is None: # если запрос в БД == 0
            message = "Вы зарегестрировались"
            addUser(email,password)
            q = models.User.query.get(email.data).first()
            print(q)
            login_user(email) #создание ссесии пользователя по email
            return redirect(url_for('cabinet'))
        else:
            message = "Пользователь занят"
        
    return render_template('register.html',message = message)

@app.route('/logout')# выход из аккаунта 
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cabinet',methods = ['POST', 'GET'])
@login_required #только зарегестрированный человек сможет зайти
def cabinet():
    return render_template('cabinet.html', email = email)

@app.route('/cabinet_changer',methods = ['POST', 'GET'])
@login_required #только зарегестрированный человек сможет зайти
def cabinet_changer():
    return render_template('cabinet_changer.html')

@app.route('/admin',methods = ['POST', 'GET'])
@login_required #только зарегестрированный человек сможет зайти
def admin():
    return render_template('admin.html')



# функция для добовление пользователя, сейчас она сдесь 
def addUser(email = "none", password_hash = "none", name = "none", nickname = "none", link_vk = "none" , inn = "none", bank_details = "none", bankName = "none", phone_number = "none"):
    news = models.User(email = email, password_hash = password_hash, 
    name = name, nickname = nickname, link_vk = link_vk , 
    inn = inn, bank_details = bank_details, bankName = bankName, 
    phone_number = phone_number)
    db.session.add(news)# добавить новые записи в базу данных
    db.session.commit()# закрываем базу данных