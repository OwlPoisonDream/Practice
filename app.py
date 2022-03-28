# Импорт библиотек
from flask import Flask, render_template, request, url_for
# Запуск сервера и связь с базой данных на будущее
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phoenix.db'

# Создание словаря. Заполнен тестовыми переменными
person_account = {
    'name': 'Test Object 2-gou',
    'nickname': 'Test',
    'vk_link': 'vk.com/poisonowl',
    'INN': '119112475684',
    'bank_details': 'БИК: 044525225, КПП: 773601001, ИНН: 7707083893',
    'bank_name': 'Sberbank',
    'password': '1234',
    'email': 'test_object@gmail.com',
    'phone_number': '+79777777777'
}


# Запуск странички с отображением данных личного кабинета
@app.route('/cabinet', methods=['GET'])
def cabinet():
    url_sequence = 'test'
    person_account[url_sequence] = person_account
    return render_template('cabinet_test.html', person_account = person_account, url_sequence = url_sequence)


# Запуск странички с изменением существующих данных.
@app.route('/info_change', methods=['POST','GET'])
def info_change():
    if request.method=="POST":
        name = request.form.get('name')
        nickname = request.form.get('nickname')
        vk_link = request.form.get('vk_link')
        INN = request.form.get('inn')
        bank_details = request.form.get('bank_details')
        bank_name = request.form.get('bank_name')
        current_password = person_account['password']
        new_pass = request.form.get('new_pass')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        if current_password == request.form.get('old_pass'):  # Проверка на соответствие старого пароля, полученного с формы
            if new_pass == request.form.get('repeat_pass'):  # Проверка на новый пароль, чтобы пользователь не ошибся
                new_pass = new_pass
                # Очищение и заполнение словаря данными
                person_account.clear()
                person_account['name'] = name
                person_account['nickname'] = nickname
                person_account['vk_link'] = vk_link
                person_account['INN'] = INN
                person_account['bank_details'] = bank_details
                person_account['bank_name'] = bank_name
                person_account['password'] = new_pass
                person_account['email'] = email
                person_account['phone_number'] = phone_number
                return (person_account)
            else:
                return "error"
        else:
            return "error"
    return  render_template('info_change.html', person_account=person_account)


@app.route('/login', methods = ['POST','GET'])
def login():
    return render_template('login.html')


@app.route('/register', methods = ['POST', 'GET'])
def register():
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)
    print(person_account)
