# Обработчик ссылок
from calendar import month
from operator import truth
from turtle import color
from unicodedata import name
from flask import  render_template, flash, request, redirect, url_for
from requests import patch
from sqlalchemy import values  # для работы с интернетом
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
from app import app, models, db, forms
from app.email import send_password_reset_email
import yadisk
from docx import Document # вставка таблицы в word 
import os
from datetime import datetime, timedelta,date
from app import yToken
from config import Config
from app import functions
from werkzeug.utils import secure_filename
import random


now = datetime.now()# заппуск считывания времени
       
@app.route('/createDb')  # вход
@login_required  # только зарегистрированный человек сможет зайти
def createDb():
    db.create_all()  # создаем БД
    user = models.User(email="root", who=3)
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
            login_user(user, remember=form.remember.data) # запуск сессии пользователя
            return redirect(url_for('cabinet'))
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route('/register', methods=['POST', 'GET'])# регистрация
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data, who=3)# блокируем профиль
        user.set_password(form.password.data)
        db.session.add(user)
        userId = db.session.query(models.User).filter(models.User.email == form.email.data).first()
        userData = models.Users_Data(idUser=userId.id, name="none",
                                     birthDAy="none", passport="none", passportData="none",
                                     passportBy="none", passportCod="none", nickname="none",
                                     link_vk="none", inn="none", bank_details="none", bankName="none",
                                     up_ooo = "none",phone_number="none",chekManager = "none",avatar ="static/x_06eb1977.jpg")
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
    #print(current_user)# просмотрт под каким пользователем вошел человек
    info = functions.chekCabinet(current_user)# проверка заполненного профиля
    return render_template('cabinet.html', current_user=current_user,info=info)
    


@app.route('/cabinet_changer',methods=['POST', 'GET'])  # Страница для изменения данных в личном кабинете и вноса изменений в базу данных
@login_required  # только зарегистрированный человек сможет зайти
def cabinet_changer():
    form = forms.PersonalForm()
    form.nickname.default = "Саня"
    error = ""
    if request.method == 'POST':
        functions.info_changer(db.session.query(models.Users_Data).filter_by(idUser=current_user.id).one())
        return redirect(url_for('cabinet'))
    return render_template('cabinet_changer.html', form=form, error = error)


@app.route('/my_tasks', methods=['GET', 'POST'])  # Страница с задачами пользователя
@login_required  # только зарегистрированный человек сможет зайти
def my_tasks(): 
    tasks = models.Tasks.query.all()# таблица задачь
    if now.month < 10: #Проверка на месяц
        today = str(now.year) + "-0" + str(now.month) + "-"  #Облегчаем проверку
    else:
        today = str(now.year) + "-" + str(now.month) + "-"  #Облегчаем проверку
    if now.day<10:
        today = today + "0" + str(now.day) #Сегодняшний день
    else:
        today = today + str(now.day)
    #print(today) #Вывожу время
    # print(list(yToken.listdir("")))
    if request.method == "POST":
        listForm = request.form.to_dict()# получение информации из формы
        qeru = models.Tasks.query.filter_by(id = listForm['task_into']).first()#поиск юзера
        print(qeru.linkDisk)
        files = request.files.getlist("file")
        for file in files:
            print("я работаю")
            file.save(os.path.join(Config.way_task, file.filename))
            #os.remove(way + file.filename)
        functions.recursive_upload(yToken, Config.way_task, qeru.linkDisk +"/"+ qeru.nameTask)

        qeru.statusСompleted = "Complete"
        qeru.linkDisk = qeru.linkDisk
        db.session.add(qeru)
        db.session.commit()
        return render_template("my_documents.html")
    
    return render_template("my_tasks.html", tasks=tasks, today=today, now=now, current_user = current_user)


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
            #print("привет я начал работать с яндекс диском")
            listForm = request.form.to_dict()# получение информации из формы
            #print(user.name)
        files = request.files.getlist("file")
        for file in files:
            #print("я работаю")
            file.save(os.path.join(Config.way_check, file.filename))
            #os.remove(way + file.filename)
        functions.recursive_upload(yToken, Config.way_check, "/чеки/" + user.name)
            
        return render_template('my_documents.html',list=List, error = "Чек прикреплён и внесен на яндекс диск")
    try:
        docList = list(yToken.listdir('/договора/' + user.name))
        a = 0
        for i in docList:
            d = {docList[a].name : docList[a].file}
            List.update(d)
            a = a + 1  
    except yadisk.exceptions.PathNotFoundError:
        return render_template("my_documents.html",list = List,error = "Договор с вами еще не составлен")
    return render_template("my_documents.html", list = List)


