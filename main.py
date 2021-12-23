from random import shuffle
import tkinter as tk
from tkinter import messagebox
import sqlite3


colors = {
    0: '#000000',
    1: '#0000ff',
    2: '#0cc20b',
    3: '#ea9579',
    4: '#472577',
    5: '#f1a8a4',
    6: '#046b32',
    7: '#f889b5',
    8: '#65233e'
}


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font=MineSweeper.font_b, *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton{self.x} {self.y} {self.number} {self.is_mine}'


class MineSweeper:

    window = tk.Tk()
    window.title('Сапер')
    window.iconbitmap("rolling-bomb_38138.ico")
    ROW = 10
    COLUMNS = 10
    MINES = 15
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True
    font_b = ('Arial', 12)
    window.withdraw()

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROW+2):
            temp = []
            for j in range(MineSweeper.COLUMNS+2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button-3>", self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def autorization(self):

        window_2 = tk.Tk()
        window_2.title('Авторизация')
        window_2.geometry('450x230')
        window_2.resizable(False, False)

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

        main_label = tk.Label(window_2, text='Авторизация пользователя', font=font_header, **header_padding)
        main_label.pack()

        username_label = tk.Label(window_2, text='Логин', font=label_font, **base_padding)
        username_label.pack()

        username_entry = tk.Entry(window_2, bg='#fff', fg='#444', font=font_entry)
        username_entry.pack()

        password_label = tk.Label(window_2, text='Пароль', font=label_font, **base_padding)
        password_label.pack()

        password_entry = tk.Entry(window_2, bg='#fff', fg='#444', font=font_entry)
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
                        window_2.destroy()
                        MineSweeper.window.deiconify()
                        self.start()
                    else:
                        messagebox.showinfo('Error', 'Неверный пароль')

        btn_1 = tk.Button(window_2, text='Войти', bg="gray", command=clicked)
        btn_1.pack(**base_padding)

        window_2.mainloop()

    def right_click(self, event):
        if MineSweeper.IS_GAME_OVER:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '?'
            cur_btn['disabledforeground'] = 'red'
        elif cur_btn['text'] == '?':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'

    def click(self, clicked_button: MyButton):

        if MineSweeper.IS_GAME_OVER:
            return None

        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_btn()
            MineSweeper.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            messagebox.showinfo('Game over', 'Вы проиграли!')
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROW and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False

    def create_set_win(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')
        tk.Label(win_settings, text='Количество строк:').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, MineSweeper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количество колонок:').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, MineSweeper.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количество мин:').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, MineSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        save_btn = tk.Button(win_settings, text='Применить',
                  command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            messagebox.showerror('Ошибка', 'Вы ввели неправильное значение!')
            return
        MineSweeper.ROW = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_set_win)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=settings_menu)

        count = 1
        for i in range(1, MineSweeper.ROW+1):
            for j in range(1, MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')
                count += 1

        for i in range(1, MineSweeper.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
        for i in range(1, MineSweeper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def open_all_buttons(self):
        for i in range(MineSweeper.ROW+2):
            for j in range(MineSweeper.COLUMNS+2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", background='red', disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        self.create_widgets()


    def print_btn(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    def mines_places(self, exclude_number: int):
        indx = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        indx.remove(exclude_number)
        shuffle(indx)
        return indx[:MineSweeper.MINES]

    def insert_mines(self, number: int):
        indx_mines = self.mines_places(number)
        for i in range(1, MineSweeper.ROW+1):
            for j in range(1, MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                if btn.number in indx_mines:
                    btn.is_mine = True

    def count_mines_in_buttons(self):
        for i in range(1, MineSweeper.ROW+1):
            for j in range(1, MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    # вложенные циклы
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i+row_dx][j+col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb


game = MineSweeper()
game.autorization()

