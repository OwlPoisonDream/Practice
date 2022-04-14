# Обработчик ссылок
import email
from turtle import update
from flask import Flask, render_template, request, redirect, url_for  # для работы с интернетом
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from app import app, models, db, forms, create_contract
from app.email import send_password_reset_email
import yadisk
from docx import Document
import os
import datetime
from app import yToken


now = datetime.datetime.now()
# print("[log] обработка страниц запущена")

@app.route('/createDb')  # вход
def createDb():
    db.create_all()  # создаем БД
    user = models.User(email="root", who=2)
    user.set_password("root")
    db.session.add(user)
    db.session.commit()


@app.route('/', methods=['POST', 'GET'])  # вход
def index():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db.session.query(models.User).filter(models.User.email == form.email.data).first()
        print(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)  # запуск сессии пользователя
            return redirect(url_for('cabinet'))
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route('/register', methods=['POST', 'GET'])  # регистрация
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data, who=0)
        user.set_password(form.password.data)
        db.session.add(user)
        userId = db.session.query(models.User).filter(models.User.email == form.email.data).first()
        userData = models.Users_Data(idUser=userId.id, name="none",
                                     birthDAy="none", passport="none", passportData="none",
                                     passportBy="none", passportCod="none", nickname="none",
                                     link_vk="none", inn="none", bank_details="none", bankName="none",
                                     phone_number="none")
        db.session.add(userData)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout')  # выход из аккаунта
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/reset_password_request', methods=['GET', 'POST'])  # Страница просьбы о смене пароля
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


@app.route('/reset_password/<token>', methods=['GET', 'POST'])  # Страница сброса пароля и обработка его смены
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


@app.route('/cabinet', methods=['POST', 'GET'])  # Личный кабинет
@login_required  # только зарегистрированный человек сможет зайти
def cabinet():
    print("--------------------")
    print(current_user)
    print("--------------------")
    return render_template('cabinet.html', current_user=current_user)
    


@app.route('/cabinet_changer',
           methods=['POST', 'GET'])  # Страница для изменения данных в личном кабинете и вноса изменений в базу данных
@login_required  # только зарегистрированный человек сможет зайти
def cabinet_changer():
    form = forms.PersonalForm()
    if request.method == 'POST':
        user_data = db.session.query(models.Users_Data).filter_by(idUser=current_user.id).one()  # выдает строку с id 2
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
        user_data.tags = str(request.form.getlist('tags')) #Получение в виде строки списка с тегами
        db.session.add(user_data)
        db.session.commit()
        return redirect(url_for('cabinet'))
    return render_template('cabinet_changer.html', form=form)


@app.route('/my_tasks', methods=['GET', 'POST'])  # Страница с задачами пользователя
def my_tasks(): 
    info = models.Tasks.query.all()
    today = str(now.day) + "." + str(now.month) + "." + str(now.year)
    print(today)
    # print(list(yToken.listdir("")))
    if request.method == "POST":
        print(request.form.get("status_complete"))
        # task = models.Tass(id = id, statusCompleted = "Complete")
        # db.session.add(task)
        # db.session.commit()
    form = forms.CreateTask()
    if form.validate_on_submit(): # надо сделать завтра
        createTask = models.Tasks(idUser = form.idUser.data, idProject = form.idProject.data, 
        nameTask = form.nameTask.data,descTask = form.descTask.data,
        timeTask = form.timeTask.data,manyTask = form.manyTask.data, statusСompleted = "Uncomplete", linkDisk = form.descTask.data)
        db.session.add(createTask)
        db.session.commit()
    return render_template("my_tasks.html",form = form, list=info, today=today, now=now, current_user = current_user)


@app.route('/my_documents', methods=['GET', 'POST'])  # Страница с документами пользователя
def my_documents():
    list_yad = ()
    
    if yToken.check_token()==True:# проверка токена
        if yToken.exists("/договора/") == False: # проверка на отсутсвие папки, или создание папки
            print('Папка отсутствует')
            print(yToken.mkdir("/договора"))# создание папки и вывод папки в консоли
        elif yToken.exists("/договора/") == True:#если папка существует
            print('Папка существует')
            #print( yToken.check_token()) #получаем информацию о диске
            print (yToken.listdir("/договора"))#выводим содержимое папки дтговора



    yToken.clear_session_cache()
    info = models.User.query.all() #Получаем словарь с содержимым таблиц user и users_Data
    return render_template("my_documents.html", current_user=current_user, yToken=yToken, list_yad=list_yad)


