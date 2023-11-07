import pandas as pd
import gui

def get_dataset(path):
    tab1 = pd.read_excel(f"{path}", sheet_name="ads_database1")
    tab2 = pd.read_excel(f"{path}", sheet_name="ads_database2")
    del tab1['Unnamed: 0']  # Delete the index column
    del tab2['Unnamed: 0']
    del tab2['Дата просмотра']
    tab = pd.concat([tab1, tab2], axis=1)
    return tab

def get_season(date) -> str:
    if date.split('-')[1] in ('03', '04', '05'):
        return 'Весна'
    elif date.split('-')[1] in ('06', '07', '08'):
        return 'Лето'
    elif date.split('-')[1] in ('09', '10', '11'):
        return 'Осень'
    else:
        return 'Зима'


def depersonalization(path):
    tab = pd.read_excel(f"{path}")
    del tab['Unnamed: 0']
    emails = tab['Пользователь'].to_numpy()  # Leave only the domain
    platform = tab['Платформа'].to_numpy()  #
    date = tab['Дата просмотра'].to_numpy()  # Leave only the year and month
    number = tab['Кол-во рекламы'].to_numpy()  # Leave only tens
    time = tab['Время просмотра рекламы'].to_numpy()  # Leave only minutes
    type = tab['Вид рекламы'].to_numpy()  # Do not edit

    videohostings = open("videohostings.txt").readlines()
    for i in range(len(videohostings)):
        videohostings[i] = videohostings[i].strip()

    # for i in range(len(platform)):
    #     if platform[i] in videohostings:
    #         platform[i] = 'Видеохостинг'
    #     else:
    #         platform[i] = 'Социальная сеть'

    for i in range(len(emails)):
        # emails[i] = '*****@***.' + emails[i].split('.')[1]
        emails[i] = '****@' + emails[i].split('@')[1]

    for i in range(len(date)):
        season = get_season(date[i])
        date[i] = season + ' ' + date[i].split('-')[0]

    numbers_out = []
    for i in range(len(number)):
        min_num = int(number[i]) // 30
        if min_num == 0:
            numbers_out.append(str(1) + '-' + str(30))
        else:
            mx_num = min_num + 1
            min_num *= 30
            numbers_out.append(str(min_num) + '-' + str(mx_num * 30))

    for i in range(len(time)):
        hours = time[i].split(':')[0]
        minutes = time[i].split(':')[1]
        if minutes == '00': minutes = '01'
        if hours != '00':
            time[i] = hours + ' ч ' + minutes + 'мин'
        else:
            time[i] = minutes + ' мин'

    output_df1 = pd.DataFrame({
        'Пользователь': emails,
        'Платформа': platform,
        'Дата просмотра': date
    })

    output_df2 = pd.DataFrame({
        'Дата просмотра': date,
        'Кол-во рекламы': numbers_out,
        'Время просмотра рекламы': time,
        'Вид рекламы': type
    })
    output = []
    output.append(output_df1)
    output.append(output_df2)
    return output


def count_k(path, non_ignore_args):
    tab = get_dataset(path)
    print(list(tab))
    print(non_ignore_args)
    for x in list(tab):
        if x not in non_ignore_args: del tab[x]

    print(list(tab))

    arr = tab.to_numpy()
    ans = 10 ** 9
    cnt = {}
    min_nums = []
    for i in range(len(arr)):
        all_columns = ''
        for x in arr[i]:
            all_columns += str(x)
            all_columns += ' '
        try:
            cnt[all_columns] += 1
        except:
            cnt[all_columns] = 1

    for x in cnt:
        min_nums.append(cnt[x])

    min_nums = sorted(min_nums)
    for x in cnt:
        if cnt[x] in min_nums[:5]: print(x, f'k = {cnt[x]}', f'{round(cnt[x]/len(arr)*100, 3)}%')

    for i in range(len(arr)):
        all_columns = ''
        for x in arr[i]:
            all_columns += str(x)
            all_columns += ' '
        ans = min(ans, cnt[all_columns])

    if ans == 1:
        print('k-anonymity = 1')
        print('Уникальные строки: ')
        for x in cnt:
            if cnt[x] == 1: print(x)
    return ans


if __name__ == "__main__":
    root = gui.CustomUI()
    root.mainloop()
