from concurrent.futures import thread
from function import wait_if_day_off, wait_if_sleeping_time, wait_customized
import telebot

bot = telebot.TeleBot('5540979383:AAHjJMwpp4Jlb6NhfwO1CqkGG23gCvjMob0')  # working bot 
# bot = telebot.TeleBot('5517469762:AAGXoE4Qyfc215kO-J-VNbJTtSRSUpYPdSA')   # testing bot

import threading
import time
import random

chats_dict = {} # chat_id : (Thread, ChatContext)



class ChatContext:
    def __init__(self, chat_id, last_message_id, channel_title):
        self.messages_ids = list(range(last_message_id + 1))
        self.chat_id = chat_id
        self.channel_title = channel_title
        self.last_message_id = last_message_id # used for reinitialization of messages ids when interation over all messages is finished
        
    def handle_new_message(self, message_id):
        self.messages_ids.append(message_id)
        self.last_message_id = message_id 


@bot.message_handler(content_types='text')
def handle_bot_message(message):
    print(message.chat.id)
    bot.reply_to(message, "Hello, did someone call for help?")


@bot.channel_post_handler()
def handle_chat_message(message):
    print("FUNC: handle_chat_message")
    if message.chat.id in chats_dict:
        print("Чат обновился")
        chat_thread, chat_context = chats_dict[message.chat.id]
        chat_context.handle_new_message(message.id)
    else:
        print("Новый чат начал повторение")
        bot.send_message(468918244, "Бот начал работать на канале: " + str(message.chat.title), parse_mode='html')
        chat_context = ChatContext(message.chat.id, message.id, message.chat.title)
        chat_thread = threading.Thread(target=chat_thread_logic, args=(chat_context,))
        chat_thread.start()
        chats_dict[message.chat.id] = (chat_thread, chat_context)
    

def chat_thread_logic(chat_context):
    print("FUNC: chat_thread_logic")
    print(chat_context.chat_id)
    
    while True:

        if wait_customized(chat_context.chat_id): # if some some seconds returned => chat is has customized scheduling (otherwise None)
            wait_time = wait_customized(chat_context.chat_id)
            time.sleep(wait_time)
        else:
            timeout = 3*60*60    # three hours
            time.sleep(timeout)

            wait_if_day_off()
            wait_if_sleeping_time()
        
        successfully_forwaded = False
        while successfully_forwaded == False:
            rand_message_id = random.choice(chat_context.messages_ids)

            successfully_forwaded = try_forward_message_id(chat_context.chat_id, rand_message_id)
            
            if successfully_forwaded == False:
                chat_context.messages_ids.remove(rand_message_id)
                # it can happen that after removal the list will be empty => reinitialize
                if not chat_context.messages_ids:
                    chat_context.messages_ids = list(range(chat_context.last_message_id + 1))
                    bot.send_message(468918244, ":bangbang: CHANNEL: <b><i>" + str(chat_context.channel_title) + "</i></b> FINISHED. \n STARTED OVER!", parse_mode='html')
                time.sleep(0.05)
            else:
                chat_context.messages_ids.remove(rand_message_id)
                # if empty, refill the messages id for new loop of iterations
                if not chat_context.messages_ids:
                    chat_context.messages_ids = list(range(chat_context.last_message_id + 1))
                    bot.send_message(468918244, ":bangbang: CHANNEL: <b><i>" + str(chat_context.channel_title) + "</i></b> FINISHED. \n STARTED OVER!", parse_mode='html')
                                       

def try_forward_message_id(chat_id, message_id):
    # print("FUNC: try_forward_message_id")
    try:
        bot.forward_message(468918244, chat_id, message_id) 
        return True
    except:
        return False


bot.infinity_polling(timeout=10, long_polling_timeout = 5)