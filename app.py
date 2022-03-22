from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

# Создать вход, выход и личный кабинет


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phoenix.db'
user_db = SQLAlchemy(app)




class User(user_db.Model):
    id = user_db.Column(user_db.Integer, primary_key =True)
    name = user_db.Column(user_db.String(100), nullable=False)
    nickname = user_db.Column(user_db.String(20), nullable=False)
    link_vk = user_db.Column(user_db.String(50), nullable=False)
    inn = user_db.Column(user_db.String(12), nullable=False)
    rek_data = user_db.Column(user_db.String(100), nullable=False)
    password = user_db.Column(user_db.String(15), nullable=False)
    login = user_db.Column(user_db.String(20), nullable=False)
    phone_number = user_db.Column(user_db.String(11), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("main.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/main_cabinet')
def main_cabinet():
    users = User.query.order_by(User.date).all()
    return render_template("cabinet_test.html", users=users)


@app.route('/admin')
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    user_db = SQLAlchemy(app)
    print(user_db)
    app.run(debug=True)
