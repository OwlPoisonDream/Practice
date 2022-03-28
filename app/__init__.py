from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_migrate import Migrate

#создание экземпляра приложения
app = Flask(__name__) 
app.config.from_object('config.DevelopementConfig')# назначение конфигурации из другого файла

app.secret_key = 'xxxxyyyyyzzzzz'
#инцилизируем расширения
db = SQLAlchemy(app)# Иницилизация БД
migrate = Migrate(app, db) # Иницилизация миграций
#mail = Mail(app)# Иницилизация почты
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




from app import views, models,forms

