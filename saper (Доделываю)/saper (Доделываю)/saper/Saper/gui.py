# gui.py
import tkinter.messagebox as tkMessageBox
import tkinter as Tkinter
import tkinter.simpledialog as simpledialog
from Saper.constants import *


class GUI(Tkinter.Tk):
    is_grid = False

    _time_begin = 1
    _timer_id = False

    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.title(WINDOW_TITLE)
        self.geometry("%sx%s" % (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Меню
        menubar = Tkinter.Menu(self)
        self.config(menu=menubar)

        # Меню "Файл"
        file_menu = Tkinter.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Войти как игрок", command=self.player_login)
        file_menu.add_command(label="Войти как администратор", command=self.admin_login)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        self.tk_frame_toolbar = Tkinter.Frame(self, width=WINDOW_WIDTH, height=WINDOW_TOOLBAR_HEIGHT, background="grey",
                                              relief=Tkinter.GROOVE, border=2)

        self.tk_frame_main = Tkinter.Frame(self, width=WINDOW_WIDTH, height=(WINDOW_HEIGHT - WINDOW_TOOLBAR_HEIGHT),
                                           background=WINDOW_MAIN_FRAME_COLOR_BACKGROUND, relief=Tkinter.GROOVE,
                                           border=2)

        self.tk_label_timer = Tkinter.Label(self.tk_frame_toolbar, text="0000")
        self.tk_label_timer.grid(row=0, column=0, sticky=Tkinter.NSEW)

        self.tk_label_button_new = Tkinter.Button(self.tk_frame_toolbar, text="NEW", command=self.reset_game)
        self.tk_label_button_new.grid(row=0, column=1, sticky=Tkinter.NSEW)

        self.tk_label_counter = Tkinter.Label(self.tk_frame_toolbar, text="00/00")
        self.tk_label_counter.grid(row=0, column=2, sticky=Tkinter.NSEW)

    def reset_game(self):
        if hasattr(self, 'reset_callback') and callable(self.reset_callback):
            self.reset_callback()

    def show_all_count_mine(self):
        self.tk_label_counter['text'] = "00/%2d" % MINE_COUNT

    def show_selected_count_mine(self, selected_mine):
        self.tk_label_counter['text'] = "%2d/%2d" % (selected_mine, MINE_COUNT)

    def timer_start(self):
        if not self._timer_id and self._time_begin == 1:
            self.timer()

    def timer_stop(self):
        if self._timer_id:
            self.tk_label_timer.after_cancel(self._timer_id)
            self._timer_id = False

    def timer(self):
        self.tk_label_timer['text'] = "%0004d" % self._time_begin
        self._time_begin += 1
        self._timer_id = self.tk_label_timer.after(1000, self.timer)

    def game_over(self):
        self.timer_stop()
        tkMessageBox.showerror(GAME_OVER_WINDOW_TITLE, GAME_OVER_MESSAGE)
        return False

    def game_winner(self):
        self.timer_stop()
        tkMessageBox.showinfo(WINNER_WINDOW_TITLE, WINNER_MESSAGE)
        return False

    def grid(self):
        super(GUI, self).grid()
        self.tk_frame_toolbar.grid(row=0, column=0)

        self.tk_frame_toolbar.rowconfigure('all', minsize=WINDOW_TOOLBAR_HEIGHT)

        width_label_toolbar = (float(WINDOW_WIDTH - WINDOW_TOOLBAR_HEIGHT)) / 2.0
        self.tk_frame_toolbar.columnconfigure(0, minsize=width_label_toolbar - 5)
        self.tk_frame_toolbar.columnconfigure(1, minsize=WINDOW_TOOLBAR_HEIGHT)
        self.tk_frame_toolbar.columnconfigure(2, minsize=width_label_toolbar - 5)

        self.tk_frame_main.grid(row=1, column=0)
        self.is_grid = True

    def player_login(self):
        self.player_name_dialog()

    def player_name_dialog(self):
        dialog = Tkinter.Toplevel(self)
        dialog.title("Введите имя пользователя")

        label = Tkinter.Label(dialog, text="Имя:")
        label.pack()

        name_entry = Tkinter.Entry(dialog)
        name_entry.pack()

        def save_player_name():
            player_name = name_entry.get()
            if player_name:
                self.player_name = player_name
                dialog.destroy()
                self.show()

        submit_button = Tkinter.Button(dialog, text="Войти", command=save_player_name)
        submit_button.pack()

    def admin_login(self):
        self.admin_password_dialog()

    def admin_password_dialog(self):
        dialog = Tkinter.Toplevel(self)
        dialog.title("Введите пароль администратора")

        label = Tkinter.Label(dialog, text="Пароль:")
        label.pack()

        password_entry = Tkinter.Entry(dialog, show='*')
        password_entry.pack()

        def validate_password():
            password = password_entry.get()
            if password == "123":  # Замените ADMIN_PASSWORD на реальный пароль
                dialog.destroy()
                self.admin_interface()
            else:
                tkMessageBox.showerror("Ошибка", "Неверный пароль")

        submit_button = Tkinter.Button(dialog, text="Войти", command=validate_password)
        submit_button.pack()

    def admin_interface(self):
        admin_win = Tkinter.Toplevel(self)
        admin_win.title("Администраторская панель")

        edit_game_params_button = Tkinter.Button(admin_win, text="Редактировать параметры игры", command=self.edit_game_params)
        edit_game_params_button.pack()

    def edit_game_params(self):
        params_win = Tkinter.Toplevel(self)
        params_win.title("Настройки игры")

        size_label = Tkinter.Label(params_win, text="Размер поля:")
        size_label.pack()
        size_entry = Tkinter.Entry(params_win)
        size_entry.pack()

        mines_label = Tkinter.Label(params_win, text="Количество мин:")
        mines_label.pack()
        mines_entry = Tkinter.Entry(params_win)
        mines_entry.pack()

        def save_game_params():
            new_size = int(size_entry.get())
            new_mines = int(mines_entry.get())

            print(f"Новое поле: {new_size}x{new_size}, Количество мин: {new_mines}")

            params_win.destroy()

        save_button = Tkinter.Button(params_win, text="Сохранить", command=save_game_params)
        save_button.pack()

    def show(self):
        if not self.is_grid:
            self.grid()
        self.mainloop()

