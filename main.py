from aiogram import Bot, Dispatcher, executor
# Bot - Класс бота, которого вы регестрируете в телеграме по ТОКЕНУ
# Dispatcher - Класс, который следит за ботом, за сигналами (за сообщениями), все что придет боту
# executor - Класс, который запускает диспейчера и зацикливает его (бот работает бесконечно)
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext  # Адрес на локальное хранилище - Оперативка
from aiogram.dispatcher.filters.state import State, StatesGroup  # Группа вопросов и вопросы
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Хранилице в памяти, куда будем сохранять
from configs import *
from keyboards import generate_languages
from googletrans import Translator
import sqlite3



storage = MemoryStorage() # Открываем хранилице
bot = Bot(token=TOKEN, parse_mode='HTML') # Подключитесь к боту в телеграме, и редактирование в виде HTML

dp = Dispatcher(bot, storage=storage) # Объект диспейчера, который будет следить за ботом, сохраняем хранилице

class GetLanguages(StatesGroup): # Создаем последовательность вопросов
    src = State() # С какого языка
    dest = State() # На какой язык
    text = State() # Текст который надо перести


@dp.message_handler(commands=['start', 'about', 'help'])
async def command_start(message: Message):
    if message.text == '/start':
        await message.answer(f'Здравстуйте <b>{message.from_user.full_name}</b>. Я бот переводчик')
        await get_first_language(message)
    elif message.text == '/about':
        await message.answer(f'''Данный бот был создан при поддержке <i>PROWEB</i>
Во время создания бота ни один студент не пострадал''')
    elif message.text == '/help':
        await message.answer('''При возникших проблема или идеях пишите сюда:
<tg-spoiler>@FomichevEvgeniy</tg-spoiler>''')

# Будет 3 вопроса: Выбрать язык с которого перевести, Выбрать язык на который перевести, Сам текст
# Ответы на вопросы надо хранить - State

# @dp.message_handler(lambda message: 'О боте' in message.text)
# @dp.message_handler(regexp='О боте')
async def get_first_language(message: Message):
    await GetLanguages.src.set() # Говорим, что сейчас будет первый вопрос
    await message.answer('Выберите язык с которого хотите перести: ', reply_markup=generate_languages())

#TODO Доделать вопросник. Заимпортировать библиотеку для перевода.
# Сделать базу для сохранения всех переводов пользователей


@dp.message_handler(content_types=['text'], state=GetLanguages.src) # Отлавливаем текст и ответ на 1 вопрос
async def get_second_language(message: Message, state: FSMContext): # Получаем доступ в хранилище
    if message.text in ['/start', '/about', '/help']:
        await command_start(message)
    else:
        # Открыть локальное хранилище(оперативку) и сохранить ответ
        async with state.proxy() as data: # Открываем
            data['src'] = message.text   # Сохраняем
        #await GetLanguages.dest.set()
        await GetLanguages.next() # Следующий вопрос
        await message.answer('Выберите язык на который хотите перевести: ', reply_markup=generate_languages())


@dp.message_handler(content_types=['text'], state=GetLanguages.dest)
async def get_text(message: Message, state: FSMContext):
    if message.text in ['/start', '/about', '/help']:
        await command_start(message)
    else:
        async with state.proxy() as data:
            data['dest'] = message.text
        await GetLanguages.next()
        await message.answer('Введите текст, который хотите перевести', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=['text'], state=GetLanguages.text)
async def translate_function(message: Message, state: FSMContext):
    if message.text in ['/start', '/about', '/help']:
        await command_start(message)
    else:
        async with state.proxy() as data:
            data['text'] = message.text
        await message.answer(f'''Язык с которого вы переводите: {data['src']}
На который {data['dest']}
Текст: {data['text']}''')
        danil = Translator()
        src = get_key(data['src'])
        dest = get_key(data['dest'])


        result = danil.translate(text=data['text'],  # Текст
                                 src= src,  # C какого
                                 dest=dest).text # На какой
        await message.answer(result)
        await state.finish()  # Завершаем опрос
        database = sqlite3.connect('bot.db')
        cursor = database.cursor()

        cursor.execute('''
        INSERT INTO translate(telegram_id, src, dest, original_text, translated_text)
        VALUES (?,?,?,?,?)
        ''', (message.chat.id, src, dest, message.text, result))
        database.commit()
        database.close()




        await get_first_language(message)


executor.start_polling(dp) # Запуск и зацикливание вашего бота




