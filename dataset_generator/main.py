import io
import random
import string
import time
from datetime import datetime, timedelta
import pandas as pd


def generate_alphanum_random_string(length) -> str:
    letters_and_digits = string.ascii_lowercase + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string

def get_season(date) -> str:
    if date.month >= 3 and date.month <= 5: return 'Spring'
    elif date.month >= 6 and date.month <= 8: return 'Summer'
    elif date.month >= 9 and date.month <= 11: return 'Fall'
    else: return 'Winter'

if __name__ == '__main__':
    # Getting the number of rows
    print('N = ', end = '')
    N = int(input())

    print('Begin date: ', end = '')
    str_begin_date = str(input())
    begin_date = datetime.strptime(str_begin_date, '%d.%m.%Y')

    print('End date: ', end = '')
    str_end_date = str(input())
    end_date = datetime.strptime(str_end_date, '%d.%m.%Y')

    print('Generate time of view automatically?: ', end = '')
    flag = int(input())
    if (flag == 0):
        print('Multiplier = ', end = '')
        multiplier = int(input())

    # Getting platforms dictionary
    platforms = open("platforms.txt").readlines()
    for i in range(len(platforms)):
        platforms[i] = platforms[i].strip()

    platforms_random = [None]*N
    for i in range(N):
        platforms_random[i] = platforms[random.randint(0, len(platforms)-1)]

    # Getting the list of domains
    domains = open("domains.txt").readlines()
    for i in range(len(domains)):
        domains[i] = domains[i].strip()

    # Generating random emails
    emails = set()
    while len(emails) < N:
        email_address = (generate_alphanum_random_string(random.randint(5, 25))
                         + '@' + domains[random.randint(0, len(domains)-1)])
        emails.add(email_address)

    # Generating IP-address
    ip_addresses = set()
    while (len(ip_addresses) < N):
        ip = (str(random.randint(0, 255)) + '.' +str(random.randint(0, 255))
         + '.'+str(random.randint(0, 255)) + '.' +str(random.randint(0, 255)))
        ip_addresses.add(ip)

    # Generating the number of ads
    number_of_ads = [None]*N
    for i in range(len(number_of_ads)):
        number_of_ads[i] = random.randint(1, 100)

    # Generating the date of view
    date_of_view = [None]*N
    for i in range(len(date_of_view)):
        delta = end_date - begin_date
        date_of_view[i] = begin_date + timedelta(random.randint(0, delta.days))

    # Generating time of view
    time_of_view = [None]*N
    for i in range(len(time_of_view)):
        if (flag == 1):
            time_of_view[i] = time.strftime("%H:%M:%S", time.gmtime(number_of_ads[i] * random.randint(20, 360)))
        else:
            time_of_view[i] = time.strftime("%H:%M:%S", time.gmtime(number_of_ads[i] * multiplier))

    # Getting the types of ad
    types_of_ad = {}
    seasons = ['Winter', 'Spring', 'Summer', 'Fall']
    for x in seasons:
        types_of_ad[x] = []
    ads = io.open("types_of_ad.txt", encoding='utf-8').readlines()
    k = 0
    for el in ads:
        if el.strip() == '---': k+=1
        else: types_of_ad[seasons[k]].append(el.strip())

    ad_type = [None]*N
    for i in range(N):
        ad_type[i] = types_of_ad[get_season(date_of_view[i])][random.randint(0, len(types_of_ad[get_season(date_of_view[i])])-1)]

    # Deleting hours, minutes and seconds from date of view
    for i in range(len(date_of_view)):
        date_of_view[i] = str(date_of_view[i]).split(' ')[0]

    # Output in CSV file
    df = pd.DataFrame({
        'Пользователь': list(emails),
        'IP адрес' : list(ip_addresses),
        'Платформа' : platforms_random,
        'Дата просмотра' : date_of_view,
        'Кол-во рекламы' : number_of_ads,
        'Время просмотра рекламы' : time_of_view,
        'Вид рекламы' : ad_type
    })
    writer = pd.ExcelWriter('output.xlsx')
    df.index = range(1, len(df) + 1)
    df.to_excel(writer, sheet_name='ads_databse', index=True, na_rep='NaN')

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
        writer.sheets['ads_databse'].set_column(col_idx+1, col_idx+1, column_width)

    writer.save()
