from concurrent.futures import thread
import telebot

bot = telebot.TeleBot('5540979383:AAHjJMwpp4Jlb6NhfwO1CqkGG23gCvjMob0')

# @bot.message_handler(commands=['start'])
# def start(message):
#     if message.text == 'start':
#         bot.send_message(message.from_user.id, "привет", parse_mode=None)
#         bot.send_message(message.from_user.id, "<b>привет</b>", parse_mode='html')                 # message.chat.id <-- через сообщение мы обратились к чату и получили его индентификатор
#     else:
#         bot.send_message(message.from_user.id, "Напиши /start")


@bot.message_handler(content_types=['text'])
def start_2(message):
    print(message)
    # if message.text == 'start':
    #     bot.send_message(message.from_user.id, "привет", parse_mode=None)
    #     bot.send_message(message.from_user.id, "<b>привет</b>", parse_mode='html')                 # message.chat.id <-- через сообщение мы обратились к чату и получили его индентификатор
    # else:
    #     bot.send_message(message.from_user.id, "Напиши /start")

# @bot.channel_post_handler()
# def start_2(message):
#     print("HERE")
#     print(message)   
#     print(message.chat.id) 
#     bot.forward_message(468918244, message.chat.id, 300)  
    


##################################################################

import threading
import time
import random
 


chats_dict = {} 

# chats_dict =  { chat_id_1: {"thread_id": thread_id_1; "messages_id": []},
#                 chat_id_2: {"thread_id": thread_id_2; "messages_id": []}            
#               }




last_message_id = 0
last_task = None
last_chat_id = 0
stop_thread = None






 
@bot.channel_post_handler()
def handle_chat_message(message):
    
    global last_message_id
    global last_chat_id
    global last_task
    global chats_dict

    last_message_id = message.id
    last_chat_id = message.chat.id
    
    if last_chat_id in chats_dict: 
        old_thread = chats_dict[last_chat_id]["thread_id"]

        global stop_thread 
        stop_thread = True
        old_thread.join()

        # chats_dict[last_chat_id]["message_ids"] = list(range(last_message_id))
        # chats_dict[last_chat_id]["thread_id"] = threading.Thread(target=random_forward_task(last_chat_id, last_message_id))
        # chats_dict[last_chat_id]["thread_id"].start()
        
        
    else:
        stop_thread = False
        last_task = threading.Thread(target=random_forward_task(last_chat_id, last_message_id))
        chats_dict[last_chat_id] = {"message_ids": list(range(last_message_id)), "thread_id": last_task}
        last_task.start()




    
def random_forward_task(chat_id, last_msg_id_local):

    global stop_thread

    while True:
        time.sleep(5)
        rnd_msg_id = random.randint(0, last_msg_id_local)
        
        print("LAST_MESSAGE_ID")
        print(last_msg_id_local)
        
        isSuccess = False
        
        if stop_thread:
            break
        
        while isSuccess == False:
            try:
                # print(1)
                bot.forward_message(468918244, chat_id, rnd_msg_id)
                # print(3)
                isSuccess = True
            except:
                # print(2)
                isSuccess = True
    
    # stop_thread = False
 



##################################################################






bot.polling(none_stop=True)