import tkinter
import sqlite3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox


task_book = Flask(__name__)
task_book.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
task_book.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(task_book)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    req_time = db.Column(db.String(50), nullable=True)
    task_link = db.Column(db.Text, nullable=False)
    task = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Tasks &r>' % self.id


def read_sqlite_table(tasks):
    count = 2
    try:
        sqlite_connection = sqlite3.connect('tasks.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """Select * from tasks"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        for row in records:
            print(row[0])
            id = row[0]
            id_list = Label(tasks, text=id, borderwidth=2, relief="groove", font=("Times New Roman", 14))
            id_list.grid(column=0, row=count, sticky=tkinter.W + tkinter.E)
            user = row[1]
            user_list = Label(tasks, text=user, borderwidth=2, relief="groove", font=("Times New Roman", 14))
            user_list.grid(column=1, row=count, sticky=tkinter.W + tkinter.E)
            req_time = row[2]
            req_time_list = Label(tasks, text=req_time, borderwidth=2, relief="groove", font=("Times New Roman", 14))
            req_time_list.grid(column=2, row=count, sticky=tkinter.W + tkinter.E)
            task_link = row[3]
            task_link_list = Label(tasks, text=task_link, borderwidth=2, relief="groove", font=("Times New Roman", 14))
            task_link_list.grid(column=3, row=count, sticky=tkinter.W + tkinter.E)
            task = row[4]
            task_list = Label(tasks, text=task, borderwidth=2, relief="groove", font=("Times New Roman", 14))
            task_list.grid(column=4, row=count, sticky=tkinter.W + tkinter.E)
            status = row[5]
            status_list = Label(tasks, text=status, borderwidth=2, relief="groove", font=("Times New Roman", 14))
            status_list.grid(column=5, row=count, sticky=tkinter.W + tkinter.E)
            count += 1

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
        return id, user, req_time, task_link, task, status


def createNewWindow():
    tasks = tkinter.Toplevel(main)
    tasks.title("Задачник. Просмотр всех задач")
    tasks.geometry('1500x400')
    lblt = Label(tasks, text="Все задачи", font=("Times New Roman", 24, "italic bold"))
    lblt.grid(column=0, row=0)
    cell1 = Label(tasks, text="ID", borderwidth=2, relief="groove", font=("Times New Roman", 20))
    cell1.grid(column=0, row=1, sticky=tkinter.W + tkinter.E)
    cell2 = Label(tasks, text="ФИО", borderwidth=2, relief="groove", font=("Times New Roman", 20))
    cell2.grid(column=1, row=1, sticky=tkinter.W + tkinter.E)
    cell3 = Label(tasks, text="Время выполнения", borderwidth=2, relief="groove", font=("Times New Roman", 20))
    cell3.grid(column=2, row=1, sticky=tkinter.W + tkinter.E)
    cell4 = Label(tasks, text="Ссылка на работу", borderwidth=2, relief="groove", font=("Times New Roman", 20))
    cell4.grid(column=3, row=1, sticky=tkinter.W + tkinter.E)
    cell5 = Label(tasks, text="Задача", borderwidth=2, relief="groove", font=("Times New Roman", 20))
    cell5.grid(column=4, row=1, sticky=tkinter.W + tkinter.E)
    cell6 = Label(tasks, text="Статус выполнения", borderwidth=2, relief="groove", font=("Times New Roman", 20))
    cell6.grid(column=5, row=1, sticky=tkinter.W + tkinter.E)
    read_sqlite_table(tasks)


def send():
    task_send = Tasks(user=user_txt.get(),
                      req_time=req_time_txt.get(),
                      task_link=task_link_txt.get(),
                      task=task_txt.get(),
                      status=status_txt.get())
    try:
        db.session.add(task_send)
        db.session.commit()
        messagebox.showinfo("Сообщение", "Отправлено")
    except:
        messagebox.showinfo("Сообщение", "Error")


def delete():
    task_delete = Tasks.query.get_or_404(celld1.get())
    try:
        db.session.delete(task_delete)
        db.session.commit()
    except:
        messagebox.showinfo("Ошибка", "Ошибка")


def var_set(id, combo, text):
    id_var=id
    combo_info_var = combo
    text_var = text
    return id_var, combo_info_var, text_var


def change():
    change_win = tkinter.Toplevel(main)
    change_win.title("Задачник. Изменение задач")
    change_win.geometry("700x300")
    id_lbl = Label(change_win, text = "Введите id записи, которую хотите изменить", font=("Times New Roman", 18))
    id_lbl.grid(column=0,row=0)
    id_change_txt = Entry(change_win, width=20)
    id_change_txt.grid(column=0, row=1,sticky=tkinter.W)
    combo_lbl = Label(change_win, text="Выберите поле для изменения:", font=("Times New Roman", 16))
    combo_lbl.grid(column=0, row=2,sticky=tkinter.W)
    combo = Combobox(change_win)
    combo['values'] = ("ФИО","Время выполнения", "Ссылка на работу", "Задача", "Статус выполнения")
    combo.current(0)
    combo.grid(column=1,row=2,sticky=tkinter.W)
    text_lbl = Label(change_win, text= "Введите новые данные:",  font=("Times New Roman", 16))
    text_lbl.grid(column=0,row=3, sticky=tkinter.W)
    text_entry = Entry(change_win, width = 50)
    text_entry.grid(column=1,row=3)
    var_set(id_change_txt.get(),combo.get(),text_entry.get())
    report_bth= Button(change_win, text="ОК", command=lambda: changeinfo(id_change_txt.get(),combo.get(),text_entry.get()), width=20,height=2)
    report_bth.grid(column=0,row=5,sticky=tkinter.W)

def changeinfo(id_var, combo, text):
    print(id_var)
    print(combo)
    print(text)

    try:
        sqlite_connection = sqlite3.connect('tasks.db')
        cursor = sqlite_connection.cursor()

        if combo == "ФИО":
            sql_update_query = """Update tasks set user = ? where id = ?"""
            data = (text, id_var)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
        elif combo == "Время выполнения":
            sql_update_query = """Update tasks set req_time = ? where id = ?"""
            data = (text, id_var)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
        elif combo == "Ссылка на работу":
            sql_update_query = """Update tasks set task_link = ? where id = ?"""
            data = (text, id_var)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
        elif combo == "Задача":
            sql_update_query = """Update tasks set task = ? where id = ?"""
            data = (text, id_var)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
        elif combo == "Статус выполнения":
            sql_update_query = """Update tasks set status = ? where id = ?"""
            data = (text, id_var)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


main = Tk()
main.title("Задачник. Добавление задачи")
main.geometry('800x350')
id_var = tkinter.StringVar()
combo_info_var = tkinter.StringVar()
text_var = tkinter.StringVar()
lbl = Label(main, text="Добавить задачу", font=("Times New Roman", 24))
lbl.grid(column=0, row=0)
tasks_button=Button(main,text="Все задачи", command=createNewWindow, width=20, height=2)
tasks_button.grid(column=1, row=0)
lbl1 = Label(main, text="ФИО", font=("Times New Roman", 20))
lbl1.grid(column=0, row=1)
user_txt = Entry(main, width=30)
user_txt.grid(column=1,row=1)
lbl2 = Label(main, text="Время выполнения", font=("Times New Roman", 20))
lbl2.grid(column=0, row=2)
req_time_txt = Entry(main, width=30)
req_time_txt.grid(column=1,row=2)
lbl3 = Label(main, text="Ссылка на задачу", font=("Times New Roman", 20))
lbl3.grid(column=0, row=3)
task_link_txt = Entry(main, width=30)
task_link_txt.grid(column=1,row=3)
lbl4 = Label(main, text="Задача", font=("Times New Roman", 20))
lbl4.grid(column=0, row=4)
task_txt = Entry(main, width=30)
task_txt.grid(column=1,row=4)
lbl5 = Label(main, text="Статус выполнения", font=("Times New Roman", 20))
lbl5.grid(column=0, row=5)
status_txt = Entry(main, width=30)
status_txt.grid(column=1,row=5)
entry_btn=Button(main,text="Отправить в базу данных", command=send, width=20, height=2)
entry_btn.grid(column=0, row=6)
change_btn=Button(main, text = "Изменение записей", command=change, width = 20, height = 2)
change_btn.grid(column=0, row=7)
lbld1 = Label(main, text="Введите ID", font=("Times New Roman", 20))
lbld1.grid(column=0,row=8)
celld1 = Entry(main, text="ID", borderwidth=2, relief="groove", font=("Times New Roman", 20))
celld1.grid(column=1, row=8)
delete_btn = Button(main, text = "Удаление записей", command=delete, width = 20, height = 2)
delete_btn.grid(column=2, row=8)
main.mainloop()