base = {'idProject':"", 'id_folder': ""}
@app.route('/my_projects', methods=['GET', 'POST'])  # Страница с проектами шоураннера
@login_required  # только зарегистрированный человек сможет зайти
def my_projects():
    error = ""
    projects = models.Project.query.all() #запрос в базу данны для вывода проектов
    user_project = models.Users_Projects.query.all()#запрос в базу данны для вывода какой человек к каому проекту
    info = models.User.query.all() #запрос в базу данны для вывода людей
    tasks = models.Tasks.query.all()# таблица задачь
    folders = models.Folder.query.all()# таблица папок

    
    if request.method == 'POST': # обработка post
        listForm = request.form.to_dict()# получение информации из формы
        print(listForm)
        
        # добавить людей
        if (listForm.get('thePiple')):
            print("добавить человека------------------------")
            for k, v in listForm.items():
                if v == 'id_sel':
                    print(k)
                    if (models.Users_Projects.query.filter_by(User_id = k,Project_id = listForm.get('thePiple')).first()):
                        continue
                    else:
                        print("я добовляю:" + k)
                        update_user_projects = models.Users_Projects(User_id = k, Project_id = listForm.get('thePiple'))# обновления таблицы Users_project
                        db.session.add(update_user_projects)# запись в базу данных users_projekt
                        db.session.commit()# закрытие соеденения с бд
            return redirect(url_for('my_projects'))           

        # форма добавления фона
        if (listForm.get('theBackground')):
            print("добавить фон-----------------------------")
            
            file = request.files['file']
            print(file)
            if file.filename =='':
                print("файла нет")
            else:
                filename = secure_filename(file.filename)# безопасно извлекаем оригинальное имя файла
                print(filename)
                way = Config.linkPoto # указываю путь к папке
                print(way)
                file.save(os.path.join(way,filename))# сохранения файла
                patch = 'static/photoProjekt/' + filename
                print(patch)
                update = db.session.query(models.Project).filter_by(id = int(listForm['theBackground'])).one()# обновления таблицы Users_project
                update.linkPoto = patch
                print(update)
                db.session.add(update)#обновление данных
                db.session.commit()# закрытие соеденения с бд
          
        
        # создание проекта
        if (listForm.get('projectName')):
            if (models.Project.query.filter_by(projectName = listForm['projectName']).first()):
                error = "имя уже занято, проект не создался"
                return render_template("my_projects.html", projects = projects, list = info, 
                    user_project = user_project, 
                    folders = folders,
                    tasks = tasks, error = error)
            pr_name = str(listForm["projectName"])
            functions.yadisk_check_pr(str(listForm["projectName"]), Config.yad_pr_way)
            createProjekt = models.Project(projectName = pr_name,# создание проекта
            descProject = listForm['descProject'], linkDisk = Config.yad_pr_way+ pr_name, linkPoto = 'static/photoProjekt/primer.jpg')

            db.session.commit()# создание соеденения
            db.session.add(createProjekt)# запись в базу данных users_projekt
            id_project = models.Project.query.filter_by(projectName = pr_name).first()
            print(id_project.id)
            for k, v in listForm.items():
                if v == 'id_sel':
                    update_user_projects = models.Users_Projects(User_id = k, Project_id = id_project.id)# обновления таблицы Users_project
                    db.session.add(update_user_projects)# запись в базу данных users_projekt
            db.session.commit()# закрытие соеденения с бд
            return redirect(url_for('my_projects'))

   
    return render_template("my_projects.html", projects = projects, list = info, 
                    user_project = user_project,error = error)

