# Обработчик ссылок
from calendar import month
import email
from flask import  render_template, flash, request, redirect, url_for  # для работы с интернетом
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
from app import app, models, db, forms
from app.email import send_password_reset_email
import yadisk
from docxtpl import DocxTemplate # вставка данных в word 
from docx import Document # вставка таблицы в word 
import os
from datetime import datetime, timedelta,date
from app import yToken
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
now = datetime.now()
# print("[log] обработка страниц запущена")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
@app.route('/createDb')  # вход
@login_required  # только зарегистрированный человек сможет зайти
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
    


@app.route('/cabinet_changer',methods=['POST', 'GET'])  # Страница для изменения данных в личном кабинете и вноса изменений в базу данных
@login_required  # только зарегистрированный человек сможет зайти
def cabinet_changer():
    form = forms.PersonalForm()
    if request.method == 'POST':
        user_data = db.session.query(models.Users_Data).filter_by(idUser=current_user.id).one()  # выдает строку с id
        if form.name.data and form.name.data.strip() and form.name.data != None :
            user_data.name = form.name.data

        if form.birthDAy.data and form.birthDAy.data.strip() and form.birthDAy.data != None :
            user_data.birthDAy = form.birthDAy.data

        if form.passport.data and form.passport.data.strip() and form.passport.data != None :
         user_data.passport = form.passport.data

        if form.passportData.data and form.passportData.data.strip() and form.passportData.data != None :
            user_data.passportData = form.passportData.data

        if form.passportBy.data and form.passportBy.strip() and form.passportBy.data != None :
            user_data.passportBy = form.passportBy.data

        if form.passportCod.data and form.passportCod.strip() and form.passportCod.data != None and len(form.passportCod.data)==6:
            user_data.passportCod = form.passportCod.data

        if form.nickname.data and form.nickname.strip() and form.nickname.data != None :
            user_data.nickname = form.nickname.data
            
        if form.link_vk.data and form.link_vk.strip() and form.link_vk.data != None :
            user_data.link_vk = form.link_vk.data

        if form.inn.data and form.inn.strip() and form.inn.data != None and len(form.inn.data)==12:
            user_data.inn = form.inn.data

        if form.bank_details.data and form.bank_details.strip() and form.bank_details.data != None :
            user_data.bank_details = form.bank_details.data

        if form.bankName.data and form.bankName.strip() and form.bankName.data != None :
            user_data.bankName = form.bankName.data

        if form.phone_number.data and form.phone_number.strip() and form.phone_number.data != None and len(form.phone_number.data)<=18:
            user_data.phone_number = form.phone_number.data

        if str(request.form.getlist('tags')) != "[]":
            user_data.tags = str(request.form.getlist('tags'))
        print(user_data)

        if form.photo.data != None :
            # загрузка фото
            f = form.photo.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(
            "app", 'static/photos', filename
            ))
            if yToken.exists("/Фотки для профиля/" + str(current_user.pr.name)) == False:
                yToken.mkdir("/Фотки для профиля/"+ str(current_user.pr.name)) # создание папки
                try:
                    yToken.upload("app/static/photos/" + filename , "/Фотки для профиля/"+ str(current_user.pr.name) + "/" + filename)
                    
                    if os.path.isfile("app/static/photos/"+ filename): 
                        os.remove("app/static/photos/"+ filename) 
                        print("удалил") 
                    else: 
                        print("файла и небыло")

                except yadisk.exceptions.PathExistsError:
                    return render_template('cabinet_changer.html', error="Проблема с яндекс диском")
            elif yToken.exists("/Фотки для профиля/" + str(current_user.pr.name)) == True: #если папка существует
                try:
                    yToken.upload("app/static/photos/" + filename , "/Фотки для профиля/"+ str(current_user.pr.name) + "/" + filename)
                    
                    if os.path.isfile("app/static/photos/"+ filename): 
                        os.remove("app/static/photos/"+ filename) 
                        print("удалил") 
                    else: 
                        print("файла и небыло")

                except yadisk.exceptions.PathExistsError:
                    return render_template('cabinet_changer.html', error="Проблема с яндекс диском")

            user_data.avatar = form.photo.data.filename

        db.session.add(user_data)
        db.session.commit()
        
        return redirect(url_for('cabinet'))
    error = "ошибка"
    return render_template('cabinet_changer.html', form=form, error = error)


