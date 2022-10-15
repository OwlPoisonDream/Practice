# файл конфигурации 
import os
from docxtpl import DocxTemplate # вставка данных в word 


app_dir = os.path.abspath(os.path.dirname(__file__)) # путь файла для загрузки модуля 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') # Задаем токен для генерации cookie
    SQLALCHEMY_TRACK_MODIFICATIONS = False # отключаем модификацию SQLAlchemy
    SQLALCHEMY_DATABASE_URI = '' #ссылка на SQL

    ##### настройка Flask-Mail #####
    ADMINS = [''] 
    MAIL_SERVER = 'smtp.yandex.com'#название сервиса почты
    MAIL_PORT = 465 #порт почты
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('')# логин, а именно почта 
    MAIL_PASSWORD = os.environ.get('')# пароль от почты 
    MAIL_DEFAULT_SENDER = MAIL_USERNAME #email отправителя
    
    way_photo = 'static/photos/' #Путь хранения фотографий для аватарок
    way_task = 'app/static/workTemplates/' # Путь хранения файлов для задач, которые удаляются после загрузки
    way_check = 'app/static/checkTemplates/' #Путь хранения чеков, которые удаляются после загрузки
    doc = DocxTemplate("app/static/wordTemplates/шаблон_договор.docx")# открываем шаблон договра
    doc_act = DocxTemplate("app/static/wordTemplates/шаблон_акт.docx")# открываем шаблон акта
    way_doc = "app/static/wordTemplates/" #Путь хранения документов
    yad_pr_way = "/Феникс проекты/" #Папка проектов в Яндекс Диске
    yad_con = "/договора/" #Папка договоров в Яндекс Диске
    photo = 'static/photos/' #Папка фотографий
    linkPoto = 'static/photoProjekt/' #Папка хранения фотографий для проекта
    
    


class DevelopementConfig(Config): # Конфигурация разработки
    DEBUG = True #состояние дебага
    

class TestingConfig(Config):# Конфиуграция для тестирования
    DEBUG = True #состояние дебага
    

class ProductionConfig(Config):#Конфигурация
    DEBUG = False #состояние дебага
