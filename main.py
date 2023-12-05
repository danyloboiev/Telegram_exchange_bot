import telebot
from BotAPI import Bot_API
from Monobank_Rate import *
from Privat_Rate import *
from telebot import types


bot = telebot.TeleBot(Bot_API)

bot_information = f'/monobank - ця команда покаже курс у Монобанк на данний момент' \
				  f'\n\n/privatbank - - ця команда покаже курс у Приватбанк на данний момент' \
				  f'\n\n/uah - ця команда розрахує суму, яку ти введеш у вибрану тобою валюту' \
				  f'\n\nЗараз ти можеш конвертувати у такі валюти:' \
				  f'\nUSD - Долар США' \
				  f'\nEUR - Євро' \
				  f'\nGEL - Грузинська Ларі' \
				  f'\nPLN - Польска злота' \
				  f'\nHUF - Угорський Форінт'

#Команда для загальної інформації та кнопки які показуються під клавіатурою
@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
	mn = types.KeyboardButton('Курс у Монобанк')
	pr = types.KeyboardButton('Курс у Приватбанк')
	markup1.row(mn, pr)
	rate = types.KeyboardButton('Конвертувати суму')
	inf = types.KeyboardButton('Інформація')
	markup1.row(rate, inf)
	bot.send_message(message.chat.id, f"Привіт, {message.from_user.first_name}!\n\nВ цьому боті ти можеш подивитися курс валют "
									  f"у Монобанк та Приватбанк"
									  f"\n\nА також ти можеш конвертувати необхідну сумму у 5 інших валют"
									  f"\n\nДля роботи з ботом обирай команди натиснувши кнопку 'Меню' "
									  f"або натисни на команду /help щоб отримати більше інформації", reply_markup=markup1)
	bot.register_next_step_handler(message, without_comand)

#команда навігація
@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, bot_information)


#Команда для отримання курса у монобанк
@bot.message_handler(commands=['monobank'])
def monobank_all_rate(message):
	bot.send_message(message.chat.id, rate_monobank_to_uah)

#Команда для отримання курса у приватбанк
@bot.message_handler(commands=['privatbank'])
def privatbank_all_rate(message):
	bot.send_message(message.chat.id, rate_privat_to_uah)


#Команда для розрахування сумми у грн до інших валют
@bot.message_handler(commands=['uah'])
def amount_in_uah(message):
		bot.send_message(message.chat.id, crnc_type)
		bot.send_message(message.chat.id, 'Будь ласка, пиши тількі сумму без зайвих знаків та слів.')
		bot.register_next_step_handler(message, handle_number_input)

# Глобальний словник для зберігання останніх чисел від користувачів
last_numbers = {}
def handle_number_input(message):
    user_id = message.from_user.id
    if message.text.isdigit():
        amount = float(message.text)
        if user_id not in last_numbers:
            last_numbers[user_id] = []
        last_numbers[user_id].append(amount)
        show_currency_buttons(message)
    else:
        bot.send_message(message.chat.id, "Будь ласка, пиши тількі сумму без зайвих знаків та слів.\n--> /uah")

#Виконання натискання на кнопку
@bot.callback_query_handler(func=lambda callback: True)
def currency_type(callback):
	chat_id = callback.message.chat.id
	user_id = callback.from_user.id
	if user_id in last_numbers and last_numbers[user_id]:
		amnt = last_numbers[user_id][-1]
		crnc = str(callback.data).upper()
		amnt_rate_mb = round((amnt / mono_uah_to_all[crnc]), 3)
		amnt_rate_pb = round((amnt / privat_uah_to_all[crnc]), 3)
		bot.send_message(callback.message.chat.id, f'{current_date}\n\nУ Монобанк: {amnt} UAH = {amnt_rate_mb} {crnc}'
											   f'\n\nУ Приватбанк: {amnt} UAH = {amnt_rate_pb} {crnc}')
		bot.send_message(callback.message.chat.id,f'Для іншої валюти просто ще раз натисни кнопку вище')
	else:
		bot.send_message(callback.message.chat.id, "Ти не вводив(ла) сумму")

#Кнопки валюти
def show_currency_buttons(message):
	markup = types.InlineKeyboardMarkup()
	USD = types.InlineKeyboardButton('USD', callback_data='usd')
	EUR = types.InlineKeyboardButton('EUR', callback_data='eur')
	markup.row(USD, EUR)
	GEL = types.InlineKeyboardButton('GEL', callback_data='gel')
	PLN = types.InlineKeyboardButton('PLN', callback_data='pln')
	HUF = types.InlineKeyboardButton('HUF', callback_data='huf')
	markup.row(GEL, PLN, HUF)
	bot.reply_to(message, 'Будь ласка, обери валюту в яку хочеш конвертувати', reply_markup=markup)

#Команда якщо просто відправили повідомлення без команди
@bot.message_handler(content_types=['text'])
def without_comand(message):
	if message.text == 'Курс у Монобанк':
		bot.send_message(message.chat.id, rate_monobank_to_uah)
	elif message.text == 'Курс у Приватбанк':
		bot.send_message(message.chat.id, rate_privat_to_uah)
	elif message.text == 'Конвертувати суму':
		bot.send_message(message.chat.id, amount_in_uah(message))
	elif message.text == 'Інформація':
		bot.send_message(message.chat.id, bot_information)
	else:
		bot.send_message(message.chat.id, f'Для того, щоб бот працював треба спочатку натиснути на необхідну команду.'
									  f'\n\nУсі команди тут --> /help')


bot.infinity_polling()