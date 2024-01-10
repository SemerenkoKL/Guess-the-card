from random import choice
import telebot


API_KEY = '***' # API бота
CARD_NUMBERS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_SUIT = ["♦", "♥", "♠", "♣"]
TEXT_START = "Привет! Я бот который могу с тобой поиграть в карты."
TEXT_HELP = """Лис всегда поможет!
/menu - Показывет возможные игры (меню)
/help - Введёт в курс дела (помощь)
/show - Показывает твои результаты в игре (счёт)"""
TEXT_MENU = """Выберите уровень сложности:
Уровень 1 - Угадай цвет карты 🟥 или ⬛️
Уровень 2 - Угадай масть карты ♥, ♦, ♠, ♣
Уровень 3 - Угадай карту"""

bot = telebot.TeleBot(API_KEY)
show_cart = {"level_1" : 0, "level_1_victory" : 0, "level_1_defeat" : 0,
             "level_2" : 0, "level_2_victory" : 0, "level_2_defeat" : 0,
             "level_3" : 0, "level_3_victory" : 0, "level_3_defeat" : 0}

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, TEXT_START)
  help(message)
  
@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, TEXT_HELP)

@bot.message_handler(commands=['show'])
def show(message):
  string_1 = f'Ты сыграл в 1 уровень {show_cart["level_1"]} раз:\n Победил: {show_cart["level_1_victory"]} Проиграл: {show_cart["level_1_defeat"]}\n'
  string_2 = f'Ты сыграл в 2 уровень {show_cart["level_2"]} раз:\n Победил: {show_cart["level_2_victory"]} Проиграл: {show_cart["level_2_defeat"]}\n'
  string_3 = f'Ты сыграл в 3 уровень {show_cart["level_3"]} раз:\n Победил: {show_cart["level_3_victory"]} Проиграл: {show_cart["level_3_defeat"]}'
  string = string_1 + "\n" + string_2 + "\n" + string_3
  bot.send_message(message.chat.id, string)
  do_you_want_to_continue_playing(message)

@bot.message_handler(commands=["menu"])
def menu(message):
  keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
  level_1_button = telebot.types.KeyboardButton("Уровень 1")
  level_2_button = telebot.types.KeyboardButton("Уровень 2")
  level_3_button = telebot.types.KeyboardButton("Уровень 3")
  keyboard.row(level_1_button)
  keyboard.row(level_2_button)
  keyboard.row(level_3_button)
  bot.send_message(message.chat.id, TEXT_MENU, reply_markup=keyboard)
  bot.register_next_step_handler(message, level_selection)

def generate_random_card():
  value = choice(CARD_NUMBERS)
  suit = choice(CARD_SUIT)
  return value, suit

def level_selection(message):
  value, suit = generate_random_card()
  if message.text == "Уровень 1":
    level_1(message)
  elif message.text == "Уровень 2":
    level_2(message)
  elif message.text == "Уровень 3":
    level_3(message)
  else:
    bot.send_message(message.chat.id, f'К сожалению нет такого уровня:')

def level_1(message):
  show_cart["level_1"] += 1
  keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
  red_button = telebot.types.KeyboardButton("🟥")
  black_button = telebot.types.KeyboardButton("⬛️")
  keyboard.row(red_button, black_button)
  bot.send_message(message.chat.id, "Тебе нужно угадать цвет масти карты: 🟥 или ⬛️", reply_markup = keyboard)
  bot.register_next_step_handler(message, answer_card_level_1)
  
def level_2(message):
  show_cart["level_2"] += 1
  keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
  heart_button = telebot.types.KeyboardButton("♥")
  diamond_button = telebot.types.KeyboardButton("♦")
  spades_button = telebot.types.KeyboardButton("♠")
  club_button = telebot.types.KeyboardButton("♣")
  keyboard.row(heart_button, diamond_button, spades_button, club_button)
  bot.send_message(message.chat.id, "Тебе нужно угадать масть карты: ♥, ♦, ♠, ♣", reply_markup = keyboard)
  bot.register_next_step_handler(message, answer_card_level_2)
  
def level_3(message):
  show_cart["level_3"] += 1
  keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
  for i in range(0, 13):
    heart_button = telebot.types.KeyboardButton(f"{CARD_NUMBERS[i]}♥")
    diamond_button = telebot.types.KeyboardButton(f"{CARD_NUMBERS[i]}♦")
    spades_button = telebot.types.KeyboardButton(f"{CARD_NUMBERS[i]}♠")
    club_button = telebot.types.KeyboardButton(f"{CARD_NUMBERS[i]}♣")
    keyboard.row(heart_button, diamond_button, spades_button, club_button)
  bot.send_message(message.chat.id, "Тебе нужно угадать карту:", reply_markup=keyboard)
  bot.register_next_step_handler(message, answer_card_level_3)

def answer_card_level_1(message):
  level = 1
  value, suit = generate_random_card()
  if message.text == "🟥" and suit in ["♦", "♥"]:
    show_cart["level_1_victory"] += 1
    bot.send_message(message.chat.id, f'Поздравляем! Вы угадали карту: {value}{suit}')
  elif message.text == "⬛️" and suit in ["♠", "♣"]:
    show_cart["level_1_defeat"] += 1
    bot.send_message(message.chat.id, f'Поздравляем! Вы угадали карту: {value}{suit}')
  else:
    show_cart["level_1_defeat"] += 1
    bot.send_message(message.chat.id, f'К сожалению вы не угадали цвет масти карты: {value}{suit}')
  do_you_want_to_continue_playing(message, level)

def answer_card_level_2(message):
  level = 2
  value, suit = generate_random_card()
  if message.text == suit:
    show_cart["level_2_victory"] += 1
    bot.send_message(message.chat.id, f'Поздравляем! Вы угадали карту: {value}{suit}')
  else:
    show_cart["level_2_defeat"] += 1
    bot.send_message(message.chat.id, f'К сожалению вы не угадали масть карты: {value}{suit}')
  do_you_want_to_continue_playing(message, level)

def answer_card_level_3(message):
  level = 3
  value, suit = generate_random_card()
  if message.text == suit:
    show_cart["level_3_victory"] += 1
    bot.send_message(message.chat.id, f'Поздравляем! Вы угадали карту: {value}{suit}')
  else:
    show_cart["level_3_defeat"] += 1
    bot.send_message(message.chat.id, f'К сожалению вы не угадали карту: {value}{suit}')
  do_you_want_to_continue_playing(message, level)

def do_you_want_to_continue_playing(message, level = 0):
  keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
  menu_button = telebot.types.KeyboardButton("Меню")
  show_button = telebot.types.KeyboardButton("Статистика")
  if level != 0:
    continue_button = telebot.types.KeyboardButton("Продолжить")
    keyboard.row(continue_button)
  keyboard.row(show_button)
  keyboard.row(menu_button)
  bot.send_message(message.chat.id, "Хочешь продолжить игру?", reply_markup=keyboard)
  bot.register_next_step_handler(message, do_you_want_to_continue_playing_if, level)

def do_you_want_to_continue_playing_if(message, level = 0):
  if message.text == "Меню":
    menu(message)
  elif message.text == "Статистика":
    show(message)
  elif message.text == "Продолжить":
    match level:
      case 1:
        level_1(message)
      case 2:
        level_2(message)
      case 3:
        level_3(message)
  else:
    bot.send_message(message.chat.id, f'К сожалению нет такой команды:')
    menu(message)

bot.enable_save_next_step_handlers(delay = 2)
bot.load_next_step_handlers()
bot.infinity_polling()