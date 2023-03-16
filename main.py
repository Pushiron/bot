import asyncio
from aiogram import Bot, Dispatcher, executor, types
from core.settings import CONSOLE_LOG, TOKEN_API, CHAT_ID, VERSION
from api.v1.api import CategoryMenu, GetRequest, promotion
from database.sqlite import db_start, create_user, get_users, get_user_status, save_wallpaper, setRole
from aiogram.utils.exceptions import (MessageCantBeDeleted, MessageToDeleteNotFound)
from contextlib import suppress


bot = Bot(TOKEN_API)


dp = Dispatcher(bot)


wallpaper = ''


SEND = False


NOTE_TITLE = ''


NOTE_BODY = ''


async def on_startup(_):
    await db_start()
    CONSOLE_LOG(1, 'Ultimate Wallpaper Bot готов к работе')


# Функция для удаления сообщения через определенное время
async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


# Функция регистрирует пользователя и отправляет приветственное сообщение
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await create_user(user_id=message.from_user.id, user_name=message.from_user.full_name)
    await bot.send_message(message.chat.id, 'Привет! Я бот приложения Ultimate Wallpapers! Отправь мне изображение\n'
                                            'и я перешлю его модераторам, для того, чтобы они проверили его.\n'
                                            'Если изображение будет одобрено, то оно будет добавлено в приложение =)\n'
                                            'Если есть вопросы, напиши /help')


