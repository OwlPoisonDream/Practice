from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from gevent import config
import yadisk # библиотека для работы с яндекс диском

#создание экземпляра приложения
app = Flask(__name__) 
app.config.from_object('config.DevelopementConfig')# назначение конфигурации из другого файла

app.secret_key = 'xxxxyyyyyzzzzz'
#инцилизируем расширения
db = SQLAlchemy(app)# Иницилизация БД
migrate = Migrate(app, db) # Иницилизация миграций
mail = Mail(app)# Иницилизация почты
mail.init_app(app)
login_manager = LoginManager() #Инициализация работы с логинами
login_manager.init_app(app)
login_manager.login_view = 'login'
yToken = "AQAAAABetchDAAfIOoTtzk4Bd0cNm0VX3nt7gWs"# токен для яндекс диска

from app import views, models,forms,email

