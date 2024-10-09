import vk_api
import os

# Получение пути к файлу и его имени
path, filename = os.path.split(os.path.abspath(__file__))

# Ввод токена
token = input("Введите токен: ")
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

# Открытие файла с html-кодом и чтение содержимого
with open(f"{path}/photo_pre.html", "r", encoding="utf8") as f:
    file, file1, file2 = [f.read() for _ in range(3)]

try:
    # Получение информации о профиле пользователя
    profile_info = vk.account.getProfileInfo()
    user_id = profile_info["id"]
    first_name = profile_info["first_name"]
    last_name = profile_info["last_name"]

    # Получение списка диалогов пользователя
    conversations = vk.messages.getConversations(count=200)
    print(f"Всего найдено диалогов: {conversations['count']}")
    print(f"Начинаю выгрузку фотографий | {first_name} {last_name} - vk.com/id{user_id}")

    # Обработка каждого диалога
    for conversation in conversations["items"]:
        peer_id = conversation["conversation"]["peer"]["id"]
        peer_type = conversation["conversation"]["peer"]["type"]

        if peer_type == "user" and peer_id > 0:  # Только диалоги с пользователями
            print(f"Выгрузка фотографий - {peer_id}")
            user_info = vk.users.get(user_ids=peer_id, fields="sex")[0]
            sex = user_info["sex"]

            file_to_write = {1: file, 2: file1}.get(sex, file2)
            attachments = vk.messages.getHistoryAttachments(
                peer_id=peer_id, media_type="photo", count=200, preserve_order=1, max_forwards_level=45
            )

            # Обработка фотографий
            for attachment in attachments["items"]:
                for size in attachment["attachment"]["photo"]["sizes"]:
                    if 500 < size["height"] < 650:
                        url = size["url"]
                        file_to_write += f'<img class="photos" src="{url}" alt="Не удалось загрузить (:" title="Найдено в диалоге - vk.com/id{peer_id}">'

        else:
            print("Это группа!" if peer_type == "group" else "Это конфа!")

    # Запись результатов в файлы
    output_files = {
        f"{path}/Девочки - id{user_id}.html": file,
        f"{path}/Мальчики - id{user_id}.html": file1,
        f"{path}/Не определено - id{user_id}.html": file2,
    }

    for file_path, content in output_files.items():
        with open(file_path, "w+", encoding="utf8") as f:
            f.write(content)

except Exception as e:
    print(f"Произошла ошибка: {e}")