@app.route('/my_tasks', methods=['GET', 'POST'])  # Страница с задачами пользователя
@login_required  # только зарегистрированный человек сможет зайти
def my_tasks(): 
    tasks = models.Tasks.query.all()# таблица задачь
    today = str(now.day) #Сегодняшний день
    if now.month <10: #Проверка на месяц
        today = today + ".0" + str(now.month) + "." + str(now.year) #Облегчаем проверку
    form = forms.CreateTask()# форма создания задачь
    print(today) #Вывожу время
    # print(list(yToken.listdir("")))
    if request.method == "POST":
        if request.form.get("link")==None or request.form.get("link") == "":
            print(request.form.get("task_into"))
            task_id=request.form.get("task_into")
            print(task_id)
            task = db.session.query(models.Tasks).filter_by(id = task_id).first()
            print(task)
            if task.idProject == models.Project.id:
                user = models.Users_Data.query.filter_by(id = id).first()#поиск юзера
                nameFail = user.name + " " + now.today().strftime("%d.%m.%Y")#имя файла
                print("привет я начал работать с яндекс диском")
                if yToken.exists("/Феникс проекты/" + str(project_name)) == False:
                    yToken.mkdir("/Феникс проекты/"+ str(project_name))# создание папки
                if 'files' not in request.files: #Проверяем на добавление файлов
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['files'] #Получаем имена файлов
                if file.filename == '': #Если файл не был прикреплён
                    flash('No selected file')
                    return render_template("my_tasks.html",form = form, tasks=tasks, today=today, now=now, current_user = current_user)
                if file and allowed_file(file.filename): #Если файл был прикреплён и обладает нужным расширением
                    nameFail = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], nameFail))
                    return render_template("my_tasks.html",form = form, tasks=tasks, today=today, now=now, current_user = current_user)
                project_name = models.Project.projectName
                if yToken.exists("/Феникс проекты/"+ str(project_name)) == True:#если папка существует
                    print('Папка существует')
                    yToken.upload(os.path.join(app.config['UPLOAD_FOLDER'], nameFail), "/Феникс проекты/"+ str(project_name)+ "/" + nameFail)
                    task.statusСompleted = "Complete"
                    db.session.add(task)
                    db.session.commit()
        elif request.form.get("link")!=None or request.form.get("link") !="":
            print(request.form.get("task_our"))
            task_id=request.form.get("task_our")
            task = db.session.query(models.Tasks).filter_by(id = task_id).one()
            task.statusСompleted = "Complete"
            task.linkDisk = request.form.get("link")
            db.session.add(task)
            db.session.commit()
        return render_template("my_tasks.html",form = form, tasks=tasks, today=today, now=now, current_user = current_user)
    
    return render_template("my_tasks.html",form = form, tasks=tasks, today=today, now=now, current_user = current_user)


@app.route('/my_documents', methods=['GET', 'POST'])  # Страница с документами пользователя
@login_required  # только зарегистрированный человек сможет зайти
def my_documents():
    user = models.Users_Data.query.filter_by(id = current_user.id ).first()#поиск юзера
    List = {}
    if request.method == 'POST':
        listForm = request.form.to_dict()
        listFormKeys = listForm.keys()# выводим все ключи выбранных блоках
        # вставка данных
        for id in listFormKeys:
            user = models.Users_Data.query.filter_by(id = id).first()#поиск юзера
            nameFail = user.name + " " + now.today().strftime("%d.%m.%Y")#имя файла
            print("привет я начал работать с яндекс диском")
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return render_template('my_documents.html',list=user, error = "Чек не прикреплён")
            if file and allowed_file(file.filename):
                nameFail = secure_filename(file.filename)
                file.save("app/static/checkTemplates/" + nameFail + ".pdf")
                return render_template('my_documents.html',list=user, error = "Чек загружен на сервер")
            if yToken.exists("/чеки/" + str(user.name)) == False:
                yToken.mkdir("/чеки/"+ str(user.name))# создание папки
                try:
                    yToken.upload("app/static/checkTemplates/"+ nameFail +".pdf", "/чеки/"+ str(user.name)+"/" + nameFail +".pdf")
                except yadisk.exceptions.PathExistsError:
                    return render_template('my_documents.html',list=user, error="У " + user.name + " Чек уже прикреплён")
            elif yToken.exists("/чеки/"+ str(user.name)) == True:#если папка существует
                try:
                    yToken.upload("app/static/checkTemplates/"+ nameFail +".pdf", "/чеки/"+ str(user.name)+"/" + nameFail +".pdf")
                except yadisk.exceptions.PathExistsError:
                    return render_template('my_documents.html',list=user, error="У " + user.name + " Чек уже прикреплён")
            
        return render_template('my_documents.html',list=user, error = "Чек прикреплён и внесен на яндекс диск")
    try:
        docList = list(yToken.listdir("/договора/" + user.name))
        a = 0
        for i in docList:
            d = {docList[a].name : docList[a].file}
            List.update(d)
            a = a + 1  
    except yadisk.exceptions.PathNotFoundError:
        return render_template("my_documents.html",list = List,error = "Чеков нету")
    return render_template("my_documents.html", list = List)



