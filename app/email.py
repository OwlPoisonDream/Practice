# Импорты, ничего нового...
# надо все проверить, но потом
from threading import Thread
from flask import render_template
from flask_mail import Message
from app import app
import smtplib as smtp


def send_password_reset_email(user):
    print("я отпровляю сообщение востоновления пароля")
    token = user.get_reset_password_token()
    #print(render_template('email/reset_password.html', user=user, token=token))
    email = app.config['MAIL_USERNAME'] # почта от феникса
    password = app.config['MAIL_PASSWORD'] # пароль от феникса 
    dest_email = user.email # пароль от почты
    subject = 'Востоновление пароля от сервиса Kirin' # заголовок

    email_text = "перейдите по ссылке для ввода нового пароля " + render_template('email/reset_password.html', user=user, token=token) # это ссылка

    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,# вот тут происходит магия
                                                       dest_email, 
                                                       subject, 
                                                       email_text).encode('utf-8')

    server = smtp.SMTP_SSL('smtp.yandex.com')
    server.set_debuglevel(1)
    server.ehlo(email)
    server.login(email, password)
    server.auth_plain()
    server.sendmail(email, dest_email, message)
    server.quit()