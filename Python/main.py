import vk_api
import datetime
import time
import os
import requests

# Токен
vk_session = vk_api.VkApi(token='Введите токен: ')
vk = vk_session.get_api()
a = vk.friends.get(order='name', count=5000, fields='domain, first_name, last_name')
for i in a["items"]:
    k = i['id']
    g = vk.messages.getHistory(count=1, user_id=k)
    num_m = g['count']  # кол-во сообщений
    if num_m > 0:
        print(f'Дамп юзера - {k}')
        print('Кол-во сообщений:', num_m)
        f = open(f'Dilog{k}.txt', 'w', encoding='utf-8')
        f.write(f'Диалог с {i["first_name"]} {i["last_name"]} {k} \n')
        q = 0
        while num_m > q:
            var = vk.messages.getHistory(offset=q, count=200, user_id=k, rev=1)
            for a in var['items']:
                times = datetime.datetime.fromtimestamp(a["date"])
                f.write(f'От: https://vk.com/id{a["from_id"]}\n')
                f.write(f'Дата: {times.strftime("%d/%m/%Y, %H:%M:%S")}\n')
                f.write(f'Сообщение: {a["text"]}\n')
                f.write('\n')
            q += 200
            time.sleep(0.3)
        f.close()
        fo = vk.messages.getHistoryAttachments(peer_id=k, media_type='photo', start_from=0, count=200, preserve_order=1,
                                               max_forwards_level=45)
        os.mkdir(f'Архив id{k}')
        os.replace(f'Dilog{k}.txt', f'Архив id{k}/Dilog{k}.txt')
        for i in fo["items"]:
            for j in i["attachment"]["photo"]["sizes"]:
                if j["height"] > 500 and j["height"] < 650:
                    url = j["url"]
                    print(f'Дамп фото: {url}')
                    r = requests.get(url)
                    with open(f'Архив id{k}/image{k}-{i["attachment"]["photo"]["access_key"]}.jpg', 'wb') as img:
                        img.write(r.content)
    else:
        continue