@app.route('/my_projects', methods=['GET', 'POST'])  # Страница с проектами шоураннера
@login_required  # только зарегистрированный человек сможет зайти
def my_projects():
    info = {}
    error = ""
    # отображение проектов
    projects = models.Project.query.all() #запрос в базу данны для вывода проектов
    user_project = models.Users_Projects.query.all()#запрос в базу данны для вывода какой человек к каому проекту
    info = models.User.query.all() #запрос в базу данны для вывода людей
    tasks = models.Tasks.query.all()# таблица задачь
    folders = models.Folder.query.all()# таблица папок
    
    if request.method == 'POST': # обработка post

        listForm = request.form.to_dict()# получение информации из формы
        print(listForm)

        # создание проекта
        if ( listForm.get('projectName')):
            if (models.Project.query.filter_by(projectName = listForm['projectName']).first()):
                error = "имя уже занято, проект не создался"
                return render_template("my_projects.html", projects = projects, list = info, 
                    user_project = user_project, folders = folders,tasks = tasks, error = error)

            if yToken.exists("/Феникс проекты/" + str(listForm["projectName"])):
                print('Папка отсутствует')
                yToken.mkdir("/Феникс проекты/" + str(listForm["projectName"])) # создание папки и вывод папки в консоли

            elif yToken.exists("/Феникс проекты/"+ str(listForm["projectName"])) == True: #если папка существует
                print('Папка существует')
                #print( yToken.check_token()) #получаем информацию о диске
                print (yToken.listdir("/Феникс проекты/"+ str(listForm["projectName"])))#выводим содержимое папки

            createProjekt = models.Project(projectName = listForm['projectName'],# создание проекта
            descProject = listForm['descProject'], linkDisk = "/Феникс проекты/"+ str(listForm["projectName"]))

            db.session.commit()# создание соеденения
            db.session.add(createProjekt)# запись в базу данных users_projekt
            id_project = models.Project.query.filter_by(projectName = listForm['projectName']).first()
            print(id_project.id)
            for k, v in listForm.items():
                if v == 'id_sel':
                    update_user_projects = models.Users_Projects(User_id = k, Project_id = id_project.id)# обновления таблицы Users_project
                    db.session.add(update_user_projects)# запись в базу данных users_projekt
            db.session.commit()# закрытие соеденения с бд
            return redirect(url_for('my_projects'))
            
        # для создании папки
        if (listForm.get('folderName')):
            print("в меня вошли")
            createFolder = models.Folder(name = listForm['folderName'],id_progect = listForm['id'])
            db.session.commit()# создание соеденения
            db.session.add(createFolder)# запись в базу данных users_projekt
            db.session.commit()# закрытие соеденения с бд
            return redirect(url_for('my_projects'))
        
        if form.validate_on_submit(): # надо сделать завтра
        if len(form.timeTask.data)==2:
            createTask = models.Tasks(idUser = form.idUser.data, idProject = form.idProject.data, 
            nameTask = form.nameTask.data,descTask = form.descTask.data,
            timeTask = form.timeTask.data,manyTask = form.manyTask.data, statusСompleted = "Uncomplete", linkDisk = form.descTask.data)
        else:
            print("Введите числовое значение месяца")
        db.session.add(createTask)
        db.session.commit()
    return render_template("my_projects.html", projects = projects, list = info, 
                    user_project = user_project, folders = folders,tasks = tasks, error = error)


