from datetime import datetime, timedelta
import random
import string
import time
import pandas as pd
import io
import customtkinter as ctk
from customtkinter import filedialog

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def generate_alphanum_random_string(length) -> str:
    letters_and_digits = string.ascii_lowercase + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string

def get_season(date) -> str:
    if date.month >= 3 and date.month <= 5: return 'Spring'
    elif date.month >= 6 and date.month <= 8: return 'Summer'
    elif date.month >= 9 and date.month <= 11: return 'Fall'
    else: return 'Winter'

def generate_data():
    status_label.configure(text=f"В процессе...", text_color="yellow")
    N = N_entry.get()
    str_begin_date = begin_date_entry.get()
    str_end_date = end_date_entry.get()
    multiplier = multiplier_entry.get()

    try:
        temp_var = int(N)
        N_entry.configure(fg_color=default_fg)
    except:
        if N == "": N_entry.configure(fg_color=default_fg)
        else: N_entry.configure(fg_color="red")

    try:
        temp_str = datetime.strptime(str_begin_date, '%d.%m.%Y')
        begin_date_entry.configure(fg_color=default_fg)
    except:
        if str_begin_date == "": begin_date_entry.configure(fg_color=default_fg)
        else: begin_date_entry.configure(fg_color="red")

    try:
        temp_str = datetime.strptime(str_end_date, '%d.%m.%Y')
        end_date_entry.configure(fg_color=default_fg)
    except:
        if str_end_date == "": end_date_entry.configure(fg_color=default_fg)
        else: end_date_entry.configure(fg_color="red")

    try:
        temp_var = int(multiplier)
        multiplier_entry.configure(fg_color=default_fg)
    except:
        if multiplier == "": multiplier_entry.configure(fg_color=default_fg)
        else: multiplier_entry.configure(fg_color="red")

    try:
        if N != "": N = int(N)
        else: N = 100

        if str_begin_date != "": begin_date = datetime.strptime(str_begin_date, '%d.%m.%Y')
        else:
            str_begin_date = "01.01.2000"
            begin_date = datetime.strptime(str_begin_date, '%d.%m.%Y')

        if str_end_date != "": end_date = datetime.strptime(str_end_date, '%d.%m.%Y')
        else:
            str_end_date = "31.12.2020"
            end_date = datetime.strptime(str_end_date, '%d.%m.%Y')

        if multiplier != "": multiplier = int(multiplier)
        else: multiplier = random.randint(20, 360)

        # Getting platforms dictionary
        platforms = open("platforms.txt").readlines()
        for i in range(len(platforms)):
            platforms[i] = platforms[i].strip()

        platforms_random = [None] * N
        for i in range(N):
            platforms_random[i] = platforms[random.randint(0, len(platforms) - 1)]

        # Getting the list of domains
        domains = open("domains.txt").readlines()
        for i in range(len(domains)):
            domains[i] = domains[i].strip()

        # Generating random emails
        emails = set()
        while len(emails) < N:
            email_address = (generate_alphanum_random_string(random.randint(5, 25))
                             + '@' + domains[random.randint(0, len(domains) - 1)])
            emails.add(email_address)

        # Generating IP-address
        ip_addresses = set()
        while (len(ip_addresses) < N):
            ip = (str(random.randint(0, 255)) + '.' + str(random.randint(0, 255))
                  + '.' + str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)))
            ip_addresses.add(ip)

        # Generating the number of ads
        number_of_ads = [None] * N
        for i in range(len(number_of_ads)):
            number_of_ads[i] = random.randint(1, 100)

        # Generating the date of view
        date_of_view = [None] * N
        for i in range(len(date_of_view)):
            delta = end_date - begin_date
            date_of_view[i] = begin_date + timedelta(random.randint(0, delta.days))

        # Generating time of view
        time_of_view = [None] * N
        for i in range(len(time_of_view)):
            time_of_view[i] = time.strftime("%H:%M:%S", time.gmtime(number_of_ads[i] * multiplier))

        # Getting the types of ad
        types_of_ad = {}
        seasons = ['Winter', 'Spring', 'Summer', 'Fall']
        for x in seasons:
            types_of_ad[x] = []
        ads = io.open("types_of_ad.txt", encoding='utf-8').readlines()
        k = 0
        for el in ads:
            if el.strip() == '---':
                k += 1
            else:
                types_of_ad[seasons[k]].append(el.strip())

        ad_type = [None] * N
        for i in range(N):
            ad_type[i] = types_of_ad[get_season(date_of_view[i])][
                random.randint(0, len(types_of_ad[get_season(date_of_view[i])]) - 1)]

        # Deleting hours, minutes and seconds from date of view
        for i in range(len(date_of_view)):
            date_of_view[i] = str(date_of_view[i]).split(' ')[0]

        # Output in CSV file
        df = pd.DataFrame({
            'Пользователь': list(emails),
            'IP адрес': list(ip_addresses),
            'Платформа': platforms_random,
            'Дата просмотра': date_of_view,
            'Кол-во рекламы': number_of_ads,
            'Время просмотра рекламы': time_of_view,
            'Вид рекламы': ad_type
        })

        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            writer = pd.ExcelWriter(save_path)
            df.index = range(1, len(df) + 1)
            df.to_excel(writer, sheet_name='ads_database', index=True, na_rep='NaN')

            # Adjust columns' width
            for column in df:
                column_width = len(column)
                if (column == 'Дата просмотра' or column == 'Кол-во рекламы' or column == 'Платформа'):
                    column_width = max(column_width, 15)
                elif (column == 'Время просмотра рекламы'):
                    column_width = max(column_width, 25)
                elif (column == 'Пользователь'):
                    column_width = max(column_width, 45)
                elif (column == 'IP адрес'):
                    column_width = max(column_width, 16)
                elif (column == 'Вид рекламы'):
                    column_width = max(column_width, 60)
                col_idx = df.columns.get_loc(column)
                writer.sheets['ads_database'].set_column(col_idx + 1, col_idx + 1, column_width)

            writer.save()
            status_label.configure(text=f"Файл сохранен в {save_path}", text_color="green")
        else:
            status_label.configure(text=f"Операция отменена", text_color="grey")
    except:
        status_label.configure(text=f"Ошибка", text_color="red")


