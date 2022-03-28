from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_migrate import Migrate

#создание экземпляра приложения
app = Flask(__name__) 
app.config.from_object('config.DevelopementConfig')# назначение конфигурации из другого файла

app.secret_key = 'xxxxyyyyyzzzzz'
#инцилизируем расшерения
db = SQLAlchemy(app)# Инцилизация БД
migrate = Migrate(app, db) # Инцилизация миграций
#mail = Mail(app)# Инцилизация почты
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




from app import views, models,forms