@app.route('/salary', methods=['GET', 'POST'])  # Страница с зарплатами. Менеджер видит и устанавливает
@login_required  # только зарегистрированный человек сможет зайти
def salary():
    task = models.Tasks.query.filter_by(idUser = current_user.id).all()# поиск отмеченных пользователя
    total = 0
    for u in task:
        u.timeTask = datetime.strptime(u.timeTask,'%d.%m.%Y').date()
        total = task.manyTask + total
    a = date.today()# время сейчас
    b = date.today() - timedelta(days=7)#время неделю назад
    c = date.today() - timedelta(weeks = 4)#время месяц назад
    d = date.today() - timedelta(weeks = 48)#время год назад
    return render_template("salary.html", task = task, a = a, b = b, c = c, d = d, total = total)


@app.route('/employeers', methods=['GET', 'POST'])  # Страница с сотрудниками компании. Доступна менеджеру
@login_required  # только зарегистрированный человек сможет зайти
def employeers():
    info = models.User.query.all()
    return render_template("employeers.html", list = info)


@app.route('/completed_tasks/<who>/', methods=['GET', 'POST'])  # Страница с выполненными задачами по людям
@login_required  # только зарегистрированный человек сможет зайти
def completed_tasks(who):
    user = models.User.query.filter_by(id = who).first()
    infoUser = models.Users_Data.query.filter_by(idUser = who).first()
    try:
        docList = list(yToken.listdir("/договора/" + infoUser.name))
        List = {}
        a = 0
        for i in docList:
            d = {docList[a].name : docList[a].file}
            List.update(d)
            a = a + 1  
    except yadisk.exceptions.PathNotFoundError:
        return render_template("completed_tasks.html",user = user,infoUser = infoUser,error = "Договоров нету")

    return render_template("completed_tasks.html",user = user,infoUser = infoUser, list = List)

@app.route('/cabinet_tasks_changer/<who>/', methods=['GET', 'POST'])  # Страница с выполненными задачами по людям
@login_required  # только зарегистрированный человек сможет зайти
def completed_tasks_changer(who):
    form = forms.PersonalForm()
    
    user = models.User.query.filter_by(id = who).first()
    infoUser = models.Users_Data.query.filter_by(idUser = who).first()
    if form.validate_on_submit():
        print("я нажал на кнопку")
        user_data = db.session.query(models.Users_Data).filter_by(idUser=who).one()  # выдает строку с id 2
        if form.name.data and form.name.data.strip() and form.name.data != None :
            user_data.name = form.name.data

        if form.birthDAy.data and form.birthDAy.data.strip() and form.birthDAy.data != None :
            user_data.birthDAy = form.birthDAy.data

        if form.passport.data and form.passport.data.strip() and form.passport.data != None :
         user_data.passport = form.passport.data

        if form.passportData.data and form.passportData.data.strip() and form.passportData.data != None :
            user_data.passportData = form.passportData.data

        if form.passportBy.data and form.passportBy.strip() and form.passportBy.data != None :
            user_data.passportBy = form.passportBy.data

        if form.passportCod.data and form.passportCod.strip() and form.passportCod.data != None and len(form.passportCod.data)==6:
            user_data.passportCod = form.passportCod.data

        if form.nickname.data and form.nickname.strip() and form.nickname.data != None :
            user_data.nickname = form.nickname.data
            
        if form.link_vk.data and form.link_vk.strip() and form.link_vk.data != None :
            user_data.link_vk = form.link_vk.data

        if form.inn.data and form.inn.strip() and form.inn.data != None and len(form.inn.data)==12:
            user_data.inn = form.inn.data

        if form.bank_details.data and form.bank_details.strip() and form.bank_details.data != None :
            user_data.bank_details = form.bank_details.data

        if form.bankName.data and form.bankName.strip() and form.bankName.data != None :
            user_data.bankName = form.bankName.data

        if form.phone_number.data and form.phone_number.strip() and form.phone_number.data != None and len(form.phone_number.data)<=18:
            user_data.phone_number = form.phone_number.data
        if str(request.form.getlist('tags')) != "[]":
            user_data.tags = str(request.form.getlist('tags'))
        print(user_data)
        db.session.add(user_data)
        db.session.commit()
        return redirect(url_for('completed_tasks',who = who))
    return render_template("completed_tasks_changer.html",user = user,infoUser = infoUser,form=form)


