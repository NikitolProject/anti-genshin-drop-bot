from typing import Optional

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from src.events import bot, dp, logging
from src.database.api import YouTuber


# States
class YouTuberForm(StatesGroup):
    username = State()
    url = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """

    hello_button = InlineKeyboardButton('Добавить ютубера в список', callback_data="greetings_callback")
    greetings_keyboard_markup = InlineKeyboardMarkup()
    greetings_keyboard_markup.add(hello_button)

    await message.reply(
        "Привет! Если ты знаешь ютубера, который рекламировал помойку Genshin Drop и прочие "
        "говно рулетки, связанные с геншином - просим помочь нам и пополнить список таких же ютуберов! "
        "Просто нажми на кнопку и следуй инструкциям от бота, а мы сами проверим ролики ютубера и убедимся "
        "в его причастности к рекламе помоечных сервисов.",
        reply_markup=greetings_keyboard_markup
    )


@dp.callback_query_handler(text='greetings_callback')
async def process_greetings_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await YouTuberForm.username.set()

    await bot.send_message(
        callback_query.from_user.id,
        text = "Введи ник ютубера, которого собираешься добавить в список, в этот чат"
    )


@dp.message_handler(state=YouTuberForm.username)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process youtuber username
    """
    async with state.proxy() as data:
        data['username'] = message.text

    await YouTuberForm.next()
    await message.reply("Теперь введи ссылку на ютуб канал этого человека")


@dp.message_handler(lambda message: not any((message.text.startswith("http://"), message.text.startswith("https://"))), state=YouTuberForm.url)
async def process_url_invalid(message: types.Message):
    """
    Process user url invalid
    """
    return await message.reply("Введи настоящую ссылку, пожалуйста")


@dp.message_handler(lambda message: any((message.text.startswith("http://"), message.text.startswith("https://"))), state=YouTuberForm.url)
async def process_url(message: types.Message, state: FSMContext):
    """
    Process youtuber url
    """
    async with state.proxy() as data:
        YouTuber.create(username=data['username'], url=message.text)

    await state.finish()

    await message.reply("Спасибо за помощь! Теперь информация о данном ютубере будет проверяться нашими модераторами и в последующем занесён в список.")