# Функция для отправки уведомлений пользователю
@dp.message_handler(commands=['note'])
async def send_notification(message: types.Message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin == True:
        users = await get_users()
        msg = message.text.split(" ", 1)
        if len(msg) > 1:
            if len(msg[1]) >= 10:
                for user in users:
                    await bot.send_message(user[0], f'Уведомление от команды Ultimate Wallpapers:\n{msg[1]}')
            else:
                await bot.send_message(CHAT_ID, 'Текст уведомления не может быть меньше 10 символов')
        else:
            await bot.send_message(CHAT_ID, 'Вы не указали текст уведомления. Пример команды\n'
                                            '/note <message>')


@dp.message_handler(commands=['makeadmin'])
async def make_admin(message: types.Message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin == True:
        msg = message.text.split(" ", 1)
        if len(msg) > 1 and len(msg[1]) > 3:
            await setRole(msg[1], 1)
            await bot.send_message(CHAT_ID, f'Пользователь {msg[1]} назначен администратором')


@dp.message_handler(commands=['makeuser'])
async def make_admin(message: types.Message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin == True:
        msg = message.text.split(" ", 1)
        if len(msg) > 1 and len(msg[1]) > 3:
            if msg[1] == '645755081':
                await bot.send_message(message.chat.id, 'Нахуй пошел')
            else:
                await setRole(msg[1], 0)
                await bot.send_message(CHAT_ID, f'Пользователь {msg[1]} разжалован')



@dp.message_handler(commands=['list'])
async def set_user_role(message: types.Message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin == True:
        msg = message.text.split(" ", 1)
        if len(msg) > 1 and len(msg[1]) == 2 and msg[1] == '-u':
            users = await get_users()
            for user in users:
                if user[2] == 1:
                    role = 'Администратор'
                else:
                    role = 'Пользователь'
                await bot.send_message(message.chat.id, f"Пользователь: {user[1]};\nUID: {user[0]};\nРоль: {role}")


@dp.message_handler(commands=['help'])
async def help_comma(message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin==True:
        msg = message.text.split(" ", 1)
        if len(msg) > 1:
            if msg[1] == 'note':
                msg = await bot.send_message(CHAT_ID, 'Команда /note <!message>\n'
                                                'Команда имеет параметр "message", который обязателен \n'
                                                'для заполнения и должен содержать минимум 10 символов'
                                                '\n'
                                                'Команда отпраляет сообщение содержащееся в message\n'
                                                'всем пользователям бота')
                asyncio.create_task(delete_message(msg, 60))
            elif msg[1] == 'accept':
                msg = await bot.send_message(CHAT_ID, 'Команда /accept {!reply_to_message}\n'
                                                'Команда не имеет параметров, но обязана быть использована \n'
                                                'в качестве ответа на изображение от пользователя'
                                                '\n'
                                                'Команда отпраляет пользователю сообщение о том, что его\n'
                                                'изображение одобрено и добавлено в библиотеку. \n'
                                                '!!!ВНИМАНИЕ!!!\n'
                                                'Команду необходимо использовать ПОСЛЕ добавления изображения в '
                                                'библиотеку, так как она удаляет сообщение с изображением')
                asyncio.create_task(delete_message(msg, 60))
            elif msg[1] == 'decline':
                msg = await bot.send_message(CHAT_ID, 'Команда /decline {!reply_to_message} <message>\n'
                                                'Команда имеет параметр "message", который обязателен\n'
                                                'для заполнения и должен содержать минимум 5 символов,\n'
                                                'и обязана быть использована в качестве ответа на изображение,'
                                                'полученное от пользователя'
                                                '\n'
                                                'Команда отправляет пользователю сообщение о том, что его\n'
                                                'изображение отклонено и причину, содержащуюся в message. \n'
                                                '!!!ВНИМАНИЕ!!!\n'
                                                'Команда удаляет сообщение с изображением')
                asyncio.create_task(delete_message(msg, 60))
            elif msg[1] == 'list':
                msg = await bot.send_message(CHAT_ID, 'Команда /list {argument} \n'
                                                'Команда имеет аргументы, которые обязательны\n'
                                                'для заполнения.\n'
                                                '\n'
                                                '-u - Выводит список всех пользователей')
                asyncio.create_task(delete_message(msg, 60))
            elif msg[1] == 'setrole':
                msg = await bot.send_message(CHAT_ID, 'Команда /makeadmin {user_id} \n'
                                                'Команда имеет аргумент, которые обязателен\n'
                                                'для заполнения.\n'
                                                '\n'
                                                'user_id - id пользователя. Узнать можно через команду /list -u')
                asyncio.create_task(delete_message(msg, 60))
        else:
            msg = await bot.send_message(CHAT_ID, 'Команды администратора:\n'
                                            '/bot_version - Выводит текущую версию бота\n'
                                            '/adminreaction - Выводит реакции для установки статуса работы '
                                            'над изображением\n'
                                            '/accept {!reply_to_message} - обои приняты. '
                                            'Пользователь получает уведомление об этом\n'
                                            '/decline {!reply_to_message} <!message (5)> - Обои '
                                            'отклонены. Пользоватль получает уведомление об этом \n'
                                            '/note <!message (10)> - Отправляет уведомление с заданным параметром '
                                            '<message> всем пользователям\n'
                                            '*! - параметр является обязательным\n'
                                            '*(5) - минимальная длинна параметра')
            asyncio.create_task(delete_message(msg, 60))
    else:
        await bot.send_message(message.chat.id, 'Отправь ине изображение с размерами минимум 590px или '
                                                '1080px по ширине\n'
                                                'и 860px или 1920px по высоте\n'
                                                'Преимущество отдаем изображениям с размерами от 1080х1920')


@dp.message_handler(commands=['adminreaction'])
async def adminreaction(message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin==True:
        msg = await bot.send_message(message.chat.id, '👍 - Начал загружать обои\n\n'
                                                '👎 - Обои отклонены')
        asyncio.create_task(delete_message(msg, 10))


@dp.message_handler(commands=['start_promotion'])
async def start_promotion(message: types.Message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin==True:
        msg = message.text.split(" ", 1)
        if len(msg) > 1:
            if len(msg[1]) > 0:
                await promotion(True)
                await bot.send_message(CHAT_ID, 'Акция началась, все premium обои перешли в статус обычных')
                msg = f'{msg[1]}\nНачалась акция! Все премиум обои теперь можно установить без просмотра рекламы!'
                users = await get_users()
                for user in users:
                    await bot.send_message(user[0], f'Уведомление от команды Ultimate Wallpapers:\n{msg}')
        else:
            await promotion(True)
            await bot.send_message(CHAT_ID, 'Акция началась, все premium обои перешли в статус обычных')
            msg = f'Началась акция! Все премиум обои теперь можно установить без просмотра рекламы!'
            users = await get_users()
            for user in users:
                await bot.send_message(user[0], f'Уведомление от команды Ultimate Wallpapers:\n{msg}')


@dp.message_handler(commands=['end_promotion'])
async def start_promotion(message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin==True:
        await promotion(False)
        await bot.send_message(CHAT_ID, 'Акция окончена, все premium обои перешли в статус premium')
        msg = 'Акция закончилась! Все премиум обои теперь вновь требуют просмотра рекламы!'
        users = await get_users()
        for user in users:
            await bot.send_message(user[0], f'Уведомление от команды Ultimate Wallpapers:\n{msg}')


@dp.message_handler(commands=['bot_version'])
async def bot_version(message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin==True:
        msg = await bot.send_message(message.chat.id, VERSION)
        asyncio.create_task(delete_message(msg, 10))


@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    global SEND
    global wallpaper
    wallpaper = await save_wallpaper(message.from_user.id, message.photo[-1].file_id)
    SEND = True
    await message.reply('Отлично, а теперь давай выберем категорию. Если нужной категории нет,'
                        ' то придумай свою', reply_markup=await CategoryMenu(await GetRequest()))


@dp.message_handler(commands=['accept'])
async def accept(message: types.Message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin==True:
        if message.reply_to_message != None:
            if len(message.reply_to_message.photo) != 0:
                user = message.reply_to_message.caption.split()
                msg = await bot.send_message(CHAT_ID, 'Уведомление доставлено пользователю')
                await bot.delete_message(chat_id=CHAT_ID, message_id=message.reply_to_message.message_id)
                await bot.send_photo(chat_id=user[1],
                                     photo=message.reply_to_message.photo[-1].file_id,
                                     caption='Ваши обои одобрены и добавлены в библиотеку')
                asyncio.create_task(delete_message(msg, 10))
            else:
                msg = await bot.send_message(CHAT_ID,
                                       'Команда может быть использована только в качестве ответа на изображение')
                asyncio.create_task(delete_message(msg, 10))
        else:
            msg = await bot.send_message(CHAT_ID, 'Команда может быть использована только '
                                                  'в качестве ответа на изображение')
            asyncio.create_task(delete_message(msg, 10))

@dp.message_handler(commands=['decline'])
async def decline(message):
    isAdmin = await get_user_status(message.from_user.id)
    if isAdmin==True:
        if message.reply_to_message != None:
            if len(message.reply_to_message.photo) != 0:
                msg = message.text.split(" ", 1)
                if len(msg) > 1:
                    reason = msg[1]
                    if len(msg[1]) >= 5:
                        user = message.reply_to_message.caption.split()
                        msg = await bot.send_message(CHAT_ID, 'Уведомление доставлено пользователю')
                        await bot.delete_message(chat_id=CHAT_ID, message_id=message.reply_to_message.message_id)
                        await bot.send_photo(chat_id=user[1],
                                             photo=message.reply_to_message.photo[-1].file_id,
                                             caption=f'Ваши обои отклонены по причине:\n{reason}')
                        asyncio.create_task(delete_message(msg, 10))
                    else:
                        msg = await bot.send_message(CHAT_ID, 'Слишком мало информации о причине для пользователя')
                        asyncio.create_task(delete_message(msg, 10))
                else:
                    msg = await bot.send_message(CHAT_ID, 'Не указана причина')
                    asyncio.create_task(delete_message(msg, 10))
            else:
                msg = await bot.send_message(CHAT_ID,
                                       'Команда может быть использована только в качестве ответа на изображение')
                asyncio.create_task(delete_message(msg, 10))
        else:
            msg = await bot.send_message(CHAT_ID, 'Команда может быть использована только '
                                                  'в качестве ответа на изображение')
            asyncio.create_task(delete_message(msg, 10))


@dp.message_handler(content_types=['text'])
async def send_category(message: types.Message):
    if SEND:
        await bot.send_message(message.from_user.id, f'Категория: {message.text}')
        await send_to_admins(message)
    else:
        await bot.send_message(message.from_user.id, 'Для начала отправь мне изображение')


async def send_to_admins(message):
    global SEND
    if SEND:
        await bot.send_photo(chat_id=CHAT_ID, photo=wallpaper[1],
                             caption=f'Пользователь {wallpaper[0]} определил категорию {message.text}')
        await bot.send_message(message.chat.id,
                               'Спасибо! Я отправил твоё изображение модераторам. Можешь отправить еще!')
        CONSOLE_LOG(1, f'Пользователь {message.from_user.username} отправил фото')
        CONSOLE_LOG(1, 'Изображение получено модераторами')
        SEND = False


@dp.message_handler(content_types=['text', 'sticker', 'pinned_message', 'audio'])
async def get_another(message):
    await message.answer('Отправь мне пожалуйста изображение')
    CONSOLE_LOG(1, 'Пользователь отправил что-то иное')


async def on_shutdown(_):
    CONSOLE_LOG(1, 'Ultimate Wallpaper Bot завершил работу')


executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