@app.route('/projects/<proj>/<topFolder>/', methods=['GET', 'POST'])  # Страница с папками и задачами шоуранера
@login_required  # только зарегистрированный человек сможет зайти
def projekt(proj,topFolder):
    print(proj)# id проекта
    print(topFolder)# верхняя папка
    project = models.Project.query.filter_by(id = proj).one()
    # ищем все папки и и все задачи этого проекта
    tasks = models.Tasks.query.filter_by(idProject = proj,id_folder = topFolder).all()# таблица задачь
    folders = models.Folder.query.filter_by(id_progect = proj,id_folder = topFolder).all()# таблица папок
    user_project = models.Users_Projects.query.filter_by(Project_id = proj).all()#запрос в базу данны для вывода какой человек к каому проекту
    massege = models.Massege.query.filter_by(id_progect = proj,id_folder = topFolder).all()# таблица сообщений

    if (topFolder == "-1"):
        print("")
        url = project.projectName
    else:
        foldersTop = models.Folder.query.filter_by(id_progect = proj,id = topFolder).one()# таблица верхней папки
        url = project.projectName + foldersTop.link
    print(folders)
    form = forms.CreateTask()# создание задачи

    if request.method == 'POST': # обработка post
        listForm = request.form.to_dict()# получение информации из формы
        print(listForm)

        # для создании задачи
        if (listForm.get('nameTask')):
            print("я создаю задачу")
            link = ""
            for k, v in listForm.items():
                if v == 'id_sel':
                    user = models.Users_Data.query.filter_by(idUser = k).one()
                    if user.up_ooo == 0:
                        receipt = 0
                    else:
                        receipt = 1

                    if (topFolder == "-1"):
                        link = "/" + listForm['nameTask']
                    if (topFolder != "-1"):
                        link = foldersTop.link + "/" + listForm['nameTask']
                    createTask = models.Tasks(idUser = k, idProject = proj, id_folder = topFolder,
                    nameTask = listForm['nameTask'],descTask = listForm['descTask'],timeTask = listForm['timeTask'],
                    manyTask = listForm['manyTask'],statusСompleted = "Uncomplete",receipt=receipt,linkDisk = link)
                    db.session.commit()# создание соеденения
                    db.session.add(createTask)# запись в базу данных users_projekt
                    db.session.commit()# закрытие соеденения с бд
                    functions.yadisk_check_task(project.projectName, user.name, listForm['nameTask']) 
                    return redirect(url_for('my_projects')) 
        
        # для создании папки
        if (listForm.get('folderName')):
            print("я создаю папку")
            link =""
            if (topFolder == "-1"):
                link = "/" + listForm['folderName']
            if (topFolder != "-1"):
                link = foldersTop.link + "/" + listForm['folderName']
            createFolder = models.Folder(name = listForm['folderName'],id_progect = proj,link =link,
                color="#c99f2d",id_folder=topFolder)
            db.session.commit()# создание соеденения
            db.session.add(createFolder)# запись в базу данных users_projekt
            db.session.commit()# закрытие соеденения с бд
            functions.yadisk_check_folder(link)
            return redirect(url_for('my_projects'))
    
    return render_template("projects.html",form=form,tasks = tasks,folders = folders,proj=proj,url=url,
            list = user_project,massege=massege)

        

@app.route('/salary', methods=['GET', 'POST'])  # Страница с зарплатами. Менеджер видит и устанавливает
@login_required  # только зарегистрированный человек сможет зайти
def salary():
    task = models.Tasks.query.filter_by(idUser = current_user.id).all()# поиск отмеченных пользователя
    total = 0
    for u in task:
        if u.statusСompleted=="Complete":
            total = int(u.manyTask) + total
    for u in task:
        u.timeTask = u.timeTask[8:10] + "." + u.timeTask[5:7] + "." + u.timeTask[0:4]
        u.timeTask = datetime.strptime(u.timeTask,'%d.%m.%Y').date()
    a = date.today()# время сейчас
    b = date.today() - timedelta(days=7)#время неделю назад
    c = date.today() - timedelta(weeks = 4)#время месяц назад
    d = date.today() - timedelta(weeks = 48)#время год назад
    return render_template("salary.html", task = task, a = a, b = b, c = c, d = d, total = total)


