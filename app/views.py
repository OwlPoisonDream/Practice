# Обработчик ссылок
import email
from flask import  render_template, request, redirect, url_for  # для работы с интернетом
from flask_login import  login_required, login_user, current_user, logout_user
from app import app, models, db, forms
from app.email import send_password_reset_email
import yadisk
from docx import Document
import datetime
from app import yToken

now = datetime.datetime.now()
document = Document()
# print("[log] обработка страниц запущена")

@app.route('/createDb')  # вход
def createDb():
    db.create_all()  # создаем БД
    user = models.User(email="root", who=2)
    user.set_password("root")
    db.session.add(user)
    db.session.commit()


@app.route('/', methods=['POST', 'GET'])  # вход
def index():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db.session.query(models.User).filter(models.User.email == form.email.data).first()
        print(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)  # запуск сессии пользователя
            return redirect(url_for('cabinet'))
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route('/register', methods=['POST', 'GET'])  # регистрация
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data, who=0)
        user.set_password(form.password.data)
        db.session.add(user)
        userId = db.session.query(models.User).filter(models.User.email == form.email.data).first()
        userData = models.Users_Data(idUser=userId.id, name="none",
                                     birthDAy="none", passport="none", passportData="none",
                                     passportBy="none", passportCod="none", nickname="none",
                                     link_vk="none", inn="none", bank_details="none", bankName="none",
                                     phone_number="none")
        db.session.add(userData)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout')  # выход из аккаунта
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/reset_password_request', methods=['GET', 'POST'])  # Страница просьбы о смене пароля
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('index'))
    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])  # Страница сброса пароля и обработка его смены
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = models.User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/cabinet', methods=['POST', 'GET'])  # Личный кабинет
@login_required  # только зарегистрированный человек сможет зайти
def cabinet():
    print("--------------------")
    print(current_user)
    print("--------------------")
    return render_template('cabinet.html', current_user=current_user)
    


@app.route('/cabinet_changer',
           methods=['POST', 'GET'])  # Страница для изменения данных в личном кабинете и вноса изменений в базу данных
@login_required  # только зарегистрированный человек сможет зайти
def cabinet_changer():
    form = forms.PersonalForm()
    if form.validate_on_submit():
        user_data = db.session.query(models.Users_Data).filter_by(idUser=current_user.id).one()  # выдает строку с id 2
        user_data.name = form.name.data
        user_data.birthDAy = form.birthDAy.data
        user_data.passport = form.passport.data
        user_data.passportData = form.passportData.data
        user_data.passportBy = form.passportBy.data
        user_data.passportCod = form.passportCod.data
        user_data.nickname = form.nickname.data
        user_data.link_vk = form.link_vk.data
        user_data.inn = form.inn.data
        user_data.bank_details = form.bank_details.data
        user_data.bankName = form.bankName.data
        user_data.phone_number = form.phone_number.data

        db.session.add(user_data)
        db.session.commit()
        return redirect(url_for('cabinet'))
    return render_template('cabinet_changer.html', form=form)


@app.route('/my_tasks', methods=['GET', 'POST'])  # Страница с задачами пользователя
def my_tasks(): 
    info = models.Tasks.query.all()
    today = str(now.day) + "." + str(now.month) + "." + str(now.year)
    print(today)
    # print(list(yToken.listdir("")))
    if request.method == "POST":
        print(request.form.get("status_complete"))
        # task = models.Tass(id = id, statusCompleted = "Complete")
        # db.session.add(task)
        # db.session.commit()
    form = forms.CreateTask()
    if form.validate_on_submit(): # надо сделать завтра
        createTask = models.Tasks(idUser = form.idUser.data, idProject = form.idProject.data, 
        nameTask = form.nameTask.data,descTask = form.descTask.data,
        timeTask = form.timeTask.data,manyTask = form.manyTask.data, statusСompleted = "Uncomplete", linkDisk = form.descTask.data)
        db.session.add(createTask)
        db.session.commit()
    return render_template("my_tasks.html",form = form, list=info, today=today, now=now, current_user = current_user)


