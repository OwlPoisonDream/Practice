# Обработчик ссылок
import email
from turtle import update
from flask import Flask, render_template, request, redirect, url_for  # для работы с интернетом
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from app import app, models, db, forms
from app.email import send_password_reset_email
from docx import Document

document = Document()
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
    if form.validate_on_submit():
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

        db.session.add(user_data)
        db.session.commit()
        return redirect(url_for('cabinet'))
    return render_template('cabinet_changer.html', form=form)


@app.route('/my_tasks', methods=['GET', 'POST'])  # Страница с задачами пользователя
def my_tasks():
    form = forms.CreateTask()
    if form.validate_on_submit(): # надо сделать завтра
        createProjekt = models.Project(projectName = form.projectName.data, 
        descProject = form.descProject.data,linkDisk = form.linkDisk.data)
        db.session.add(createProjekt)
        db.session.commit()
    return render_template("my_tasks.html",form = form)


@app.route('/my_documents', methods=['GET', 'POST'])  # Страница с документами пользователя
def my_documents():
    return render_template("my_documents.html")


@app.route('/my_projects', methods=['GET', 'POST'])  # Страница с проектами шоураннера
def my_projects():
    info = {}
    # отображение проектов
    projects = models.Project.query.all()
    user_project = models.Users_Projects.query.all()
    info = models.User.query.all()
    form = forms.CreateProject()
    if request.method == 'POST':
        id_sel = request.form.get('human_project') # Получаем ID пользователя из html
        id_project = request.form.get("project_id")
        id_project = int(id_project)
        update_user_projects = models.Users_Projects(User_id=id_sel, Project_id=id_project)
        print("---------------------------------------------------------------")
        print(update_user_projects)
        print("---------------------------------------------------------------")
        db.session.add(update_user_projects)
        db.session.commit()
        return redirect(url_for('my_projects'))
    
    if form.validate_on_submit():
        print("Кнопка нажата")
        createProjekt = models.Project(projectName = form.projectName.data, 
        descProject = form.descProject.data,linkDisk = form.linkDisk.data)
        db.session.add(createProjekt)
        db.session.commit()
        return redirect(url_for('my_projects'))
    return render_template("my_projects.html",form = form, projects = projects, list = info, user_project = user_project)


@app.route('/salary', methods=['GET', 'POST'])  # Страница с зарплатами. Менеджер видит и устанавливает
def salary():
    return render_template("salary.html")


@app.route('/employeers', methods=['GET', 'POST'])  # Страница с сотрудниками компании. Доступна менеджеру
def employeers():
    return render_template("employeers.html")


@app.route('/completed_tasks', methods=['GET', 'POST'])  # Страница с выполненными задачами по людям
def completed_tasks():
    return render_template("completed_tasks.html")


@app.route('/create_contract', methods=['POST', 'GET'])
def contract():
    name = ''
    info = []
    id_sel = '0'
    id = 1
    info = models.User.query.all() #Получаем словарь с содержимым таблиц user и users_Data
    if request.method == 'POST':
        id_sel = request.form.get('human') # Получаем ID пользователя из html
        table = document.add_table(rows=1, cols=2) #Создаём таблицу
        hdr_cells = table.rows[0].cells #Устанавливем строку, которую планируем заполнять
        name = str(info[id_sel].pr.name) # получаем имя из базы данных
        birth_date = str(info[id_sel].pr.birthDAy)# Получаем дату рождения
        INN = str(info[id_sel].pr.inn)#Получаем ИНН
        passport_num = str(info[id_sel].pr.passport)# Получаем номер и серию паспорта
        passport_place = str(info[id_sel].pr.passportBy)# Получаем место выдачи
        passport_date = str(info[id_sel].pr.passportData)# Получаем дату выдачи
        passport_code = str(info[id_sel].pr.passportCod)# Получаем код подразделения
        address = str(info[id_sel].pr.address)# Получаем адрес
        bank_account = str(info[id_sel].pr.bankAccount)# Получаем банковский счёт
        bank_name = str(info[id_sel].pr.bankName)# Получаем наименование банка
        bank_details = str(info[id_sel].pr.bank_details)# Получаем реквизиты банка
        email = str(info[id_sel].email)# Получаем электронную почту
        hdr_cells[0].text = "Подрядчик" + "\n" + name + "\n" + birth_date + "\n" + INN + "\n" + passport_num + "\n" + passport_place + "\n" + passport_date + "\n" + passport_code + "\n" + address + "\n" + \
                            bank_account + "\n" + bank_name + "\n" + bank_details + "\n" + email # Заполняем первую ячейку
        hdr_cells[1].text = "Заказчик:" + "\n" + "Индивидуальный предприниматель" + "\n" + "Нечитайло Фёдор Константинович" + "\n" \
            + "ИНН 616616300580 ОГРН 318619600017594" + "\n" + "Адрес: 344065, Ростовская обл., г. Ростов-на-Дону, ул. Вятская, д. 63/1, кв. 77" \
                      + "\n" + "р/с 40802810000000405802 в АО «Тинькофф Банк»" + "\n" + "кор/сч 30101810145250000974" \
                      + "\n" + "БИК 044525974" + "\n" + "fedorcomixvideo@gmail.com" # Заполняем вторую ячейку
        document.save('contract.docx') #Сохраняем документ
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