@app.route('/create_contract', methods=['POST', 'GET'])
@login_required  # только зарегистрированный человек сможет зайти
def contract():
    info = models.User.query.all() #Получаем словарь с содержимым таблиц user и users_Data 
    if request.method == 'POST':
        listForm = request.form.to_dict()
        datStart = datetime.strptime(request.form['start'],'%Y-%m-%d')
        datEnd = datetime.strptime(request.form.get('end'),'%Y-%m-%d')
        del listForm['start']#удаляем элемент времени из списка, что бы заработал цикл
        del listForm['end']#удаляем элемент времени из списка, что бы заработал цикл
        listFormKeys = listForm.keys()# выводим все ключи выбранных блоках
        # вставка данных
        for id in listFormKeys:
            user = models.Users_Data.query.filter_by(id = id).first()#поиск юзера
            email  = models.User.query.filter_by(id = id).first()#поис email
            nameFail = user.name + " " + now.today().strftime("%d.%m.%Y")#имя файла 
            try:
                userData = user.name + "\n" + user.birthDAy + "\n" + user.inn + "\n" + user.passport + "\n" + user.passportBy + "\n" + user.passportData + "\n" + user.passportCod + "\n" + user.address + "\n" + user.bankAccount + "\n" + user.bankName + "\n" + user.bank_details + "\n" + email.email
            except TypeError:
                return render_template('create_contract.html',list=info, error="У " + user.name + " незаполнен личный кабинет")
            
            doc = DocxTemplate("app/static/wordTemplates/шаблон.docx")# открываем шаблон
            context = { #шаблон для записи 
                'date' : now.today().strftime("%d.%m.%Y"), #дата
                'name':user.name, #ФИО
                'userData':userData, # реквезиты
                } 
            doc.render(context)#ввод всех данных
            doc.save("app/static/wordTemplates/" + nameFail + ".docx")#сохранение документа
            # вставка задач
            docx = Document("app/static/wordTemplates/"+ nameFail +".docx")
            task = models.Tasks.query.filter_by(idUser = id).all()# поиск отмеченных пользователя
            i = 0
            for u in task:
                i = i + 1
                if  datEnd > datetime.strptime(u.timeTask,"%d.%m.%Y") > datStart:
                    if i > 1:
                        docx.tables[3].add_row()
                    docx.tables[1]
                    docx.tables[3].cell(i,0).text = u.nameTask# 1 столбец, 2 строка 
                    docx.tables[3].cell(i,1).text = '30 дней с момента подписания настоящего соглашения'
                    docx.tables[3].cell(i,2).text = u.manyTask
            docx.save("app/static/wordTemplates/"+ nameFail +".docx")
            print("привет я начал работать с яндекс диском")
            if yToken.exists("/договора/" + str(user.name)) == False:
                yToken.mkdir("/договора/"+ str(user.name))# создание папки
                try:
                    yToken.upload("app/static/wordTemplates/"+ nameFail +".docx", "/договора/"+ str(user.name)+"/" + nameFail +".docx")
                except yadisk.exceptions.PathExistsError:
                    return render_template('create_contract.html',list=info, error="У " + user.name + " Договор уже создан")
            elif yToken.exists("/договора/"+ str(user.name)) == True:#если папка существует
                try:
                    yToken.upload("app/static/wordTemplates/"+ nameFail +".docx", "/договора/"+ str(user.name)+"/" + nameFail +".docx")
                except yadisk.exceptions.PathExistsError:
                    return render_template('create_contract.html',list=info, error="У " + user.name + " Договор уже создан")
            
        return render_template('create_contract.html',list=info, error = "Документы созданны и внесены на яндекс диск и в личное дело")
    return render_template('create_contract.html', list=info)


@app.route('/admin', methods=['POST', 'GET'])  # Страница, доступная ЛИШЬ админу
@login_required  # только зарегистрированный человек сможет зайти
def admin():
    if current_user.who == 2:
        info = []
        info = models.User.query.all()
        tasks = models.Tasks.query.all()
        projects = models.Project.query.all()
        if request.method == "POST":
            user = models.Users_Data.query.filter_by(id = id).first()#поиск юзера
            task = models.Tasks.query.filter_by(idUser=id).all()
            user_project= models.Users_Projects.query.filter_by(User_id=id).all()
            db.session.delete(user)
            db.session.delete(task)
            db.session.delete(user_project)
            db.session.commit()
        return render_template('admin.html', list=info, tasks=tasks, projects=projects)
    else:
        return render_template('cabinet.html')


# обработка ошибок
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
    # Обработчик ссылок