@app.route('/my_projects', methods=['GET', 'POST'])  # Страница с проектами шоураннера
def my_projects():
    info = {}
    # отображение проектов
    projects = models.Project.query.all() #запрос в базу данны
    user_project = models.Users_Projects.query.all()
    info = models.User.query.all()
    list_yad = ()
    
    if yToken.check_token()==True:# проверка токена
        if yToken.exists("/Феникс проекты/") == False: # проверка на отсутствие папки, или создание папки
            print('Папка отсутствует')
            print(yToken.mkdir("/Феникс проекты"))# создание папки и вывод папки в консоли
        elif yToken.exists("/Феникс проекты/") == True:#если папка существует
            print('Папка существует')
            #print( yToken.check_token()) #получаем информацию о диске
            print (yToken.listdir("/Феникс проекты"))#выводим содержимое папки проектов
    if request.method == 'POST':
        id_sel = request.form.get('human_project') # Получаем ID пользователя из html
        id_project = request.form.get("project_id")# Получаем ID проекта из html
        id_project = str(id_project)
        project_name=request.form.get("projectName")
        update_user_projects = models.Users_Projects(User_id=id_sel, Project_id=id_project)# обновления таблицы Users_project
        if yToken.exists("/Феникс проекты/" + str(project_name)):
            print('Папка отсутствует')
            print(yToken.mkdir("/Феникс проекты" + str(project_name)))# создание папки и вывод папки в консоли
        elif yToken.exists("/Феникс проекты/"+ str(project_name)) == True:#если папка существует
            print('Папка существует')
            #print( yToken.check_token()) #получаем информацию о диске
            print (yToken.listdir("/Феникс проекты"+ str(project_name)))#выводим содержимое папки конкретного проекта
        listForm = request.form.to_dict()
        print(listForm)
        createProjekt = models.Project(projectName = listForm['projectName'],
        descProject=listForm['descProject'],linkDisk = listForm['linkDisk'])

        

        db.session.commit()# создание соеденения
        createProjekt = models.Project()# переменная создания пароля 
        db.session.add(update_user_projects)# запись в базу данных users_projekt
        db.session.add(createProjekt)# запись в базу данных users_projekt
        db.session.commit()# закрытие соеденения с бд
        return redirect(url_for('my_projects'))
    return render_template("my_projects.html", projects = projects, list = info, user_project = user_project)


@app.route('/salary', methods=['GET', 'POST'])  # Страница с зарплатами. Менеджер видит и устанавливает
def salary():
    return render_template("salary.html")


@app.route('/employeers', methods=['GET', 'POST'])  # Страница с сотрудниками компании. Доступна менеджеру
def employeers():
    info = models.User.query.all()

    return render_template("employeers.html", list = info)


@app.route('/completed_tasks/<who>/', methods=['GET', 'POST'])  # Страница с выполненными задачами по людям
def completed_tasks(who):
    user = models.User.query.filter_by(id = who).first()
    infoUser = models.Users_Data.query.filter_by(idUser = who).first()
    return render_template("completed_tasks.html",user = user,infoUser = infoUser)

@app.route('/cabinet_tasks_changer/<who>/', methods=['GET', 'POST'])  # Страница с выполненными задачами по людям
def completed_tasks_changer(who):
    form = forms.PersonalForm()
    
    user = models.User.query.filter_by(id = who).first()
    infoUser = models.Users_Data.query.filter_by(idUser = who).first()
    if form.validate_on_submit():
        print("я нажал на кнопку")
        user_data = db.session.query(models.Users_Data).filter_by(idUser=who).one()  # выдает строку с id 2
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
        user_data.tags = str(request.form.getlist('tags'))
        db.session.add(user_data)
        db.session.commit()
        return redirect(url_for('completed_tasks',who = who))
    return render_template("completed_tasks_changer.html",user = user,infoUser = infoUser,form=form)


@app.route('/create_contract', methods=['POST', 'GET'])
def contract():
    name = ''
    info = []
    tasks = models.Tasks.query.all()
    items = {"Работы:": {}, "Сроки:": {}, "Цена:": {}}
    id_sel = '0'
    id = 1
    info = models.User.query.all() #Получаем словарь с содержимым таблиц user и users_Data
    if request.method == 'POST':
        id_sel = request.form.get('human') # Получаем ID пользователя из html
        for i in tasks:
            if id_sel == models.Tasks.idUser:
                cells = str(models.Tasks.nameTask) + str(models.Tasks.timeTask) + str(models.Tasks.manyTask)
        id_sel = int(id_sel) - 1
        name = str(info[int(id_sel)].pr.name) # получаем имя из базы данных
        birth_date = str(info[int(id_sel)].pr.birthDAy)# Получаем дату рождения
        INN = str(info[int(id_sel)].pr.inn)#Получаем ИНН
        passport_num = str(info[int(id_sel)].pr.passport)# Получаем номер и серию паспорта
        passport_place = str(info[int(id_sel)].pr.passportBy)# Получаем место выдачи
        passport_date = str(info[int(id_sel)].pr.passportData)# Получаем дату выдачи
        passport_code = str(info[int(id_sel)].pr.passportCod)# Получаем код подразделения
        address = str(info[int(id_sel)].pr.address)# Получаем адрес
        bank_account = str(info[int(id_sel)].pr.bankAccount)# Получаем банковский счёт
        bank_name = str(info[int(id_sel)].pr.bankName)# Получаем наименование банка
        bank_details = str(info[int(id_sel)].pr.bank_details)# Получаем реквизиты банка
        email = str(info[int(id_sel)].email)# Получаем электронную почту
        create_contract.create_contract(name, birth_date, INN, passport_num, passport_place, passport_date, passport_code, address, bank_account, bank_name, bank_details, email)
        return redirect(url_for('cabinet'))
    return render_template('create_contract.html', name=name, id=id_sel, list=info)


@app.route('/admin', methods=['POST', 'GET'])  # Страница, доступная ЛИШЬ админу
@login_required  # только зарегистрированный человек сможет зайти
def admin():
    info = []
    info = models.User.query.all()
    tasks = models.Tasks.query.all()
    projects = models.Project.query.all()
    return render_template('admin.html', list=info, tasks=tasks, projects=projects)


# обработка ошибок
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
    # Обработчик ссылок


