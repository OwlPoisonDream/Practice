#Обработчик ссылок
import email
from flask import Flask, render_template, request, redirect, url_for #для работы с интернетом
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user,current_user,logout_user
from app import app,models,db,forms

#print("[log] обработка страниц запущена")


@app.route('/',methods = ['POST', 'GET']) #вход
def index():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    form = forms.LoginForm()
    #if form.validate_on_submit():
    #    user = db.session.query(models.User).filter(models.User.email == form.email.data).first()
    #    print(user)
    #    if user and user.check_password(form.password.data):
    #      login_user(user, remember=form.remember.data)
    #      return redirect(url_for('cabinet'))
    #    return redirect(url_for('login'))  
    return render_template('index.html', form=form)

@app.route('/register',methods = ['POST', 'GET']) # регестрация 
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

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