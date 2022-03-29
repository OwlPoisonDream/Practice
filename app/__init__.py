from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

#создание экземпляра приложения
app = Flask(__name__) 
app.config.from_object('config.DevelopementConfig')# назначение конфигурации из другого файла

app.secret_key = 'xxxxyyyyyzzzzz'
#инцилизируем расшерения
db = SQLAlchemy(app)# Инцилизация БД
migrate = Migrate(app, db) # Инцилизация миграций
mail = Mail(app)# Инцилизация почты
mail.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'





from app import views, models,forms,email

