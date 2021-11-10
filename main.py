from tkinter import *
from tkinter import messagebox
import sqlite3

def autorization():

    window = Tk()
    window.title('Авторизация')
    window.geometry('450x230')
    window.resizable(False, False)

    val = StringVar()

    font_header = ('Arial', 15)
    font_entry = ('Arial', 12)
    label_font = ('Arial', 11)
    base_padding = {'padx': 10, 'pady': 8}
    header_padding = {'padx': 10, 'pady': 12}

    conn = sqlite3.connect('lp.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin")
    inf = cur.fetchall()
    mass_1 = []
    mass_2 = []
    for i in inf:
        login = i[0]
        mass_1.append(login)
    for j in inf:
        password = j[1]
        mass_2.append(password)

    main_label = Label(window, text='Авторизация пользователя', font=font_header, justify=CENTER, **header_padding)
    main_label.pack()

    username_label = Label(window, text='Логин', font=label_font, **base_padding)
    username_label.pack()

    username_entry = Entry(window, bg='#fff', fg='#444', font=font_entry)
    username_entry.pack()

    password_label = Label(window, text='Пароль', font=label_font, **base_padding)
    password_label.pack()

    password_entry = Entry(window, bg='#fff', fg='#444', font=font_entry)
    password_entry.pack()

    def clicked():
        username = username_entry.get()
        password = password_entry.get()

        a = 0
        for i in range(len(mass_1)):
            login = mass_1[i]
            if str(login) == str(username):
                a = a + 1
        if a == 0:
            messagebox.showinfo('Error', 'Неверный логин')

        for i in range(len(mass_1)):
            login = mass_1[i]
            if str(login) == str(username):
                pas = mass_2[i]
                if str(pas) == str(password):
                    window.destroy()
                    mainWindow(val)
                else:
                    messagebox.showinfo('Error', 'Неверный пароль')

    send_btn = Button(window, text='Войти', bg="gray", command=clicked)
    send_btn.pack(**base_padding)

    #btn = Button(window, text='Войти', bg="gray", command=clicked)
    #btn.place(x=380, y=178)

    window.mainloop()

def mainWindow(val_):

    window_2 = Tk()
    window_2.title('')
    window_2.geometry('900x460')
    window_2.resizable(False, False)

    window_2.mainloop()

















if __name__ == '__main__':
    autorization()