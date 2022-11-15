from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def on_startup(_):   #действия при старте
    print("Bot Online")

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\n Это тестовый бот для записи\n Для начала, давайте познакомимся! ")



@dp.message_handler(commands='contacts')
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=4)
    # default row_width is 3, so here we can omit it actually
    # kept for clearness

    text_and_data = (
        ('УК', 'yes'),
        ('Инженер', 'no'),
    )
    # in real life for the callback_data the callback data factory should be used
    # here the raw string is used for the simplicity
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup.row(*row_btns)
    keyboard_markup.add(
        # url buttons have no callback data
        types.InlineKeyboardButton('Написать', url='dompkbot.t.me'),
    )  

    await message.reply('Для получения контактов нажмите "Написать"', reply_markup=keyboard_markup)


# Use multiple registrators. Handler will execute when one of the filters is OK
@dp.callback_query_handler(text='no')  # if cb.data == 'no'
@dp.callback_query_handler(text='yes')  # if cb.data == 'yes'
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    await query.answer(f'You answered with {answer_data!r}')

    if answer_data == 'yes':
        text = '+7(343)37-999-39'
        print('Нажали УК')
    elif answer_data == 'no':
        text = '+7(908)636-53-03'
        print('Нажали Инженер')
    else:
        text = f'Unexpected callback data {answer_data!r}!'
    


    await bot.send_message(query.from_user.id, text)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup = on_startup, skip_updates=True)