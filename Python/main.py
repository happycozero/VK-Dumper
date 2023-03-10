import vk_api
import os

# Получение пути к файлу и его имени
path, filename = os.path.split(os.path.abspath(__file__))

# Ввод токена
token = input("Введите токен: ")
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

# Открытие файлов с html-кодом
with open(f"{path}/photo_pre.html", "r", encoding="utf8") as f:
    # Чтение содержимого всех трех файлов в отдельные переменные
    file, file1, file2 = f.read(), f.read(), f.read()

try:
    # Получение информации о профиле пользователя
    getinfo = vk.account.getProfileInfo()
    iddd = getinfo["id"]
    vk_name = getinfo["first_name"]
    vk_rename = getinfo["last_name"]

    # Получение списка диалогов пользователя
    test = vk.messages.getConversations(count=200)
    num = test["count"]
    print(f"Всего найдено диалогов: {num}")
    print(f"Начинаю выгрузку фотографий | {vk_name} {vk_rename} - vk.com/id{iddd}")

    # Обработка каждого диалога
    for i in test["items"]:
        idd = i["conversation"]["peer"]["id"]
        peer_type = i["conversation"]["peer"]["type"]

        if peer_type == "user" and idd > 0: # Обработка диалогов с пользователями
            print(f"Выгрузка фотографий - {idd}")
            testtt = vk.users.get(user_ids=idd, fields="sex")

            for b in testtt:
                pol_ebaniy = b["sex"]
                file_to_write = file if pol_ebaniy == 1 else file1 if pol_ebaniy == 2 else file2
                fo = vk.messages.getHistoryAttachments(peer_id=idd, media_type="photo", start_from=0, count=200, preserve_order=1, max_forwards_level=45)

                # Обработка каждой фотографии в диалоге
                for i in fo["items"]:
                    for j in i["attachment"]["photo"]["sizes"]:
                        if 500 < j["height"] < 650:
                            url = j["url"]
                            file_to_write += f'<img class="photos" src="{url}" alt="Не удалось загрузить (:" title="Найдено в диалоге - vk.com/id{idd}">'

        elif peer_type == "group": # Обработка диалогов с группами
            print("Это группа!")
        else: # Обработка диалогов в конференциях
            print("Это конфа!")

    # Запись результатов в файлы
    with open(f"{path}/Девочки - id{iddd}.html", "w+", encoding="utf8") as f:
        f.write(file)
    with open(f"{path}/Мальчики - id{iddd}.html", "w+", encoding="utf8") as f:
        f.write(file1)
    with open(f"{path}/Не определено - id{iddd}.html",  "w+", encoding="utf8") as f:
        f.write(file2)

except Exception as e:
    print(e)