@app.route('/my_documents', methods=['GET', 'POST'])  # Страница с документами пользователя
def my_documents():
    list_yad = ()
    if yToken.check_token()==True:
        if yToken.exists("/договора/") == False:
            print('Папка отсутствует')
        elif yToken.exists("/договора/") == True:
            print(list(yToken.listdir("/договора/")))
            list_yad=list(yToken.listdir("/договора/"))

            print('Папка обнаружена')
    else:
        print("Токен не сработал")

    yToken.clear_session_cache()
    info = models.User.query.all() #Получаем словарь с содержимым таблиц user и users_Data
    return render_template("my_documents.html", current_user=current_user, yToken=yToken, list_yad=list_yad)


@app.route('/my_projects', methods=['GET', 'POST'])  # Страница с проектами шоураннера
def my_projects():
    info = {}
    # отображение проектов
    projects = models.Project.query.all()
    user_project = models.Users_Projects.query.all()
    info = models.User.query.all()
    idFin = len(projects)# получаем id последнего проекта

    if request.method == 'POST':

        listForm = request.form.to_dict()# получаем значение формы в листе
        print(listForm)
        createProjekt = models.Project(projectName = listForm['projectName'],
            descProject=listForm['descProject'],linkDisk = listForm['linkDisk']) #создание проекта
    

        iList = list(listForm.keys())
        i = 0
        while i < len(iList):
            if (i >= 3):
                db.session.commit()# создание соеденения
                update_user_projects = models.Users_Projects(User_id= iList[i], Project_id = idFin + 1)# обновления таблицы Users_project
                db.session.add(update_user_projects)# запись в базу данных users_projekt
                db.session.commit()# закрытие соеденения с бд
            i+=1

        db.session.commit()# создание соеденения
        db.session.add(createProjekt)# запись в базу данных projekt
        db.session.commit()# закрытие соеденения с бд
        return redirect(url_for('my_projects'))
    return render_template("my_projects.html", projects = projects, list = info, user_project = user_project,idFin = idFin)


@app.route('/salary', methods=['GET', 'POST'])  # Страница с зарплатами. Менеджер видит и устанавливает
def salary():
    return render_template("salary.html")


@app.route('/employeers', methods=['GET', 'POST'])  # Страница с сотрудниками компании. Доступна менеджеру
def employeers():
    return render_template("employeers.html")


@app.route('/completed_tasks', methods=['GET', 'POST'])  # Страница с выполненными задачами по людям
def completed_tasks():
    return render_template("completed_tasks.html")


