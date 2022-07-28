# Файл запуска проекта
from app import application



if __name__ == '__main__':
    context = ('certificate.crt', 'locall.key')#certificate and key files
    application.run(host = '0.0.0.0') #Запуск сервера
    #socketio.run(application, host = '37.140.192.75') #Попытки перевода сервер на новые протоколы
    #socketio.run(application, host='0.0.0.0', debug=True, keyfile='locall.key', certfile='certificate.crt')# для тестов
 
