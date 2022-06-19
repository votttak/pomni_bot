from concurrent.futures import thread
import telebot

bot = telebot.TeleBot('5540979383:AAHjJMwpp4Jlb6NhfwO1CqkGG23gCvjMob0')

import threading
import time
import random

chats_dict = {} # chat_id : (Thread, ChatContext)

class ChatContext:
    def __init__(self, chat_id, last_message_id):
        self.messages_ids = list(range(last_message_id))
        self.chat_id = chat_id
        
    def handle_new_message(self, message_id):
        self.messages_ids.append(message_id)





@bot.channel_post_handler()
def handle_chat_message(message):
    
    if message.chat.id in chats_dict:
        print("Чат обновился")
        chat_thread, chat_context = chats_dict[message.chat.id]
        chat_context.handle_new_message(message.id)
    else:
        print("Новый чат начал повторение")
        chat_context = ChatContext(message.chat.id, message.id)
        chat_thread = threading.Thread(target=chat_thread_logic, args=(chat_context,))
        chat_thread.start()
        chats_dict[message.chat.id] = (chat_thread, chat_context)

def chat_thread_logic(chat_context):
    while True:

        seconds_in_week = 604800
        seconds_in_day = 24*60*60
        seconds_in_two_h = 2*60*60
        print("Спим " + str(seconds_in_two_h) + "секунд")
        time.sleep(seconds_in_two_h)
        
        successfully_forwaded = False
        
        while successfully_forwaded == False:
            rand_message_id = random.choice(chat_context.messages_ids)
            
            successfully_forwaded = try_forward_message_id(chat_context.chat_id, rand_message_id)
            
            if successfully_forwaded == False:
                chat_context.messages_ids.remove(rand_message_id)
                time.sleep(2)
        
def try_forward_message_id(chat_id, message_id):
    try:
        bot.forward_message(468918244, chat_id, message_id)
        return True
    except:
        return False

# bot.polling(none_stop=True)
# bot.infinity_polling(True)
bot.infinity_polling(timeout=10, long_polling_timeout = 5)