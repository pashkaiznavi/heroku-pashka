

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
from datetime import datetime
import random
import time
import vk_api

import time
import random
import pyowm
from pyowm import OWM
from peewee import *
import pymysql.cursors  


connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
 
print ("connect successful!!")

q = connection.cursor()



connection.commit()
connection.close()


#login, password='login','password'
# vk_session = vk_api.VkApi(login, password)
# vk_session.auth()
token ='685aa6a78ae82e44d599bcafa15dd0abb8ed80a9ee1c1599ad03fd7e368b44b24540fbeb0fe8de9d3f854'
vk_session = vk_api.VkApi(token=token)
vk = vk_session
vk._auth_token()
session_api = vk_session.get_api()
vk_session._auth_token()
longpoll = VkLongPoll(vk_session)
owm = pyowm.OWM('4b58b95563236bfc8892bae60ba330ba', language='ru')


# -*- coding: utf-8 -*-


def create_keyboard(response):
    keyboard = VkKeyboard(one_time=False)

    if response == 'играть' or 'выход':

        keyboard.add_button('Кубик 1', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Кубик 2', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Кубик 3', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()  # Переход на вторую строку

        keyboard.add_button('Кубик 4', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Кубик 5', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Кубик 6', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()

        keyboard.add_button('Профиль', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Помощь', color=VkKeyboardColor.DEFAULT)

        keyboard.add_line()

        keyboard.add_button('Монетка орел', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('Монетка решка', color=VkKeyboardColor.POSITIVE)

        
    elif response == 'привет':
        keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Помощь', color=VkKeyboardColor.DEFAULT)

    keyboard = keyboard.get_keyboard()
    return keyboard


def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',{id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648), "attachment": attachment, 'keyboard': keyboard})

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                print('Текст сообщения: ' + str(event.text))
                print(event.user_id)
                


                response = event.text.lower()
                body = response
                keyboard = create_keyboard(response)
                messages = vk.method("messages.getConversations", {"offset": 0, "count": 200, "filter": "unanswered"})

                if event.from_user and not event.from_me:
                    if response == "помощь":
                        send_message(vk_session, 'user_id', event.user_id, message= 'Мои команды:\n' + '❓ Помощь [команда] - описание команды, например: помощь кубик или помощь русская рулетка.\n'+ '📒' +' Профиль\n' +'🤝' +' Передать [id] [сумма]\n'+ '✒Мне ник '+'[nick]\n' + '🔫 ' + 'Русская рулетка [сумма]\n' + '🎰'+' Казино' +' [сумма]\n' +'🎲' +' Кубик' +' [грань]\n' +'🦅' +' Монетка' +' [орел/решка]\n'+'🌨' +' Погода' +' [город]\n' +'💲'+ ' Недвижимость :\n🏠 Дом - (100000$)\n🚘 Машина - (50000$)\n🏡 Дача - (40000$)')
                        
                    elif response == "привет":
                        send_message(vk_session, 'user_id', event.user_id, message='Нажми на кнопку, чтобы получить список команд',keyboard=keyboard)

                    elif response == "играть":
                        send_message(vk_session, 'user_id', event.user_id, message= 'Игровые команды:',keyboard=keyboard)

                    elif response == "помощь передать":
                        send_message(vk_session, 'user_id', event.user_id, message= 
                        'Эта команда отвечает за передачу денег другим игрокам. Для того, чтобы передать деньги, вам необходимо узнать циферный'+ ' id'+ ' игрока, которому хотите передать деньги, если вы не знаете циферный'+ ' id' + ' игрока, то зайдите в нашу группу и прочитайте первый пост! Если вы знаете его, то для передачи вам нужно написать команду:\n' +'\nПередать' + ' [id]' + ' [сумма]\n'+ '\nВнимание‼ Правило использования:\n1)' + ' id' +  ' нужно указывать без слова' + ' id' +', тоесть только цифры\n2)Буквенный' + ' id' + ' не следует указывать, средства до человека не дойдут, а у вас могут списаться')

                    elif response == "помощь кубик":
                        send_message(vk_session, 'user_id', event.user_id, message= 
                        '🎲 Команда «Кубик» генерирует случайное число от 1 до 6 и сравнивает его с вашим.\n➖ За каждое угаданное число вы получаете приз: 500 - 2000 $')

                    elif response == "помощь казино":
                        send_message(vk_session, 'user_id', event.user_id, message= 
                        '🎰 Команда Казино [сумма]. Ваша сумма с вероятностью 50% умножается на 2 или вычитается из баланса. Есть шанс, равный 15%, что ваша сумма умножится на 7!')

                    elif response == "помощь монетка":
                        send_message(vk_session, 'user_id', event.user_id, message= 
                        '🦅 В игре монетка вы должны угадать сторону: орел или решка.\n➖ За каждую угаданную грань вы получаете приз: 50 - 300 $')

                    elif response == "помощь недвижимость":
                        send_message(vk_session, 'user_id', event.user_id, message= 
                        '💲 Выбирайте недвижимость, которую хотите приобрести и пишите ее.')

                    elif response == "помощь русская рулетка":
                        send_message(vk_session, 'user_id', event.user_id, message= 
                        '🔫 В игре русская рулетка заряжается револьвер с одним патроном, с каждым выстрелом шанс выжить всё меньше. Когда вы стреляете и выживаете ваша сумма делиться на 3 и с каждым выстрелом умножается на:\n1) 1\n2) 2\n3) 5\n4) 10\n5) 15 \nВ любой момент вы можете забрать выйгрыш, чтобы не рисковать. Но когда вы проигрываете, у вас со счета списывается поставленная сумма, а выйгрыш исчезает!')         

                    

                if messages["count"] >= 1:
                    id = messages['items'][0]['last_message']['peer_id']
                    body = messages['items'][0]['last_message']['text']
                    

                    if "кубик" in body.lower():
                        cube = random.randint(1, 6)
                        user_cube = int(body.lower()[-1])
                        user_win = random.randint(500, 2000)
                        connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

                        print ("connect successful!!")
                        q = connection.cursor()
                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                        result = q.fetchall()
                        if len(result) == 0:
                            Bot = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                            user_name = Bot[0]["first_name"]
                            print("Time to добавить юзера")
                            q.execute(
                                "INSERT INTO Bot (name, vk_id, balance) VALUES ('%s', '%s', '%s')" % (user_name,
                                                                                                              id, 0))
                            connection.commit()
                            connection.close()
                        else:
                            q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                            result = q.fetchall()
                            print(result)
                            user_name = result[0]['name']
                            if user_cube == cube:
                                vk.method("messages.send", {"peer_id": id,
                                                            "message": str(user_name) + ", вы угадали! 😯 Выйгрыш " + str(
                                                                format(user_win,',')) + "$\n" +"💰Ваш баланс: " + str(format((int(result[0]['balance']) + user_win),',')), "random_id": random.randint(1, 2147483647)})
                                q = connection.cursor()
                                q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                                result = q.fetchall()
                                q.execute(
                                    "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(result[0]['balance']) + user_win, id))
                                connection.commit()
                                connection.close()

                            else:
                                vk.method("messages.send", {"peer_id": id,
                                                            "message": str(user_name) +  ", вы проиграли!\n 🎲 Выпало число " + str(
                                                                cube) + " 😔", "random_id": random.randint(1, 2147483647)})
                    
                    

                                                            

                    
                    # elif 'русская рулетка' in body.lower():
                    #     id = messages['items'][0]['last_message']['peer_id']
                    #     connection = pypyodbc.connect('DRIVER={SQL Server};'
                    #     'SERVER=fearstrike.com/phpmyadmin;'
                    #     'DATABASE=admin_pashka;'
                    #     'UID=admin_pashka;'
                    #     'PWD=pavlyha2002'
                    #     'PORT=3306')
                    #     q = connection.cursor()
                    #     q.execute("SELECT * FROM BotUsers WHERE vk_id = %s" % (id))
                    #     result = q.fetchall()

                    #     if len(result) == 0:
                    #         BotUsers = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                    #         user_name = BotUsers[0]["first_name"]
                    #         print("Time to добавить юзера")
                    #         q.execute(
                    #             "INSERT INTO BotUsers (Name, vk_id, Balance) VALUES ('%s', '%s', '%s')" % (user_name,
                    #                                                                                           id, 0))
                    #         connection.commit()
                    #         connection.close()
                    #     else:
                    #         sum = int(body.lower()[16:])
                    #         koeficient = 1
                    #         win = 0
                    #         ran = random.randint(1, 6)
                    #         ch = 6
                    #         if (int(result[0][3]) >= sum) and (sum >= 500) :
                                
                    #             vk.method("messages.send", {"peer_id": id,
                    #                                         "message": '🔫 Напишите рулетка, чтобы выстрелить.\n❌ Напишите выход, чтобы забрать выйгрыш.', "random_id": random.randint(1, 2147483647)})
                    #             id = messages['items'][0]['last_message']['peer_id']
                    #             body = messages['items'][0]['last_message']['text']
                    #             for event in longpoll.listen():
                    #                 if event.type == VkEventType.MESSAGE_NEW:
                    #                     print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                    #                     print('Текст сообщения: ' + str(event.text))
                    #                     print(event.user_id)

                    #                     response = event.text.lower()
                    #                     body = response
                    #                     keyboard = create_keyboard(response)
                    #                     messages = vk.method("messages.getConversations", {"offset": 0, "count": 200, "filter": "unanswered"})

                                    




                                    
                    #                 #     if "рулетка" == response:
                    #                 #         stavka = round(sum/3)
                                            
                    #                 #         if ran == 1:
                    #                 #             vk.method("messages.send", {"peer_id": id,
                    #                 #                     "message":   "Вы проиграли 💀🔫 На лечение потрачено: " + format(sum,',') + "$\n💰Ваш баланс: " + str(format((int(result[0][3]) - sum),',')), "random_id": random.randint(1, 2147483647)})
                    #                 #             q = connection.cursor()
                    #                 #             q.execute("SELECT * FROM BotUsers WHERE vk_id = %s" % (id))
                    #                 #             result = q.fetchall()
                    #                 #             q.execute(
                    #                 #                 "UPDATE BotUsers SET Balance = '%s' WHERE vk_id = '%s'" % (int(result[0][3]) - sum, id))
                    #                 #             connection.commit()
                    #                 #             connection.close()
                    #                 #             break
                    #                 #         else:
                    #                 #             win = stavka * koeficient
                    #                 #             if koeficient == 2:
                    #                 #                 koeficient = 5
                    #                 #                 ran = random.randint(1, (ch - 1))
                    #                 #                 ch -= 1 
                    #                 #                 vk.method("messages.send", {"peer_id": id,
                    #                 #                     "message":   "Фух, пронесло 😉 Выйгрыш если уйдёте: " + format(win,',') + '$', "random_id": random.randint(1, 2147483647)})
                    #                 #                 continue
                    #                 #             elif koeficient == 5:
                    #                 #                 koeficient = 10
                    #                 #                 ran = random.randint(1, (ch - 1))
                    #                 #                 ch -= 1 
                    #                 #                 vk.method("messages.send", {"peer_id": id,
                    #                 #                     "message":   "Фух, пронесло 😉 Выйгрыш если уйдёте: " + format(win,',') + '$', "random_id": random.randint(1, 2147483647)})
                    #                 #                 continue
                    #                 #                 continue
                    #                 #             elif koeficient == 11:
                    #                 #                 win = stavka * 15
                    #                 #                 q = connection.cursor()
                    #                 #                 q.execute("SELECT * FROM BotUsers WHERE vk_id = %s" % (id))
                    #                 #                 result = q.fetchall()
                    #                 #                 q.execute(
                    #                 #                     "UPDATE BotUsers SET Balance = '%s' WHERE vk_id = '%s'" % (int(result[0][3]) + win, id))
                    #                 #                 connection.commit()
                    #                 #                 connection.close()
                    #                 #                 vk.method("messages.send", {"peer_id": id,
                    #                 #                     "message": "🎉 Поздравляю! Вы выжили после пяти выстрелов! Вы заработали: " + format(win,',') + "$\n💰Ваш баланс: " + str(format((int(result[0][3]) + win),',')), "random_id": random.randint(1, 2147483647)})
                                    

                    #                 #                 break
                                                



                    #                 #             else:
                    #                 #                 koeficient += 1
                    #                 #                 ran = random.randint(1, (ch - 1))
                    #                 #                 ch -= 1 
                    #                 #                 vk.method("messages.send", {"peer_id": id,
                    #                 #                     "message": "Фух, пронесло 😉 Выйгрыш если уйдёте: " + format(win,',') + '$', "random_id": random.randint(1, 2147483647)})
                    #                 #                 continue
                                        
                    #                 #     elif response == "выход":
                    #                 #             q = connection.cursor()
                    #                 #             q.execute("SELECT * FROM BotUsers WHERE vk_id = %s" % (id))
                    #                 #             result = q.fetchall()
                    #                 #             q.execute(
                    #                 #                 "UPDATE BotUsers SET Balance = '%s' WHERE vk_id = '%s'" % (int(result[0][3]) + win, id))
                    #                 #             connection.commit()
                    #                 #             connection.close()
                    #                 #             vk.method("messages.send", {"peer_id": id,
                    #                 #                     "message": "Вы заработали: " + format(win,',') + "$\n💰Ваш баланс: " + str(format((int(result[0][3]) + win),',')), "random_id": random.randint(1, 2147483647)})
                                                

                    #                 #             break
                                        
                    #                 #     else:
                    #                 #         vk.method("messages.send", {"peer_id": id,
                    #                 #                     "message":  "Напишите рулетка или выход", "random_id": random.randint(1, 2147483647)})
                    #                 #         continue
                    #                 # elif int(result[0][3]) < sum:
                    #                 #     vk.method("messages.send", {"peer_id": id,
                    #                 #                                 "message":  "Недостаточно средств!\n" + "Ваш баланс: " + str(format(int(result[0][3]),',')), "random_id": random.randint(1, 2147483647)})
                                                                         
                    #                 # elif sum < 500:
                    #                 #     vk.method("messages.send", {"peer_id": id,
                    #                 #                                 "message": "Минимальная ставка 500$", "random_id": random.randint(1, 2147483647)})                        
                            
                            





                    elif "мне ник" in body.lower():

                        connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                        q = connection.cursor()
                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                        result = q.fetchall()
                        if len(result) == 0:
                            Bot = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                            user_name = Bot[0]["first_name"]
                            print("Time to добавить юзера")
                            q.execute(
                                "INSERT INTO Bot (Name, vk_id, Balance) VALUES ('%s', '%s', '%s')" % (user_name,
                                                                                                              id, 0))
                            connection.commit()
                            connection.close()
                        else:
                            nick = body.lower()[8:]
                            connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                            q = connection.cursor()
                            q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                            q.execute("UPDATE Bot SET nick = '%s' WHERE vk_id = '%s'" % (nick, id))
                            connection.commit()
                            connection.close()
                            vk.method("messages.send",
                                    {"peer_id": id, "message": "Ник успешно установлен!" , "random_id": random.randint(1, 2147483647)})
                     
                    elif 'привет' in body.lower():
                        connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                        q = connection.cursor()
                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                        result = q.fetchall()
                        if len(result) == 0:
                            Bot = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                            user_name = Bot[0]["first_name"]
                            print("Time to добавить юзера")
                            q.execute(
                                "INSERT INTO Bot (Name, vk_id, Balance) VALUES ('%s', '%s', '%s')" % (user_name,
                                                                                                              id, 0))
                            connection.commit()
                            connection.close()

                    
                    elif "передать" in body.lower():
                        connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                        q = connection.cursor()
                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                        result = q.fetchall()
                        if len(result) == 0:
                            Bot = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                            user_name = Bot[0]["first_name"]
                            print("Time to добавить юзера")
                            q.execute(
                                "INSERT INTO Bot (Name, vk_id, Balance) VALUES ('%s', '%s', '%s')" % (user_name,
                                                                                                              id, 0))
                            connection.commit()
                            connection.close()
                        else:
                            
                            sum = str(body.lower()[19:])
                            chel = str(body.lower()[9:18])
                            connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                            q = connection.cursor()
                            user_name = result[0][1]
                            q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                            result = q.fetchall()
                            if int(result[0][3]) >= int(sum):
                                q = connection.cursor()

                                q.execute(
                                            "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(result[0][3]) - int(sum), id))
                               
                                
                                connection.commit()
                                connection.close()

                                connection = pymysql.connect(host='fearstrike.com',
                                 user='admin_pashka',
                                 password='pavlyha2002',
                                 db='admin_pashka',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
                                
                                q = connection.cursor()
                                q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (chel))
                                result = q.fetchall()
                                
                                q = connection.cursor()
                                q.execute(
                                            "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(result[0][3]) + int(sum), chel))
                                connection.commit()
                                connection.close()
                                vk.method("messages.send",
                                    {"peer_id": id, "message": "Средства успешно переданы!" , "random_id": random.randint(1, 2147483647)})
                                vk.method("messages.send",
                                    {"peer_id": int(chel), "message": "Получено " +sum+  "$ !\nОт: " + user_name , "random_id": random.randint(1, 2147483647)})
                            else:
                                    vk.method("messages.send",
                                  {"peer_id": id, "message": "Недостаточно средств!\n" + "Ваш баланс: " + str(result[0][3]) , "random_id": random.randint(1, 2147483647)})

                            
                        
                     



                    elif "монетка" in body.lower():
                        r = ['орел', 'решка']
                        cube = random.choice(r)
                        user_cube = str(body.lower()[8:])
                        user_win = random.randint(50, 300)
                        connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                        q = connection.cursor()
                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                        result = q.fetchall()
                        if len(result) == 0:
                            Bot = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                            user_name = Bot[0]["first_name"]
                            print("Time to добавить юзера")
                            q.execute(
                                "INSERT INTO Bot (Name, vk_id, Balance) VALUES ('%s', '%s', '%s')" % (user_name,
                                                                                                              id, 0))
                            connection.commit()
                            connection.close()
                        else:
                            q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                            result = q.fetchall()
                            print(result)
                            user_name = result[0]['name']
                            if user_cube == cube:
                                vk.method("messages.send", {"peer_id": id,
                                                            "message": user_name + ", вы угадали! 😯 Выйгрыш " + str(
                                                                format(user_win,',')) + "$\n" +"💰Ваш баланс: " + str(format((int(result[0]['balance']) + user_win),',')), "random_id": random.randint(1, 2147483647)})
                                q = connection.cursor()
                                q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                                result = q.fetchall()
                                q.execute(
                                    "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(result[0]['balance']) + user_win, id))
                                connection.commit()
                                connection.close()
                                
                            else:
                                vk.method("messages.send", {"peer_id": id,
                                                            "message": user_name + ", вы проиграли!" + " 😔", "random_id": random.randint(1, 2147483647)})




                    elif body.lower() == "пашка тащит":

                        connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                        q = connection.cursor()
                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                        result = q.fetchall()
                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                        result = q.fetchall()
                        print(result)
                        user_name = result[0]['name']

                        vk.method("messages.send", {"peer_id": id,
                                                            "message": "Павел, вы супер! 😯 Выйгрыш " + str(100000) + "$", "random_id": random.randint(1, 2147483647)})
                        q = connection.cursor()
                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                        result = q.fetchall()
                        q.execute(
                                    "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(result[0]['balance']) + 100000, id))
                        connection.commit()
                        connection.close()


                    elif "казино" in body.lower():
                        connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                        q = connection.cursor()
                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                        result = q.fetchall()
                        if len(result) == 0:
                            Bot = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                            user_name = Bot[0]["first_name"]
                            print("Time to добавить юзера")
                            q.execute(
                                "INSERT INTO Bot (Name, vk_id, Balance) VALUES ('%s', '%s', '%s')" % (user_name,
                                                                                                              id, 0))
                            connection.commit()
                            connection.close()
                        else:
                            kazino = random.randint(1, 2)
                            
                            rate = int(body.lower().split("казино ")[-1])
                            if int(result[0]['balance']) >= rate:
                                if kazino == 1:
                                    coefficient = random.randint(1, 8)
                                    
                                    if coefficient == 1:
                                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                                        result = q.fetchall()
                                        money = result[0]['balance']
                                        connection = pymysql.connect(host='fearstrike.com',
                                         user='admin_pashka',
                                         password='pavlyha2002',
                                         db='admin_pashka',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
                                        q = connection.cursor()
                                        q.execute("UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(money) +
                                                                                                                rate * 7, id))
                                        connection.commit()
                                        connection.close()
                                        vk.method("messages.send",
                                                  {"peer_id": id, "message": "Вы выиграли " + str(format((rate * 7),',')) +" (x7)" + "!😯\n" + "💰Ваш баланс: " + str(format((int(money) +
                                                                                                                rate * 7),',')), "random_id": random.randint(1, 2147483647)})
                                    else:
                                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                                        result = q.fetchall()
                                        money = result[0]['balance']
                                        connection = pymysql.connect(host='fearstrike.com',
                                         user='admin_pashka',
                                         password='pavlyha2002',
                                         db='admin_pashka',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
                                        q = connection.cursor()
                                        q.execute("UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(money) +
                                                                                                                rate * 2, id))
                                        connection.commit()
                                        connection.close()
                                        vk.method("messages.send",
                                                  {"peer_id": id, "message": "Вы выиграли " + str(format((rate * 2),',')) + " (x2)" + "!😯\n" + "Ваш баланс: " + str(format((int(money) +
                                                                                                                rate * 2),',')), "random_id": random.randint(1, 2147483647)})
                                        
                                elif kazino == 2:
                                    vk.method("messages.send",
                                              {"peer_id": id, "message": "Вы проиграли " + str(format(rate,',')) + "😔\n" + "Ваш баланс: " + str(format((int(result[0]['balance']) - rate),',')) , "random_id": random.randint(1, 2147483647)})
                                    
                                    connection = pymysql.connect(host='fearstrike.com',
                                    user='admin_pashka',
                                    password='pavlyha2002',
                                    db='admin_pashka',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
                                    q = connection.cursor()
                                    q.execute("UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(result[0]['balance']) - rate, id))
                                    connection.commit()
                                    connection.close()
                            else:
                                vk.method("messages.send",
                              {"peer_id": id, "message": "Недостаточно средств!\n" + "Ваш баланс: " + str(format(int(result[0]['balance']),',')) , "random_id": random.randint(1, 2147483647)})
                    # elif 'id' in body.lower():
                    #     connection = pymysql.connect(host='fearstrike.com',
                    #          user='admin_pashka',
                    #          password='pavlyha2002',
                    #          db='admin_pashka',
                    #          charset='utf8mb4',
                    #          cursorclass=pymysql.cursors.DictCursor)
                    #     q = connection.cursor()
                    #     q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                    #     result = q.fetchall()
                    #     if len(result) == 0:
                    #         Bot = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                    #         user_name = Bot[0]["first_name"]
                    #         print("Time to добавить юзера")
                    #         q.execute(
                    #             "INSERT INTO Bot (Name, vk_id, Balance) VALUES ('%s', '%s', '%s')" % (user_name,
                    #                                                                                           id, 0))
                    #         connection.commit()
                    #         connection.close()
                    #     else:
                    #         nick = str(body.lower()[3:])
                    #         q.execute("SELECT * FROM Bot WHERE nick = %s" % str(nick))
                    #         result = q.fetchall()
                    #         id1 = result[0][2]
                    #         if len(nick) != 0:
                    #             vk.method("messages.send", {"peer_id": id,
                    #                                     "message": id1, "random_id": random.randint(1, 2147483647)})

                    #         else:
                    #             vk.method("messages.send", {"peer_id": id,
                    #                                     "message": "Игрок не найден!", "random_id": random.randint(1, 2147483647)})




                    elif body.lower() == "профиль":
                        connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                        q = connection.cursor()
                        q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                        result = q.fetchall()
                        if len(result) == 0:
                            Bot = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                            user_name = Bot[0]["first_name"]
                            print("Time to добавить юзера")
                            q.execute(
                                "INSERT INTO Bot (Name, vk_id, Balance) VALUES ('%s', '%s', '%s')" % (user_name,
                                                                                                              id, 0))
                            connection.commit()
                            connection.close()
                        else:
                        
                            q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                            result = q.fetchall()
                            
                            name = result[0]['name']
                            balance = result[0]['balance']
                            ownment = result[0]['ownment']
                            # data = result[0][5]
                            nick = result[0]['nick']

                            ownment_message = ""
                            if ownment != None:
                                ownment = ownment.split(",")
                                ownment = ownment[:-1]
                                for own in ownment:
                                    if int(own) == 1:
                                        ownment_message += "Дом 🏠\n"
                                    elif int(own) == 2:
                                        ownment_message += "Машина 🚘\n"
                                    elif int(own) == 3:
                                        ownment_message += "Дача 🏡\n"
                            vk.method("messages.send", {"peer_id": id,
                                                        "message": name + ", ваш профиль:\n"+ "\n✒Ваш ник: " + str(nick)+  "\n💰Денег: " + str(format(int(balance),',')) +
                                                                   "\n👑 Ваши владения:\n " + ownment_message, "random_id": random.randint(1, 2147483647)})



                    elif "погода" in body.lower() :
                        place = str(body.lower()[7:])
                        observation = owm.weather_at_place(place)
                        w = observation.get_weather()
                        yasno = w.get_detailed_status()
                        temper = w.get_temperature('celsius')['temp']
                        vk.method("messages.send", {"peer_id": id,
                                "message": "Температура: " + str(temper) + " °C\n " + "Сейчас: " + yasno, "random_id": random.randint(1, 2147483647)})
                    
                    




                    elif "дом" or "машина" or "дача" == body.lower():
                        try:
                            connection = pymysql.connect(host='fearstrike.com',
                             user='admin_pashka',
                             password='pavlyha2002',
                             db='admin_pashka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                            q = connection.cursor()
                            q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                            result = q.fetchall()
                            if len(result) == 0:
                                Bot = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                                user_name = Bot[0]["first_name"]
                                print("Time to добавить юзера")
                                q.execute(
                                    "INSERT INTO Bot (Name, vk_id, Balance) VALUES ('%s', '%s', '%s')" % (user_name,
                                                                                                                  id, 0))
                                connection.commit()
                                connection.close()
                            else:
                                realty = body.lower()
                                if realty == "дом":
                                    connection = pymysql.connect(host='fearstrike.com',
                                     user='admin_pashka',
                                     password='pavlyha2002',
                                     db='admin_pashka',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
                                    q = connection.cursor()
                                    q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                                    result = q.fetchall()
                                    money = result[0]['balance']
                                    ownment = result[0]['ownment']
                                    if int(money) >= 100000:
                                        if ownment != None:
                                            q.execute("UPDATE Bot SET Ownment = '%s' WHERE vk_id = '%s'" % (
                                            str(ownment) + "1,", id))
                                            q.execute(
                                                "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(money) - 100000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": id, "message": "Вы купили дом&#127968;!\n" + "Ваш баланс: " + str(format((int(result[0]['balance'])-100000),',')), "random_id": random.randint(1, 2147483647)})
                                        else:
                                            q.execute("UPDATE Bot SET Ownment = '%s' WHERE vk_id = '%s'" % ("1,", id))
                                            q.execute(
                                                "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(money) - 100000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": id, "message": "Вы купили дом&#127968;!\n" + "Ваш баланс: " + str(format((int(result[0]['balance'])-100000),',')) , "random_id": random.randint(1, 2147483647)})
                                    else:
                                        vk.method("messages.send",
                                                  {"peer_id": id, "message": "Недостаточно денег для покупки!\n" + "Вам не хватает: " + str(format((100000 - int(result[0]['balance'])),',')), "random_id": random.randint(1, 2147483647)})
                                elif realty == "машина":
                                    connection = pymysql.connect(host='fearstrike.com',
                                     user='admin_pashka',
                                     password='pavlyha2002',
                                     db='admin_pashka',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
                                    q = connection.cursor()
                                    q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                                    result = q.fetchall()
                                    money = result[0]['balance']
                                    ownment = result[0]['ownment']
                                    if int(money) >= 50000:
                                        if ownment != None:
                                            q.execute("UPDATE Bot SET Ownment = '%s' WHERE vk_id = '%s'" % (
                                            str(ownment) + "2,", id))
                                            q.execute(
                                                "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(money) - 50000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": id, "message": "Вы купили машину!&#128664;\n" + "Ваш баланс: " + str(format((int(result[0]['balance'])-50000),',')), "random_id": random.randint(1, 2147483647)})
                                        else:
                                            q.execute("UPDATE Bot SET Ownment = '%s' WHERE vk_id = '%s'" % ("2,", id))
                                            q.execute(
                                                "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(money) - 50000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": id, "message": "Вы купили машину!&#128664;\n" + "Ваш баланс: " + str(format((int(result[0]['balance'])-50000),',')), "random_id": random.randint(1, 2147483647)})
                                    else:
                                        vk.method("messages.send",
                                                  {"peer_id": id, "message": "Недостаточно денег для покупки!\n" + "Вам не хватает: " + str(format((50000 - int(result[0]['balance'])),',')), "random_id": random.randint(1, 2147483647)})
                                elif realty == "дача":
                                    connection = pymysql.connect(host='fearstrike.com',
                                     user='admin_pashka',
                                     password='pavlyha2002',
                                     db='admin_pashka',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
                                    q = connection.cursor()
                                    q.execute("SELECT * FROM Bot WHERE vk_id = %s" % (id))
                                    result = q.fetchall()
                                    money = result[0]['balance']
                                    ownment = result[0]['ownment']
                                    if int(money) >= 40000:
                                        if ownment != None:
                                            q.execute("UPDATE Bot SET Ownment = '%s' WHERE vk_id = '%s'" % (
                                            str(ownment) + "3,", id))
                                            q.execute(
                                                "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(money) - 40000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": id, "message": "Вы купили дачу!&#127969;\n" + "Ваш баланс: " + str(format((int(result[0]['balance'])-40000),',')), "random_id": random.randint(1, 2147483647)})
                                        else:
                                            q.execute("UPDATE Bot SET Ownment = '%s' WHERE vk_id = '%s'" % ("3,", id))
                                            q.execute(
                                                "UPDATE Bot SET Balance = '%s' WHERE vk_id = '%s'" % (int(money) - 40000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": id, "message": "Вы купили дачу!&#127969;\n" + "Ваш баланс: " + str(format((int(result[0]['balance'])-40000),',')), "random_id": random.randint(1, 2147483647)})
                                    else:
                                        vk.method("messages.send",
                                                  {"peer_id": id, "message": "Недостаточно денег для покупки!\n" + "Вам не хватает: " + str(format((40000 - int(result[0]['balance'])),',')), "random_id": random.randint(1, 2147483647)})
                        except:
                            vk.method("messages.send", {"peer_id": id, "message": "Введите корректный id недвижимости!", "random_id": random.randint(1, 2147483647)})
                    

     except:
         time.sleep(1)

    print('-' * 30)