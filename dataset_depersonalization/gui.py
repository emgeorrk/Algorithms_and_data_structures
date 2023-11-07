import customtkinter as ctk
from customtkinter import filedialog
import main
import pandas as pd

path = ''
non_ignore_args = []

class CustomUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CustomTKinter Example")
        self.geometry("400x300+700+340")
        self.create_widgets()
        self.toplevel_window = None


    def create_widgets(self):
        global status_label
        status_label = ctk.CTkLabel(self, text="Файл не выбран", text_color="grey")
        status_label.pack(pady=10)


        button = ctk.CTkButton(self, text="Выбрать файл", command=self.button_click)
        button.pack()

        global k_button
        k_button = ctk.CTkButton(self, text="Посчитать k-anonimity", state="disabled", command=self.open_toplevel)
        k_button.pack(pady=10)

        global dep_button
        dep_button = ctk.CTkButton(self, text="Обезличить", state="disabled", command=self.dep_func)
        dep_button.pack()

        global result_label
        result_label = ctk.CTkLabel(self, text="")
        result_label.pack(pady=10)

        exit_button = ctk.CTkButton(self, text="Выход", command = exit_func)
        exit_button.pack()

    def button_click(self):
        global path
        path = filedialog.askopenfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        print(f"path in button_click {path}")
        if path=='':
            status_label.configure(text="Выберите файл", text_color="grey")
            k_button.configure(state="disabled")
            dep_button.configure(state="disabled")
            return
        status_label.configure(text=f"Выбран файл {path}", text_color="white")
        k_button.configure(state="normal")
        dep_button.configure(state="normal")

    def dep_func(self):
        if path == '': return
        df = main.depersonalization(path)
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            writer = pd.ExcelWriter(save_path)
            df[0].index = range(1, len(df[0]) + 1)
            df[1].index = range(1, len(df[1]) + 1)
            df[0].to_excel(writer, sheet_name='ads_database1', index=True, na_rep='NaN')
            df[1].to_excel(writer, sheet_name='ads_database2', index=True, na_rep='NaN')
            writer.save()
            status_label.configure(text=f"Файл сохранен в {save_path}", text_color="green")
        else:
            status_label.configure(text=f"Операция отменена", text_color="grey")

    def k_func(self):
        if path=='': return
        k = main.count_k(path)
        result_label.configure(text=f"k = {k}", text_color="green")

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow()
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()
        self.toplevel_window.grab_set()
        print("grab set!")


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("300x300+700+340") # 266x200
        self.resizable(False, False)
        self.but = [None] * 6
        self.gen_buttons()

    def gen_buttons(self):
        columns = ["Пользователь", "Платформа", "Дата просмотра", "Кол-во рекламы", "Время просмотра рекламы", "Вид рекламы"]
        for i in range(len(columns)):
            self.but[i] = ctk.CTkCheckBox(self, text=columns[i])
            if i%2==0: self.but[i].pack(pady=10)
            else: self.but[i].pack()

        fbut = ctk.CTkButton(self, text="Посчитать", command=self.k_func)
        fbut.pack(pady=10)

    def k_func(self):
        if path == '': return
        global non_ignore_args
        non_ignore_args = []
        for x in range(len(self.but)):
            if (self.but[x].get() == 1): non_ignore_args.append(self.but[x].cget("text"))
        k = main.count_k(path, non_ignore_args)
        result_label.configure(text=f"k = {k}", text_color="green")


def exit_func():
    exit(0)
