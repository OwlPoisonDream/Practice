import posixpath
from unicodedata import name
import yadisk
import os
from app import yToken,db,models
from config import Config
from flask import  render_template, request, url_for, redirect
from app import forms, db
from werkzeug.utils import secure_filename
from random import randrange
from datetime import timedelta

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
        
def recursive_upload(y, from_dir, to_dir):# рекурсивная загрузка, яндексдиск, откуда, куда
    for root, dirs, files in os.walk(from_dir):
        print(files)
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

# создание пути папки           
def yadisk_check_pr(path): #путь, имя папки
    print(path)
    endEl = "/Феникс проекты/" + path.split('/')[0]
    for el in path.split('/'):
        print(el)
        if el == path.split('/')[0]:
            if yToken.exists(endEl) == False:
                yToken.mkdir(endEl)
        if el != path.split('/')[0]:
            endEl = endEl + "/" + el
            if yToken.exists(endEl) == False:
                yToken.mkdir(endEl)
    return endEl# делаем папку публичной

def yadisk_check_folder(pr_name, user_name, folder_name):
    if yToken.exists("/Феникс проекты/" + pr_name) == False:
        print('Папка отсутствует')
        yToken.mkdir("/Феникс проекты/" + pr_name) # создание папки и вывод папки в консоли
        if yToken.exists("/Феникс проекты/" + pr_name + "/" + user_name) == False:
            print('Папка отсутствует')
            yToken.mkdir("/Феникс проекты/" + pr_name + "/" + user_name) # создание папки и вывод папки в консоли
    elif yToken.exists("/Феникс проекты/" + pr_name) == True: #если папка существует
        print('Папка существует')
        yToken.listdir("/Феникс проекты/" + pr_name)#выводим содержимое папки
        if yToken.exists("/Феникс проекты/" + pr_name + "/" + user_name) == False:
            print('Папка отсутствует')
            yToken.mkdir("/Феникс проекты/" + pr_name + "/" + user_name) # создание папки и вывод папки в консоли
        elif yToken.exists("/Феникс проекты/" + pr_name + "/" + user_name) == False:
            print('Папка существует')
            yToken.listdir("/Феникс проекты/" + pr_name)#выводим содержимое папки
            yToken.listdir("/Феникс проекты/" + pr_name + "/" + user_name)#выводим содержимое папки

# создание папки названия 
def yadisk_check_task(pr_name, user_name, task_name):# имя проекта,user,имя задачи
    if yToken.exists("/Феникс проекты/") == False:
        print('Папка отсутствует')
        yToken.mkdir("/Феникс проекты/") # создание папку
        if yToken.exists("/Феникс проекты/" + pr_name) == False:
            yToken.mkdir("/Феникс проекты/" + pr_name) # создание папки 
            if yToken.exists("/Феникс проекты/" + pr_name + "/" + user_name) == False:
                yToken.mkdir("/Феникс проекты/" + pr_name + "/" + user_name) # создание папки 
                if yToken.exists("/Феникс проекты/" + pr_name + "/" + user_name + "/" + task_name) == False:
                    yToken.mkdir("/Феникс проекты/" + pr_name + "/" + user_name + "/" + task_name) # создание папки
    elif yToken.exists("/Феникс проекты/") == True: #если папка существует
        print("не существует")
    return yToken.get_public_meta("/Феникс проекты/" + pr_name +"/" + user_name + "/" + task_name)
        
    
        
def info_changer(user_data):
    listForm = request.form.to_dict()# получение информации из формы
    form = forms.PersonalForm()
    if form.name.data and str(form.name.data).strip() and form.name.data != None :
        user_data.name = form.name.data
        user_data.chekManager = 1
    if form.birthDAy.data and form.birthDAy.data != None :
        user_data.birthDAy = form.birthDAy.data
        user_data.chekManager = 1
    if form.passport.data and str(form.passport.data).strip() and form.passport.data != None :
        user_data.passport = form.passport.data
        user_data.chekManager = 1
    if form.passportData.data and form.passportData.data != None :
        user_data.passportData = form.passportData.data
        user_data.chekManager = 1
    if form.passportBy.data and form.passportBy.data != None :
        user_data.passportBy = form.passportBy.data
        user_data.chekManager = 1
    if form.passportCod.data and form.passportCod.data != None:
        user_data.passportCod = form.passportCod.data
        user_data.chekManager = 1
    if form.nickname.data and form.nickname.data != None :
        user_data.nickname = form.nickname.data
        user_data.chekManager = 1
    if form.link_vk.data and str(form.link_vk).strip() and form.link_vk.data != None :
        user_data.link_vk = form.link_vk.data
        user_data.chekManager = 1
    if form.inn.data and str(form.inn).strip() and form.inn.data != None:
        user_data.inn = form.inn.data
        user_data.chekManager = 1
    if form.bankAccount.data and str(form.bankAccount).strip() and form.bankAccount.data != None:
        user_data.bankAccount = form.bankAccount.data
        user_data.chekManager = 1
    if form.bank_details.data and str(form.bank_details).strip() and form.bank_details.data != None :
        user_data.bank_details = form.bank_details.data
        user_data.chekManager = 1
    if form.bankName.data and str(form.bankName).strip() and form.bankName.data != None :
        user_data.bankName = form.bankName.data
        user_data.chekManager = 1
    if form.phone_number.data and str(form.phone_number).strip() and form.phone_number.data != None:
        user_data.phone_number = form.phone_number.data
        user_data.chekManager = 1
    if form.address.data and str(form.address).strip() and form.address.data != None:
        user_data.address = form.address.data
        user_data.chekManager = 1
    print(form.tags.data)
    if form.tags.data and str(form.tags).strip() and form.tags.data != None:
        print(form.tags.data)
        user_data.tags = form.tags.data
        user_data.chekManager = 1
    if (request.files.getlist("file")):
        file = request.files.getlist("file")
        for file in file:
            if user_data.avatar!="static/x_06eb1977.jpg" and file.filename != None and file.filename != "":
                os.remove('app/' + user_data.avatar)
            if file.filename!="":
                file.save("app/" + os.path.join(Config.way_photo , file.filename))
                user_data.avatar = Config.photo + file.filename # указываю путь к папке
    if form.up_ooo.data != None :
        user_data.up_ooo = form.up_ooo.data
        user_data.chekManager = 1
    if form.ogrn.data and str(form.ogrn).strip() and form.ogrn.data != None :
        user_data.ogrn = form.ogrn.data
        user_data.chekManager = 1
    db.session.add(user_data)
    db.session.commit()
    return "user_data"

def chekCabinet(user):
    #print(user.first())
    #print(user.pr.passport)
    if (user.pr.chekManager == 2):
        return "профиль заполнен и проверен менеджером"

    elif (user.pr.name and user.pr.nickname and user.pr.birthDAy and user.pr.passport and user.pr.passportData and user.pr.passportBy and user.pr.passportCod and user.pr.address and user.pr.bankAccount and user.pr.inn and user.pr.bank_details and user.pr.bankName and user.pr.phone_number != "none" ):
        
        user.pr.chekManager = 1
        db.session.add(user)
        db.session.commit()
        return "Профиль заполнен и отправлен на проверку менеджеру"
    else:
        user.pr.chekManager = 0
        db.session.add(user)
        db.session.commit()
        return"Профиль не заполнен"

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# рандомная дата
def random_date(start, end): # первая дата, последня дата
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)