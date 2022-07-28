# Импорты, ничего нового...
# надо все проверить, но потом
from threading import Thread
from flask import render_template
from flask_mail import Message
from app import application
import smtplib as smtp
from config import Config
import os

#Функция отправки сообщения на почту
def send_password_reset_email(user):
    print("я отправляю сообщение восстановления пароля")
    token = user.get_reset_password_token() #Вызов функции для получения токена для смены пароля
    email = 'fenix4dminproba@yandex.ru' # почта от феникса
    password = 'pmdufnoeqlwfnwbq' # пароль от феникса
    dest_email = user.email # пароль от почты
    subject = 'Восстановление пароля от сервиса Kirin' # заголовок

    email_text = "Перейдите по ссылке для ввода нового пароля " + render_template('email/reset_password.html', user=user, token=token) # это ссылка

    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,# вот тут происходит магия и отправляет структурированное сообщение пользователю
                                                       dest_email, 
                                                       subject, 
                                                       email_text).encode('utf-8')
#Отправление команды серверу на страницу восстановления пароля с поиском почты пользователя, запрашивающего смену, а также хеширования нового пароля, который получен от пользователя.
    server = smtp.SMTP_SSL('smtp.yandex.com')
    server.set_debuglevel(1)
    server.ehlo(email)
    server.login(email, password)
    server.auth_plain()
    server.sendmail(email, dest_email, message)
    server.quit()