def end_func():
    exit(0)

if __name__ == '__main__':
    # Create the main window
    window = ctk.CTk()
    window.title("Ad Data Generator")
    window.resizable(False, False)
    window.geometry("410x270+700+340")

    # Create and place GUI components
    N_label = ctk.CTkLabel(window, text="Количество строк:", )
    N_label.grid(column=0, row=0, padx=10, pady=5)
    N_entry = ctk.CTkEntry(window, placeholder_text="100")
    N_entry.grid(column=1, row=0, padx=10, pady=5)

    begin_date_label = ctk.CTkLabel(window, text="Дата начала:")
    begin_date_label.grid(column=0, row=1, padx=10, pady=5)
    begin_date_entry = ctk.CTkEntry(window, placeholder_text="01.01.2000")
    default_fg = begin_date_entry.cget("fg_color")
    begin_date_entry.grid(column=1, row=1, padx=10, pady=5)

    end_date_label = ctk.CTkLabel(window, text="Дата конца:")
    end_date_label.grid(column=0, row=2, padx=10, pady=5)
    end_date_entry = ctk.CTkEntry(window, placeholder_text="31.12.2020")
    end_date_entry.grid(column=1, row=2, padx=10, pady=5)

    multiplier_entry_label = ctk.CTkLabel(window, text="Коэффицент для времени просмотра:")
    multiplier_entry_label.grid(column=0, row=4, padx=10, pady=5)
    multiplier_entry = ctk.CTkEntry(window, placeholder_text="Автоматически")
    multiplier_entry.grid(column=1, row=4, padx=10, pady=5)

    generate_button = ctk.CTkButton(window, text="Сгенерировать", command=generate_data)
    generate_button.grid(column=0, row=5, columnspan=2, pady=5)

    exit_button = ctk.CTkButton(window, text="Выход", command=end_func)
    exit_button.grid(column=0, row=6, columnspan=3, pady=5)

    status_label = ctk.CTkLabel(window, text="")
    status_label.grid(column=0, row=7, columnspan=2, pady=5)

    # Start the GUI event loop
    window.mainloop()