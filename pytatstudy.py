from tkinter import Tk, Frame, Menu, StringVar, Label, Radiobutton, Button
from tkinter import ttk
import sqlite3
import random


class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.conn = sqlite3.connect('tatardict.db')  # Подключаемся к базе
        self.curdict = self.conn.cursor()

        self.master.title('Татарский язык')
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.fileMenu = Menu(self.menubar)
        self.nfm = Menu(self.menubar)
        self.tfm = Menu(self.menubar)
        self.fileMenu.add_cascade(label="Выбор темы", menu=self.tfm)
        self.curdict.execute('SELECT sub_them, in_them FROM themes')
        th = self.curdict.fetchall()

        self.choice_them = StringVar()
        for text, mode in th:
            self.tfm.add_radiobutton(label=text,
                                     value=mode,
                                     variable=self.choice_them,
                                     command=self.choise_theme)
        self.choice_them.set(2)

        self.fileMenu.add_command(label="Выход", command=self.onExit)
        self.menubar.add_cascade(label="≡", menu=self.fileMenu)

        self.them = Label(self.master, text='Тема: ' +
                          self.tfm.entrycget(self.choice_them.get(), 'label'),
                          bd=1, relief='flat', anchor='w')
        self.them.grid(row=1, column=0, columnspan=2)
        self.question = Label(self.master, text=' ', font=('BOLD', 12),
                              fg='red')
        self.question.grid(row=2, column=0, columnspan=4)

        ttk.Separator(self.master, orient='horizontal').grid(row=3,
                                                             column=0,
                                                             columnspan=2,
                                                             sticky='ew')
        answer_width = 15  # Ширина кнопок ответа

        self.v = StringVar()  # Выбранный ответ радиокнопкой
        self.var = StringVar()  # Строка состояния 'предыдущий ответ
        self.var1 = StringVar()      # Подсчет количества выполненных ответов
        self.var1.set('0/0')
        self.rightanswer = 0
        self.allanswer = 0

        self.b1 = Radiobutton(self.master,
                              text='',
                              variable=self.v,
                              value='',
                              indicatoron=0,
                              width=answer_width)
        self.b2 = Radiobutton(self.master,
                              text='',
                              variable=self.v,
                              value='',
                              indicatoron=0,
                              width=answer_width)
        self.b3 = Radiobutton(self.master,
                              text='',
                              variable=self.v,
                              value='',
                              indicatoron=0,
                              width=answer_width)
        self.b4 = Radiobutton(self.master,
                              text='',
                              variable=self.v,
                              value='',
                              indicatoron=0,
                              width=answer_width)
        self.b5 = Radiobutton(self.master,
                              text='',
                              variable=self.v,
                              value='',
                              indicatoron=0,
                              width=answer_width)
        self.b1.grid(row=4, column=0, columnspan=4)
        self.b2.grid(row=5, column=0, columnspan=4)
        self.b3.grid(row=6, column=0, columnspan=4)
        self.b4.grid(row=7, column=0, columnspan=4)
        self.b5.grid(row=8, column=0, columnspan=4)

        self.NextButton = Button(self.master,
                                 text='Дальше',
                                 command=self.next_question).grid(row=9,
                                                                  column=1,
                                                                  columnspan=3,
                                                                  sticky='e')

        self.status = Label(self.master,
                            text='Предыдущий ответ: ',
                            bd=1,
                            relief='sunken',
                            width=18,
                            anchor='w').grid(row=10,
                                             column=0)
        self.status1 = Label(self.master,
                             text='Не было!',
                             textvariable=self.var,
                             bd=1,
                             relief='sunken',
                             width=10,
                             anchor='w').grid(row=10,
                                              column=1)
        self.status2 = Label(self.master,
                             text=' Количество вопросов: ',
                             bd=1,
                             relief='sunken',
                             width=18,
                             anchor='e').grid(row=11,
                                              column=0,
                                              sticky='w')
        self.status3 = Label(self.master,
                             textvariable=self.var1,
                             bd=1,
                             relief='sunken',
                             width=10,
                             anchor='w').grid(row=11,
                                              column=1)
        self.choise_theme()

    # Определение правильности ответа, переход на следующий вопрос
    def next_question(self):
        if self.question['text'] == self.v.get():
            self.var.set('правильный')
            self.rightanswer += 1
        else:
            self.var.set('не верный')
        self.allanswer += 1
        self.var1.set(str(self.allanswer) + '/' + str(self.rightanswer))
        self.create_question()

    # Выбор темы
    def choise_theme(self):
        choices_them = self.tfm.entrycget(self.choice_them.get(), 'label')
        self.them["text"] = 'Тема: ' + choices_them
        dbselect = 'SELECT tatar, orys FROM dictionary where in_themes = '
        self.curdict.execute(dbselect + self.choice_them.get())
        self.f = self.curdict.fetchall()
        self.create_question()

    # Создаем вопрос
    def create_question(self):
        self.ff = random.choice(self.f)
        # Предотвращаем повторяемость вопросов
        if 'oldword' in locals():
            while self.ff == oldword:
                self.ff = random.choice(self.f)
        self.f.remove(self.ff)
        self.fff = random.sample(self.f, 4)
        self.fff.append(self.ff)
        random.shuffle(self.fff)
        self.question['text'] = self.ff[1]
        self.result = self.ff[0]
        self.b1["text"] = self.fff[0][0]
        self.b1["value"] = self.fff[0][1]
        self.b2["text"] = self.fff[1][0]
        self.b2["value"] = self.fff[1][1]
        self.b3["text"] = self.fff[2][0]
        self.b3["value"] = self.fff[2][1]
        self.b4["text"] = self.fff[3][0]
        self.b4["value"] = self.fff[3][1]
        self.b5["text"] = self.fff[4][0]
        self.b5["value"] = self.fff[4][1]
        self.f.append(self.ff)
        oldword = self.ff  # Сохраняем предыдущий ответ

    def onExit(self):
        self.master.destroy()


def main():

    root = Tk()
    root.geometry('205x230+310+210')
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()
