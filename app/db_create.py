#для создания БД и тестов над БД
from app import db
from app.models import User


# добавление к таблице User
def addUser(email = "none", password_hash = "none", name = "none", nickname = "none", link_vk = "none" , inn = "none", bank_details = "none", bankName = "none", phone_number = "none"):
    news = User(email = email, password_hash = password_hash, 
    name = name, nickname = nickname, link_vk = link_vk , 
    inn = inn, bank_details = bank_details, bankName = bankName, 
    phone_number = phone_number)
    db.session.add(news)# добавить новые записи в базу данных
    db.session.commit()# закрываем базу данных

# добавление к таблице User
def addTasks(email = "none", password_hash = "none", name = "none", nickname = "none", link_vk = "none" , inn = "none", bank_details = "none", bankName = "none", phone_number = "none"):
    news = 11
    db.session.add(news)# добавить новые записи в базу данных
    db.session.commit()# закрываем базу данных
  # пример чтения БД 
    #peter = User.query.filter_by(email = 'supe@fbfbf').first()
    #print(peter.id)

    #print("Версия SQLAlchemy:", sqlalchemy.__version__)# посмотреть версию SQLAlchemy
    #print(db)# проверка пути БД
if __name__ == '__main__':

    # первая запись
    db.create_all() #создаем БД
    user = User(email="root",who = 3)
    user.set_password("root")
    db.session.add(user)
    db.session.commit()

   

    
  