@app.route('/employeers', methods=['GET', 'POST'])  # Страница с сотрудниками компании. Доступна менеджеру
@login_required  # только зарегистрированный человек сможет зайти
def employeers():
    info = models.User.query.all()
    if request.method == 'POST': # обработка post
        personal = request.form.get('person')# получение информации из формы
        print(personal)
        user = models.User.query.filter_by(id = personal).first()
        user.pr.chekManager = 2
        db.session.add(user)
        db.session.commit()
        #создаем договор
        # email  = models.User.query.filter_by(id = id).first()#поис email
        try:
            userData = user.pr.name + "\n" + "ИНН" + " " + user.pr.inn + "\t" + "ОГРН" + " " + user.pr.ogrn + "\n" + "Паспорт гражданина РФ" + "\n" + user.pr.passport + "\n" + "Выдан" + " " + user.pr.passportBy + " " + user.pr.passportData + "\n" "Код подразделения" + " " + user.pr.passportCod + "\n" + "Адрес:" + " " + user.pr.address + "\n" + "Номер счёта" + " " + user.pr.bankAccount + "\n" + "Банк получателя" + " " + user.pr.bankName + "\n" + " " + user.pr.bank_details + "\n" + user.email
        except TypeError:
                return render_template('employeers.html', error="У " + user.pr.name + " незаполнен личный кабинет", list = info)
        context = { #шаблон для записи 
                'date' : now.today().strftime("%d.%m.%Y"), #дата
                'name':user.pr.name, #ФИО
                'userData':userData, # реквезиты
                }
        Config.doc.render(context)#ввод всех данных
        nameFail = user.pr.name + " " + now.today().strftime("%d.%m.%Y")#имя файла 
        Config.doc.save(Config.way_doc + nameFail + ".docx")#сохранение документа
        functions.yadisk_check_contract(user.pr.name, nameFail, info)
        print("привет я начал работать с яндекс диском")
        #functions.yadisk_check_contract(user.name, nameFail, info)
    return render_template("employeers.html", list = info)


@app.route('/completed_tasks/<who>/', methods=['GET', 'POST'])  # Страница с выполненными задачами по людям
@login_required  # только зарегистрированный человек сможет зайти
def completed_tasks(who):
    user = models.User.query.filter_by(id = who).first()
    infoUser = models.Users_Data.query.filter_by(idUser = who).first()
    try:
        docList = list(yToken.listdir(Config.yad_con + infoUser.name))
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
    if request.method == 'POST':
        print("я нажал на кнопку")
        listForm = request.form.to_dict()# получение информации из формы
        print(listForm)
        functions.info_changer(db.session.query(models.Users_Data).filter_by(idUser=who).one())
        print(user.email, user.who)
        user.who=request.form.get("status")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('employeers'))
    return render_template("completed_tasks_changer.html",user = user,infoUser = infoUser,form=form)


@app.route('/create_contract', methods=['POST', 'GET'])
@login_required  # только зарегистрированный человек сможет зайти
def contract():
    info = models.User.query.all() #Получаем словарь с содержимым таблиц user и users_Data 
    
    if request.method == 'POST':
        listForm = request.form.to_dict()
        datStart = datetime.strptime(request.form['start'],'%Y-%m-%d')
        datEnd = datetime.strptime(request.form.get('end'),'%Y-%m-%d')
        print(datStart.day,datEnd.day)
        if datStart.day>datEnd.day:
            random_day = random.randint(datEnd.day, datStart.day)
        else:
            random_day = random.randint(datStart.day,datEnd.day)
        print(random_day)
        del listForm['start']#удаляем элемент времени из списка, что бы заработал цикл
        del listForm['end']#удаляем элемент времени из списка, что бы заработал цикл
        listFormKeys = listForm.keys()# выводим все ключи выбранных блоках
        # вставка данных
        for id in listFormKeys:
            user = models.Users_Data.query.filter_by(id = id).first()#поиск юзера
            
            nameFail = "акт" + " " + user.name + " " + now.today().strftime("%d.%m.%Y")#имя файла 
            # вставка задач
            docx = Document(Config.way_doc + "шаблон_акт" +".docx")# открываем шаблон
            all_tables = docx.tables
            print('Всего таблиц в документе:', len(all_tables))
            task = models.Tasks.query.filter_by(idUser = id).all()# поиск отмеченных пользователя
            i = 0
            for u in task:
                if task.statusСompleted=="Complete":
                    i = i + 1
                    if  datEnd > datetime.strptime(u.timeTask,'%Y-%m-%d') > datStart:
                        if i > 1:
                            docx.tables[1].add_row()
                        docx.tables[1]
                        docx.tables[1].cell(i,0).text = u.nameTask# 1 столбец, 2 строка 
                        docx.tables[1].cell(i,1).text = '30 дней с момента подписания настоящего соглашения'
                        docx.tables[1].cell(i,2).text = u.manyTask
            docx.save(Config.way_doc+ nameFail +".docx")
            print("привет я начал работать с яндекс диском")
            functions.yadisk_check_contract(user.name, nameFail, info)
            
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
