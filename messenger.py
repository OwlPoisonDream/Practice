from flask import render_template
from flask_login import login_required


class Models_py:
    class Chat(db.Model):
        __tablename__ = "chat"
        
        id = db.Column(db.Integer, primary_key=True)#id чата
        emp_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        showrunner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
        name = db.Column(db.String(50), nullable=True)
        
    class Message(db.Model):
        __tablename__ = "message"
        
        id = db.Column(db.Integer, primary_key = True)
        chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
        mes_time = db.Column(db.String(255))
        mes_text = db.Column(db.Text)
        mes_owner = db.Column(db.String(255))
        
class Forms_py(FlaskForm):
    class Message_Form:
        message_Text= StringField(validators=[], render_kw={"placeholder": "Текст сообщения"})
        message_file = FileField(validators=[])
        submit = SubmitField('Отправить сообщение')
        
        
class templates:
    class Messenger:
        <script type='text/javascript'>
            // Стандарный input для файлов
            var fileInput = $('#file-field');
    
            // ul-список, содержащий миниатюрки выбранных файлов
            var imgList = $('ul#img-list');

            // Контейнер, куда можно помещать файлы методом drag and drop
            var dropBox = $('#img-container');

            // Обработка события выбора файлов в стандартном поле
            fileInput.bind({
                change: function() {
                displayFiles(this.files);
                }
            });
                
            // Обработка событий drag and drop при перетаскивании файлов на элемент dropBox
            dropBox.bind({
                dragenter: function() {
                $(this).addClass('highlighted');
                return false;
                },
                dragover: function() {
                return false;
                },
                dragleave: function() {
                $(this).removeClass('highlighted');
                return false;
                },
                drop: function(e) {
                var dt = e.originalEvent.dataTransfer;
                displayFiles(dt.files);
                return false;
                }
            });
                function displayFiles(files) {
                    // Создаем элемент li и помещаем в него название, миниатюру и progress bar,
                    // а также создаем ему свойство file, куда помещаем объект File (при загрузке понадобится)
                    var li = $('<li/>').appendTo(imgList);
                    $('<div/>').text(file.name).appendTo(li);
                    var img = $('<img/>').appendTo(li);
                    $('<div/>').addClass('progress').text('0%').appendTo(li);
                    li.get(0).file = file;
            
                    // Создаем объект FileReader и по завершении чтения файла, отображаем миниатюру и обновляем
                    // инфу обо всех файлах
                    var reader = new FileReader();
                    reader.onload = (function(aImg) {
                    return function(e) {
                        aImg.attr('src', e.target.result);
                        aImg.attr('width', 150);
                        /* ... обновляем инфу о выбранных файлах ... */
                    };
                    })(img);
                    
                    reader.readAsDataURL(file);
                }
                
                function uploadFile(file, url) {
                
                    var reader = new FileReader();
                
                    reader.onload = function() {    
                    var xhr = new XMLHttpRequest();    
                    
                    xhr.upload.addEventListener("progress", function(e) {
                        if (e.lengthComputable) {
                        var progress = (e.loaded * 100) / e.total;
                        /* ... обновляем инфу о процессе загрузки ... */
                        }
                    }, false);
                    
                    /* ... можно обрабатывать еще события load и error объекта xhr.upload ... */
                
                    xhr.onreadystatechange = function () {
                        if (this.readyState == 4) {
                        if(this.status == 200) {
                            /* ... все ок! смотрим в this.responseText ... */
                        } else {
                            /* ... ошибка! ... */
                        }
                        }
                    };
                    
                    xhr.open("POST", url);
                    var boundary = "xxxxxxxxx";    
                    // Устанавливаем заголовки
                    xhr.setRequestHeader("Content-Type", "multipart/form-data, boundary="+boundary);
                    xhr.setRequestHeader("Cache-Control", "no-cache");    
                    // Формируем тело запроса
                    var body = "--" + boundary + "\r\n";
                    body += "Content-Disposition: form-data; name='myFile'; filename='" + file.name + "'\r\n";
                    body += "Content-Type: application/octet-stream\r\n\r\n";
                    body += reader.result + "\r\n";
                    body += "--" + boundary + "--";
                
                    if(xhr.sendAsBinary) {
                        // только для firefox
                        xhr.sendAsBinary(body);
                    } else {
                        // chrome (так гласит спецификация W3C)
                        xhr.send(body);
                    }
                    };
                    // Читаем файл
                    reader.readAsBinaryString(file);
                }
            </script>
            
        <div class="chat_name">
            {{chat.name}}
        </div>
        <div class="messages">
        {% for u in messages %}
        {% if u.chat_id == chat.id %}
            <p>
            {{u.mes_time}} {{u.mes_owner}}
            {{u.mes_text}}
            </p>
            {% endif %}
            {% endfor %}
        </div>
        <div class="message_form">
        {{form.message_Text}}
        {{form.message_file}}
        {{form.submit}}
        </div>

class Views_py:
    @app.route('messenger/<task>/', methods=['GET', 'POST'])
    @login_required
    def messanger(who, task):
        form = forms.Message_Form()
        user = models.User.query.filter_by(id = who).first()
        task = models.Task.query.filter_by(idUser = who).first()
        chat = models.Chat.query.filter_by(id = task.id)
        messages = models.Message.query.filter_by(id=chat.id)
        
        if form.validate_on_submit():
            if form.message_text.data and form.message_text.data.strip() and form.message_text.data != None :
                message_text = form.message_text.data

            if form.message_file.data != None :
                try:
                    # загрузка фото
                    f = form.message_file.data
                    filename = secure_filename(f.filename)
                    way = Config.way_file + task.name# указываю путь к папке
                    if not os.path.isdir(way):
                        os.mkdir(way)# создаю папку
                    if os.path.isfile(Config.way_file + task.name):# удаляем старый файл если он есть
                        os.remove(Config.way_file + task.name)
                    f.save(os.path.join(
                        way, filename))# сохранения файла
                except FileNotFoundError:
                    return render_template('messenger.html',error="ошибка с сервером")
            if form.message_file.data != None :
                message_file = Config.way_file + + task.name + '/'+ filename # указываю путь к папке
        return render_template("messenger.html", task=task, user=user, messages=messages, chat=chat)