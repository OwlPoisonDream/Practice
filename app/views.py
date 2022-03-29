#Обработчик ссылок
import email
from flask import Flask, render_template, request, redirect, url_for #для работы с интернетом
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user,current_user,logout_user
from app import app,models,db,forms
from app.email import send_password_reset_email

#print("[log] обработка страниц запущена")

@app.route('/createDb') #вход
def createDb():
    db.create_all() #создаем БД
    user = models.User(email="root",who = 2)
    user.set_password("root")
    db.session.add(user)
    db.session.commit()


@app.route('/',methods = ['POST', 'GET']) #вход
def index():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db.session.query(models.User).filter(models.User.email == form.email.data).first()
        print(user)
        if user and user.check_password(form.password.data):
          login_user(user, remember=form.remember.data)# запуск ссесии пользователя
          return redirect(url_for('cabinet'))
        return redirect(url_for('index'))  
    return render_template('index.html', form=form)

@app.route('/register',methods = ['POST', 'GET']) # регестрация 
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data,who = 0)
        user.set_password(form.password.data)
        db.session.add(user)
        userId = db.session.query(models.User).filter(models.User.email == form.email.data).first()
        userData = models.Users_Data(idUser = userId.id,  name = "none", 
            birthDAy = "none", passport = "none", passportData = "none", 
            passportBy = "none", passportCod = "none", nickname = "none", 
            link_vk = "none", inn = "none", bank_details = "none", bankName = "none", 
            phone_number = "none")
        db.session.add(userData)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')# выход из аккаунта 
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('index'))
    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = models.User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/cabinet',methods = ['POST', 'GET'])
@login_required #только зарегестрированный человек сможет зайти
def cabinet():
    return render_template('cabinet.html')

@app.route('/cabinet_changer',methods = ['POST', 'GET'])
@login_required #только зарегестрированный человек сможет зайти
def cabinet_changer():
    form = forms.PersonalForm()
    if form.validate_on_submit():
        user_data = db.session.query(models.Users_Data).filter_by(idUser = current_user.id).one() # выдает строку с id 2
        user_data.name = form.name.data
        user_data.birthDAy = form.birthDAy.data
        user_data.passport = form.passport.data 
        user_data.passportData = form.passportData.data 
        user_data.passportBy = form.passportBy.data 
        user_data.passportCod = form.passportCod.data
        user_data.nickname = form.nickname.data
        user_data.link_vk = form.link_vk.data
        user_data.inn = form.inn.data
        user_data.bank_details = form.bank_details.data
        user_data.bankName = form.bankName.data
        user_data.phone_number = form.phone_number.data

        db.session.add(user_data) 
        db.session.commit()
        return redirect(url_for('cabinet'))
    return render_template('cabinet_changer.html',form=form)

@app.route('/admin',methods = ['POST', 'GET'])
@login_required #только зарегестрированный человек сможет зайти
def admin():
    return render_template('admin.html')

# обработка ошибок
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500