@app.route('/create_contract', methods=['POST', 'GET'])
def contract():
    name = ''
    info = []
    tasks = models.Tasks.query.all()
    items = {"Работы:": {}, "Сроки:": {}, "Цена:": {}}
    id_sel = '0'
    id = 1
    info = models.User.query.all() #Получаем словарь с содержимым таблиц user и users_Data
    if request.method == 'POST':
        id_sel = request.form.get('human') # Получаем ID пользователя из html
        for i in tasks:
            if id_sel == models.Tasks.idUser:
                cells = str(models.Tasks.nameTask) + str(models.Tasks.timeTask) + str(models.Tasks.manyTask)
        id_sel = int(id_sel) - 1
        name = str(info[int(id_sel)].pr.name) # получаем имя из базы данных
        birth_date = str(info[int(id_sel)].pr.birthDAy)# Получаем дату рождения
        INN = str(info[int(id_sel)].pr.inn)#Получаем ИНН
        passport_num = str(info[int(id_sel)].pr.passport)# Получаем номер и серию паспорта
        passport_place = str(info[int(id_sel)].pr.passportBy)# Получаем место выдачи
        passport_date = str(info[int(id_sel)].pr.passportData)# Получаем дату выдачи
        passport_code = str(info[int(id_sel)].pr.passportCod)# Получаем код подразделения
        address = str(info[int(id_sel)].pr.address)# Получаем адрес
        bank_account = str(info[int(id_sel)].pr.bankAccount)# Получаем банковский счёт
        bank_name = str(info[int(id_sel)].pr.bankName)# Получаем наименование банка
        bank_details = str(info[int(id_sel)].pr.bank_details)# Получаем реквизиты банка
        email = str(info[int(id_sel)].email)# Получаем электронную почту
        section = document.sections[0]
        header = section.header
        header
        paragraph = header.paragraphs[0]
        header.is_linked_to_previous = True
        paragraph.text = "Договор подряда от" + str(now.day )+ str(now.month) + str(now.year)
        section = document.sections[0]
        footer = section.footer
        footer
        paragraph = footer.paragraphs[0]
        footer.is_linked_to_previous = True
        paragraph.text = name +  'Нечитайло Ф.К.' + "\n"\
        '_____________'	+ '_____________'
        document.add_paragraph(
    'Договор подряда' + '\n'+
    'г. Санкт-Петербург'+ '\t' + '\t' + '\t' + '\t' + '\t' + '\t' + '\t' +str(now.day )+ str(now.month) + str(now.year) + '\n'+
name + ', именуемый (-ая) в дальнейшем "Подрядчик", с одной стороны и' + '\n'+
'Индивидуальный предприниматель Нечитайло Фёдор Константинович, именуемый в дальнейшем "Заказчик", с другой стороны, а вместе именуемые "Стороны", заключили договор о нижеследующем:' +'\n'+
'1. Предмет договора' +'\n'+
'1.1. По настоящему договору Подрядчик обязуется выполнять в соответствии с согласованными в приложениях к настоящему договору заданиями Заказчика работы, и сдать результат данных работ Заказчику, а Заказчик обязуется принять результат работ и оплатить его.' +'\n'+
'1.2. Работа выполняется иждивением Подрядчика - из его материалов, его силами и средствами.' +'\n'+
'1.3. Работа выполняется Подрядчиком лично. Привлечение субподрядчиков не допускается.' +'\n'+
'1.4. Работа должна быть выполнена в срок, согласованный сторонами в приложениях к настоящему договору. Работа может быть выполнена и сдана досрочно' +'\n'+
'1.5. Работа считается выполненной после подписания Сторонами акта приема-сдачи выполненных работ.' +'\n'+
'1.6. Если иной порядок не предусмотрен в приложении к договору для конкретного вида работ, то права на результаты интеллектуальной деятельности (далее – РИД), созданные Подрядчиком при выполнении условий настоящего договора, Подрядчик обязуется передать Заказчику вместе с передачей РИД. Под отчуждением исключительного права в настоящем Договоре понимается передача исключительного права от Подрядчика Заказчику в полном объеме, без каких-либо ограничений, обременений и иных препятствий к использованию. Подрядчик с момента подписания акта приема-передачи выполненных работ теряет все исключительные права на РИД и не вправе использовать РИД самостоятельно, передавать права на РИД третьим лицам в любой форме. За Подрядчиком сохраняются личные неимущественные права и права, прямо указанные в настоящем договоре. Вознаграждение за отчуждение исключительного права на РИД включено в стоимость работ по Договору'+'\n'+
'2. Обязанности Сторон договора' +'\n'+
'2.1. Подрядчик обязуется:' +'\n'+
'2.1.1. Выполнить предусмотренные настоящим договором работы лично в соответствии с заданием Заказчика, определяющим объем, содержание работ, и со сметой, определяющей цену работ.' +'\n'+
'2.1.2. Представлять по требованию Заказчика информацию о ходе исполнения выполняемых работ.' + '\n'+
'2.1.3. Выполнить работу надлежащим образом.' +'\n'+
'2.1.4. Немедленно предупредить Заказчика и до получения от него указаний приостановить работу при обнаружении:' +'\n'+
'- непригодности или недоброкачественности технической документации, задания;' +'\n'+
'- возможных неблагоприятных для Заказчика последствий его указаний о способе исполнения работы;' +'\n'+
'- иных не зависящих от Подрядчика обстоятельств, которые грозят качеству результата выполняемой работы либо создают невозможность ее завершения в срок.' +'\n'+
'2.1.5. Передать результат выполненной работы Заказчику по акту приема-сдачи выполненных работ.' +'\n'+
'2.1.6. Передать Заказчику вместе с результатом работы информацию, касающуюся использования результата работ.' +'\n'+
'2.1.7. В случае обнаружения в выполненной работе недостатков устранить их в течение трёх календарных дней.' +'\n'+
'2.2. Подрядчик вправе:' +'\n'+
'2.2.1. Самостоятельно определять способы выполнения работы по настоящему договору.'+'\n'+
'2.3. Заказчик обязуется:'+'\n'+
'2.3.1. Предоставлять Подрядчику все документы и информацию, необходимые для выполнения Подрядчиком своих обязательств по настоящему договору.'+'\n'+
'2.3.2. Принять результат выполненной работы по акту приема-сдачи выполненных работ.'+'\n'+
'2.3.3. Своевременно оплатить выполненные работы в порядке, предусмотренном разделом 3 настоящего договора.'+'\n'+
'2.4. Заказчик вправе:'+'\n'+
'2.4.1. В любое время проверять ход и качество работы, выполняемой Подрядчиком, не вмешиваясь в его деятельность.'+'\n'+
'2.4.2. Назначить Подрядчику разумный срок для устранения недостатков в случае выявления ненадлежащего выполнения работы и при неисполнении Подрядчиком в назначенный срок этого требования отказаться от настоящего договора либо поручить исправление работ другому лицу за счет Подрядчика, а также потребовать возмещения убытков.'+'\n'+
'3. Цена работы и порядок оплаты'+'\n'+
'3.1. Цена выполняемой работы по настоящему договору определена в приложениях к настоящему договору и включает в себя компенсацию издержек подрядчика, причитающееся ему вознаграждение, а также права, предусмотренные п. 1.6. и 6.4. настоящего договора.'+'\n'+
'3.2. По настоящему договору цена работы считается твердой.'+'\n'+
'3.3. Заказчик оплачивает результат выполненной работы в течение 30 дней с момента подписания акта приема-сдачи выполненных работ.'+'\n'+
'3.4. Оплата выполненных Подрядчиком работ осуществляется путем перечисления денежных средств на банковский счет Подрядчика или иным не запрещённым законом способом по усмотрению Заказчика.'+'\n'+
'3.6. Обязанность Заказчика по оплате выполненных работ считается исполненной с даты списания денежных средств с корреспондентского счета Заказчика/даты передачи наличных денежных средств.'+'\n'+
'3.7. Подрядчик сообщает и гарантирует Заказчику, что не является плательщиком НДФЛ. В случае, если на доход Подрядчика будет начисляться НДФЛ, он обязуется сообщить об этом не позднее двух дней с момента наступления данного события, но в любом случае не позднее даты подписания акта приёма передач работ, подлежащих оплате.' +'\n'+
'Заказчик, если это применимо в соответствии с законом к правоотношениям Сторон по настоящему Договору, при выплате вознаграждения, удержит и уплатит в бюджет налог на доходы физических лиц в качестве налогового агента Подрядчика.'+'\n'+
'В случае если Подрядчик является налоговым резидентом иностранного по отношению к Российской Федерации государства, то в целях должного исполнения Заказчиком публичных обязательств в рамках действующего налогового законодательства Подрядчик предоставляет Заказчику официальный документ компетентного органа, подтверждающий статус Подрядчика в качестве налогового резидента иностранного государства для целей применения соглашения об избежании двойного налогообложения между Российской Федерацией и таким иностранным государством'+'\n'+
'В случае, если выплата вознаграждения производится на счёт Подрядчика открытый в валюте отличной от российского рубля (RUR), выплата вознаграждения производится на условиях конвертации валют обслуживающим банком, а в случае невозможности отправки вознаграждения в российских рублях (RUR), Заказчик на условиях конвертации валют обслуживающего банка вправе самостоятельно произвести перерасчёт вознаграждения в валюту, по которой возможна отправка вознаграждения Подрядчику.'+'\n'+
'Подписывая Договор, Подрядчик, если это применимо в соответствии с действующим законодательством, делает Заказчику заявление о предоставлении последним Подрядчику профессионального налогового вычета, предусмотренного ст. 221 НК РФ, полагающихся Подрядчику по Договору. Данное заявление Подрядчика действует в течение всего срока действия Договора с учетом возможных изменений в течение такого срока положений налогового законодательства России.'+'\n'+
'4. Порядок приема-сдачи работы'+'\n'+
'4.1. По окончании работ Подрядчик направляет в адрес Заказчика уведомление, после получения которого, не позднее 15 дней, Заказчик обязан осмотреть и принять выполненные работы по акту приема-сдачи выполненных работ.'+'\n'+
'4.2. Недостатки, обнаруженные в работе при ее приемке, должны быть отражены в акте приема-сдачи выполненных работ.'+'\n'+
'4.3. Заказчик, принявший работу без проверки, лишается права ссылаться на недостатки работы, которые могли быть установлены при обычном способе ее приемки (явные недостатки).'+'\n'+
'4.4. Заказчик, обнаруживший после приемки работы отступления в ней от настоящего договора или иные недостатки, которые не могли быть установлены при обычном способе приемки (скрытые недостатки), в том числе такие, которые были умышленно скрыты Подрядчиком, обязан в течение 30 дней со дня обнаружения известить об этом Подрядчика.''\n'+
'4.5. В случае возникновения между Сторонами настоящего договора спора по поводу недостатков выполненной работы или их причин, по требованию любой из Сторон должна быть назначена экспертиза. Расходы на экспертизу несет Подрядчик, за исключением случаев, когда экспертизой установлено отсутствие нарушений Подрядчиком настоящего договора или причинной связи между действиями Подрядчика и обнаруженными недостатками. В указанных случаях расходы на экспертизу несет Сторона, потребовавшая назначения экспертизы, а если она назначена по соглашению Сторон, обеими Сторонами поровну.'+'\n'+
'5. Качество работы'+'\n'+
'5.1. Результат выполненной работы должен в момент передачи Заказчику обладать свойствами, указанными в настоящем договоре или определенными обычно предъявляемыми требованиями, и в пределах разумного срока быть пригодным для установленного настоящим договором использования либо для обычного использования результата работы такого рода.'+'\n'+
'5.2. Заказчик вправе в случаях, когда работа выполнена Подрядчиком с отступлениями от настоящего договора, ухудшившими результат работы, или с иными недостатками, которые делают его не пригодным для предусмотренного в договоре использования, потребовать от Подрядчика:'+'\n'+
'- безвозмездного устранения недостатков в разумный срок;'+'\n'+
'- соразмерного уменьшения установленной за работу цены.'+'\n'+
'5.3. Подрядчик вправе вместо устранения недостатков, за которые он отвечает, безвозмездно выполнить работу заново с возмещением Заказчику причиненных просрочкой исполнения убытков. В этом случае Заказчик обязан возвратить ранее переданный ему результат работы Подрядчику.'+'\n'+
'6. Прочие условия'+'\n'+
'6.1.	В случае неисполнения или ненадлежащего исполнения своих обязательств по настоящему договору Стороны несут ответственность в соответствии с действующим законодательством Российской Федерации.'+'\n'+
'6.2.	За нарушение срока выполнения работы Подрядчик по требованию Заказчика уплачивает Заказчику штраф в размере 1% (одного процента) от стоимости выполняемой работы за каждый день просрочки.'+'\n'+
'6.3.	Подрядчик гарантирует, что факт передачи РИД не нарушает прав третьих лиц и на момент передачи не существует обстоятельств, дающих возможность третьим лицам предъявить к Заказчику претензии в отношении РИД. В случае если в связи с указанием информации, предусмотренной данным пунктом Договора, к Заказчику будут предъявлены третьими лицами какие-либо претензии / требования / иски, Подрядчик обязуется своими силами и за свой счет урегулировать их и возместить Заказчику понесенные в связи с ними убытки.'+'\n'+
'6.4.	Подрядчик не возражает против использования Заказчиком имени/творческого псевдонима/коммерческого обозначения Подрядчика. Заказчик и третьи лица с разрешения Заказчика вправе без выплаты дополнительного вознаграждения Подрядчику использовать имя (псевдоним/коммерческое обозначение) Подрядчика в любых целях (включая информационные и рекламные) и любым способом при любом использовании или популяризации результата работ, в том числе при включении результата работ в состав сложного объекта, переработки/изменения результата работ. Использование Заказчиком имени/творческого псевдонима/коммерческого обозначения Подрядчика не оплачивается Заказчиком отдельно (включено в стоимость работ).'+'\n'+
'6.5.	Настоящий договор вступает в силу с момента его подписания и действует до полного исполнения обязательств сторонами. '+'\n'+
'6.6.	Настоящий договор составлен и подписан в двух идентичных экземплярах на русском языке - по одному для каждой из Сторон. Каждая сторона подтверждает, что текст договора ею изучен и полностью понятен. Названия статей и разделов в тексте Договора приведены для удобства пользования текстом и не могут учитываться при толковании Договора и рассматриваться как что-то поясняющие или определяющие. Изменения и дополнения к договору совершаются в письменной форме и подписываются Сторонами.'+'\n'+
'6.7.	Споры и разногласия, которые могут возникнуть при исполнении настоящего договора, будут по возможности разрешаться путем переговоров и претензионной переписки между Сторонами. Срок ответа на претензию не должен превышать 15 (пятнадцати) дней с момента её получения. В случае если Стороны не придут к соглашению в рамках претензионной переписки, споры разрешаются в судебном порядке по месту нахождения Заказчика.'+'\n'+
'6.8.	Юридически значимые сообщения подлежат передаче путем доставки почтовой или курьерской службой по адресам, указанным в реквизитах сторон. Заказчик считается надлежаще уведомившим Подрядчика в случаях направления уведомления на электронную почту Подрядчика, мессенджер, связанный с номером телефона Подрядчика или путём направки сообщения на страницу социальной сети Подрядчика. Сообщение считается доставленным и в тех случаях, если оно поступило Стороне, которой оно направлено, но по обстоятельствам, зависящим от нее, не было ей вручено или Сторона не ознакомилась с ним.'+'\n'+
'6.9.	Применимым право по настоящему договору является законодательство Российской Федерации. Во всем остальном, что не предусмотрено настоящим договором, Стороны руководствуются действующим законодательством Российской Федерации. В случае, если положения настоящего договора не соответствуют положениям действующего законодательства России, договор продолжает действовать в части, не противоречащей действующему законодательству. При этом стороны обязуются согласовать и внести в договор необходимые изменения, либо иным образом в письменной форме согласовать порядок исполнения договора в течение 30 дней с момента как им станет известно о наличии противоречий между условий договора и действующим законодательством. Сторона, которой стало известно о наличии в положениях настоящего договора условий, не соответствующих положениям действующего законодательства России, обязана об этом уведомить другую сторону в письменной форме не позднее 15 дней с момента обнаружения такого противоречия.'+'\n'+
'7. Адреса и реквизиты Сторон', style='List Number')
        table = document.add_table(rows=1, cols=2) #Создаём таблицу
        hdr_cells = table.rows[0].cells #Устанавливем строку, которую планируем заполнять
        hdr_cells[0].text = "Подрядчик" + "\n" + name + "\n" + birth_date + "\n" + INN + "\n" + passport_num + "\n" + passport_place + "\n" + passport_date + "\n" + passport_code + "\n" + address + "\n" + \
                            bank_account + "\n" + bank_name + "\n" + bank_details + "\n" + email # Заполняем первую ячейку
        hdr_cells[1].text = "Заказчик:" + "\n" + "Индивидуальный предприниматель" + "\n" + "Нечитайло Фёдор Константинович" + "\n" \
            + "ИНН 616616300580 ОГРН 318619600017594" + "\n" + "Адрес: 344065, Ростовская обл., г. Ростов-на-Дону, ул. Вятская, д. 63/1, кв. 77" \
                      + "\n" + "р/с 40802810000000405802 в АО «Тинькофф Банк»" + "\n" + "кор/сч 30101810145250000974" \
                      + "\n" + "БИК 044525974" + "\n" + "fedorcomixvideo@gmail.com" # Заполняем вторую ячейку
        document.add_paragraph('Приложение № 1 ' +'\n'+
                       'г. Санкт-Петербург' + '\t' + '\t' + '\t' + '\t' + '\t' + '\t' + '\t' +str(now.day )+ str(now.month) + str(now.year) +'\n'+
                       '' +'\n'+
                       name +', именуемый (-ая) в дальнейшем "Подрядчик", с одной стороны и'+'\n'+
                       'Индивидуальный предприниматель Нечитайло Фёдор Константинович, именуемый в дальнейшем "Заказчик", с другой стороны, '+'\n'+
                       'а вместе именуемые "Стороны", составили настоящее приложение к договору подряда от' + '\t'+str(now.day )+ str(now.month) + str(now.year) +'\t'+ '(далее «Договор»)о нижеследующем:'+'\n'+
                       ''+'\n'+
                       '1.	По условиям Договора Подрядчик обязуется выполнить следующие работы: ', style='List Number')
        table = document.add_table(rows=1, cols=3) #Создаём таблицу
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Работы'
        hdr_cells[1].text = 'Срок'
        hdr_cells[2].text = 'Цена'
        for row in items:
            cells = table.add_rows().cells
            for i, item in enumerate(row):
            # вставляем данные в ячейки
                cells[i].text = str(item)
            # если последняя ячейка
                if i == 2:
            # изменим шрифт
                    cells[i].paragraphs[0].runs[0].font.name = 'Arial'
        document.add_paragraph(
            '2.	Настоящее приложение является неотъемлемой частью Договора.'+'\n'+
            '3.	Настоящее приложение вступает в силу с момента подписания Договора и действует до окончания срока действия Договора.'+'\n'+
            '4.	Термины и сокращения, используемые в настоящем приложении, понимаются в значении терминов и сокращений, используемых в Договоре.'+'\n'+
            '5.	Настоящее приложение составлено в двух идентичных экземплярах на русском языке по одному для каждой из сторон.'+'\n'+
''+'\n'+
''+'\n'+
''+'\n'+
''+'\n'+
''+'\n'+
            'АКТ СДАЧИ-ПРИЕМКИ'+'\n'+
            'к договору подряда от '+str(now.day )+ str(now.month) + str(now.year) + '\n'+
''+'\n'+
            'г. Санкт-Петербург	'+ '\t' + '\t' + '\t' + '\t' + '\t' + '\t' + '\t' + str(now.day )+ str(now.month) + str(now.year) + '\n'+
            'name, именуемый (-ая) в дальнейшем "Подрядчик", с одной стороны и'+'\n'+
            'Индивидуальный предприниматель Нечитайло Фёдор Константинович, именуемый в дальнейшем "Заказчик", с другой стороны, '+'\n'+
            'совместно также именуемые «Стороны», подписали настоящий акт сдачи-приемки (далее – «Акт») к договору подряда от '+ str(now.day )+ str(now.month) + str(now.year) + '(далее «Договор») о нижеследующем:'+'\n'+
''+'\n'+
            '1.	Подрядчик передал Заказчику результат работ, предусмотренный п. 1.1. Договора и приложением №1 к Договору, а также права на использование результата работ согласно Договора, а Заказчик настоящим подтверждает получение результата работ и прав на его использование в объеме, предусмотренном Договором. '+'\n'+
            '2.	Результат работ передан Заказчику в цифровой форме путём предоставления доступа к облачному хранилищу в сети Интернет.'+'\n'+
            '3.	Настоящий Акт подтверждает факт передачи прав использования результата работ в объемах и на условиях Договора.'+'\n'+
            '4.	Настоящий Акт является основанием для выплаты Подрядчику вознаграждения в срок и порядке, предусмотренные Договором.'+'\n'+
            '5.	Настоящий Акт является неотъемлемой частью Договора, составлен в 2 (двух) экземплярах, имеющих равную юридическую силу, по одному для каждой из Сторон.', style='List Number')
        document.save('contract.docx') #Сохраняем документ
        return redirect(url_for('cabinet'))
    return render_template('create_contract.html', name=name, id=id_sel, list=info)


@app.route('/admin', methods=['POST', 'GET'])  # Страница, доступная ЛИШЬ админу
@login_required  # только зарегистрированный человек сможет зайти
def admin():
    info = []
    info = models.User.query.all()
    tasks = models.Tasks.query.all()
    projects = models.Project.query.all()
    return render_template('admin.html', list=info, tasks=tasks, projects=projects)


# обработка ошибок
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
    # Обработчик ссылок


