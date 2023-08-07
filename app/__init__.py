from flask import Flask
import werkzeug.urls
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
import yadisk # библиотека для работы с яндекс диском
import ssl
from flask_socketio import SocketIO#для работами с сокетами


#создание экземпляра приложения
application = Flask(__name__) 
application.config.from_object('config.DevelopementConfig')# назначение конфигурации из другого файла

application.secret_key = 'xxxxyyyyyzzzzz'
#инцилизируем расширения
db = SQLAlchemy(application)# Иницилизация БД
migrate = Migrate(application, db) # Иницилизация миграций
mail = Mail(application)# Иницилизация почты
mail.init_app(application)
login_manager = LoginManager() #Инициализация работы с логинами
login_manager.init_app(application)
login_manager.login_view = 'login'
yToken = yadisk.YaDisk(token="AQAAAABetchDAAfIOoTtzk4Bd0cNm0VX3nt7gWs")# токен для яндекс диска
socketio = SocketIO(application)# подключение сокета

from app import views, models,forms,email

