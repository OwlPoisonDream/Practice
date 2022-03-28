#для создания БД и тестов над БД
from app import db
from models import User


# добовление к таблице User
def addUser(email = "none", password_hash = "none", name = "none", nickname = "none", link_vk = "none" , inn = "none", bank_details = "none", bankName = "none", phone_number = "none"):
    news = User(email = email, password_hash = password_hash, 
    name = name, nickname = nickname, link_vk = link_vk , 
    inn = inn, bank_details = bank_details, bankName = bankName, 
    phone_number = phone_number)
    db.session.add(news)# добавить новые записи в базу данных
    db.session.commit()# закрываем базу данных

# добовление к таблице User
def addTasks(email = "none", password_hash = "none", name = "none", nickname = "none", link_vk = "none" , inn = "none", bank_details = "none", bankName = "none", phone_number = "none"):
    news = 11
    db.session.add(news)# добавить новые записи в базу данных
    db.session.commit()# закрываем базу данных


if __name__ == '__main__':
    #print("Версия SQLAlchemy:", sqlalchemy.__version__)# посмотреть версию SQLALchemy
    #print(db)# проверка пути БД
    db.create_all()#создание БД

    # пример чтения БД 
    peter = User.query.filter_by(email = 'supe@fbfbf').first()
    print(peter.id)

    # Обновление записи

   

    
  


