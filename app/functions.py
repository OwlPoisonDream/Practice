import posixpath
import yadisk
import os
from app import yToken
from config import Config
from flask import  render_template, request, url_for, redirect
from app import forms, db
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
        
def recursive_upload(y, from_dir, to_dir):# рекурсивная загрузка 
    for root, dirs, files in os.walk(from_dir):
        p = root.split(from_dir)[1].strip(os.path.sep)
        dir_path = posixpath.join(to_dir, p)
        try:
            y.mkdir(dir_path)
        except yadisk.exceptions.PathExistsError:
            for file in files:
                file_path = posixpath.join(dir_path, file)
                p_sys = p.replace("/", os.path.sep)
                in_path = os.path.join(from_dir, p_sys, file)
                try:
                    y.upload(in_path, file_path)
                except yadisk.exceptions.PathExistsError:
                    pass     
                
def yadisk_check_pr(pr_name, yad_pr_way):
    if yToken.exists(yad_pr_way + pr_name) == False:
        print('Папка отсутствует')
        yToken.mkdir(yad_pr_way + pr_name) # создание папки и вывод папки в консоли
    elif yToken.exists(yad_pr_way + pr_name) == True: #если папка существует
        print('Папка существует')
        #print( yToken.check_token()) #получаем информацию о диске
        yToken.listdir(yad_pr_way+ pr_name)#выводим содержимое папки

def yadisk_check_folder(pr_name, user_name):
    if yToken.exists("/Феникс проекты/" + pr_name + "/" + user_name) == False:
        print('Папка отсутствует')
        yToken.mkdir("/Феникс проекты/" + pr_name + "/" + user_name) # создание папки и вывод папки в консоли
    elif yToken.exists("/Феникс проекты/" + pr_name + "/" + user_name) == True: #если папка существует
        print('Папка существует')
        #print( yToken.check_token()) #получаем информацию о диске
        yToken.listdir("/Феникс проекты/" + pr_name + "/" + user_name)#выводим содержимое папки

def yadisk_check_task(pr_name, user_name, task_name):
    if yToken.exists("/Феникс проекты/" + pr_name + "/" + user_name + "/" + task_name) == False:
        print('Папка отсутствует')
        yToken.mkdir("/Феникс проекты/" + pr_name + "/" + user_name + "/" + task_name) # создание папки и вывод папки в консоли
    elif yToken.exists("/Феникс проекты/" + pr_name + "/" + user_name + "/" + task_name) == True: #если папка существует
        print('Папка существует')
        #print( yToken.check_token()) #получаем информацию о диске
        yToken.listdir("/Феникс проекты/" + pr_name + "/" + user_name + "/" + task_name)#выводим содержимое папки
        
def yadisk_check_contract(user_name, filename, info):
    if yToken.exists(Config.yad_con + user_name) == False:
        yToken.mkdir(Config.yad_con+ user_name)# создание папки
        try:
            yToken.upload(Config.way_doc+ filename +".docx", Config.yad_con + user_name+"/" + filename +".docx")
        except yadisk.exceptions.PathExistsError:
                return render_template('create_contract.html',list=info, error="У " + user_name + " Договор уже создан")
    elif yToken.exists(Config.yad_con+ user_name) == True:#если папка существует
        try:
            yToken.upload(Config.way_doc+ filename +".docx", Config.yad_con + user_name+"/" + filename +".docx")
        except yadisk.exceptions.PathExistsError:
            return render_template('create_contract.html',list=info, error="У " + user_name + " Договор уже создан")
        
def info_changer(user_data):
    form = forms.PersonalForm()
    if form.name.data and form.name.data.strip() and form.name.data != None :
        user_data.name = form.name.data
        
    if form.birthDAy.data and form.birthDAy.data != None :
        user_data.birthDAy = form.birthDAy.data

    if form.passport.data and form.passport.data.strip() and form.passport.data != None :
        if form.passport.data[4]==" ":
            user_data.passport = form.passport.data
        else:
            error=error + "\n" + "Неправильно введены серия и номер паспорта"

    if form.passportData.data and form.passportData.data != None :
        user_data.passportData = form.passportData.data
            
    if form.passportBy.data and form.passportBy.data != None :
        user_data.passportBy = form.passportBy.data

    if form.passportCod.data and form.passportCod.data != None:
        if form.passportCod.data[3]=="-":
            user_data.passportCod = form.passportCod.data
        else:
            error=error + "\n" + "Неправильно введён код подразделения"

    if form.nickname.data and form.nickname.strip() and form.nickname.data != None :
        user_data.nickname = form.nickname.data
            
    if form.link_vk.data and form.link_vk.strip() and form.link_vk.data != None :
        user_data.link_vk = form.link_vk.data

    if form.inn.data and form.inn.strip() and form.inn.data != None:
        user_data.inn = form.inn.data
        if len(form.inn.data)!=12:
            error=error + "\n" + "Некорректный ИНН"
    if form.bank_details.data and form.bank_details.strip() and form.bank_details.data != None :
        user_data.bank_details = form.bank_details.data

    if form.bankName.data and form.bankName.strip() and form.bankName.data != None :
        user_data.bankName = form.bankName.data

    if form.phone_number.data and form.phone_number.strip() and form.phone_number.data != None:
        if (form.phone_number.data[0:1]=="+7" or form.phone_number.data[0]=="8"):
            user_data.phone_number = form.phone_number.data
        else:
            error=error + "\n" + "Некорректный номер телефона"

    if str(request.form.getlist('tags')) != "[]":
        user_data.tags = str(request.form.getlist('tags'))
    if form.photo.data != None :
        try:
            # загрузка фото
            f = form.photo.data
            filename = secure_filename(f.filename)
            way = Config.way_photo + user_data.name# указываю путь к папке
            if not os.path.isdir(way):
                os.mkdir(way)# создаю папку
            if os.path.isfile('app/'+ str(user_data.avatar)):# удаляем старый файл если он есть
                os.remove('app/'+str(user_data.avatar))
            f.save(os.path.join(
                way, filename))# сохранения файла
        except FileNotFoundError:
            return render_template('cabinet_changer.html',error="ошибка с сервером")
        if form.photo.data != None :
            user_data.avatar = Config.photo + str(user_data.name) + '/'+ filename # указываю путь к папке
    print(user_data)
    db.session.add(user_data)
    db.session.commit()