from aiogram import Bot, Dispatcher, types, executor
from fuzzywuzzy import fuzz as f
from fuzzywuzzy import process as p
import logging
import config

from filters import IsAdminFilter

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(is_admin=True, commands=["kick"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply("Пользователь забанен!")

@dp.message_handler(is_admin=True, commands=["del"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.delete_message(config.GROUP_ID, message.reply_to_message.message_id)

@dp.message_handler(is_admin=True, commands=["warn"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.answer("<b>{} {}</b> - вам было вынесено предупреждение!\nПосле нескольких предупреждений вы будете выгнаны".format(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name), parse_mode="html")

@dp.message_handler(is_admin=True, commands=["chatstop"], commands_prefix="!/")
async def stopchat(message: types.Message):
    await message.delete()
    await message.answer("Чат остановлен!\nВсе сообщения после этого будут удаляться!")
    config.stoppedc = True

@dp.message_handler(is_admin=True, commands=["chatrun"], commands_prefix="!/")
async def stopchat(message: types.Message):
    await message.delete()
    await message.answer("Чат запущен!\bПриятного общения :)")
    config.stoppedc = False

@dp.message_handler(commands=["yn"], commands_prefix="!/")
async def yn(message: types.Message):
    inline_btn_1 = types.InlineKeyboardButton('Да - !y', callback_data='y')
    inline_btn_2 = types.InlineKeyboardButton('Нет - !n', callback_data='n')
    inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn_1,inline_btn_2)
    inv = message.text.replace("!yn","").strip()
    await message.delete()
    await message.answer("<b>{} {}</b> предлагает:\n{}\n\nВы можете предложить своё коммандой !yn (предложение)".format(message.from_user.first_name, message.from_user.last_name, inv), parse_mode="html", reply_markup=inline_kb1)

@dp.message_handler(commands=["post"], commands_prefix="!/")
async def post(message: types.Message):
    in1 = types.InlineKeyboardButton('👍', callback_data='like')
    in2 = types.InlineKeyboardButton('👎', callback_data='dislike')
    kb1 = types.InlineKeyboardMarkup().add(in1,in2)
    inv = message.text.replace("!post","").strip()
    await message.delete()
    await message.answer("<b>{} {}</b> создал пост/новость:\n{}".format(message.from_user.first_name, message.from_user.last_name, inv), parse_mode="html", reply_markup=kb1)

@dp.callback_query_handler(lambda c: c.data == "like")
async def likePost(c: types.CallbackQuery):
    await bot.answer_callback_query(c.id, "Ваш лайк отправлен!")

@dp.callback_query_handler(lambda c: c.data == "dislike")
async def dislikePost(c: types.CallbackQuery):
    await bot.answer_callback_query(c.id, "Ваш дислайк отправлен!")

@dp.message_handler(commands=["y"], commands_prefix="!/")
async def iYes(message:types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на предложение!")
        return

    await message.delete()
    await message.answer("<b>{} {}</b> - согласен".format(message.from_user.first_name, message.from_user.last_name), parse_mode="html")

@dp.message_handler(commands=["n"], commands_prefix="!/")
async def iYes(message:types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на предложение!")
        return

    await message.delete()
    await message.answer("<b>{} {}</b> - несогласен".format(message.from_user.first_name, message.from_user.last_name), parse_mode="html")

@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_member(message: types.Message):
    await message.delete()

@dp.message_handler(content_types=["text"])
async def text_handler(message: types.Message):
    #stop chat
    if config.stoppedc:
        await message.bot.delete_message(config.GROUP_ID, message.message_id)

    #helper
    if f.ratio(message.text, "Хочу есть") > 40 or f.ratio(message.text, "Вот бы поесть") > 40 or f.ratio(message.text, "Что поедим?") > 40 or f.ratio(message.text, "Надо заказать") > 40 or f.ratio(message.text, "Можеть поедим?") > 40:
        await message.answer("Мне показалось что вы хотите есть, вот варианты:\n1.Заказать пиццу на Рустерс, Пекарня34, Диливери Клаб, Яндекс Еда, Жар Пицца\n2. Купить шаурму\n3.Заказать роллы или вок на СушиВёсла, СушиДаром, Яндекс Еда, Диливери клаб\n3. Самое простое отварить пельмеши :)")

    #filter of messages
    if f.ratio(message.text, "блять") > 35 or "блять" in message.text:
        await message.delete()
    elif f.ratio(message.text, "сука") > 35 or "сука" in message.text:
        await message.delete()
    if f.ratio(message.text, "пидор") > 35 or "пидор" in message.text:
        await message.delete()
    if f.ratio(message.text, "нахуй") > 35 or "нахуй" in message.text:
        await message.delete()
    if f.ratio(message.text, "ёбанный") > 35 or "ёбанный" in message.text:
        await message.delete()
    if f.ratio(message.text, "ебанный") > 35 or "ебанный" in message.text:
        await message.delete()
    if f.ratio(message.text, "сучара") > 35 or "сучара" in message.text:
        await message.delete()
    if f.ratio(message.text, "еблан") > 35 or "еблан" in message.text:
        await message.delete()
    if f.ratio(message.text, "заебал") > 35 or "заебал" in message.text:
        await message.delete()
    if f.ratio(message.text, "blyat") > 35 or "blyat" in message.text:
        await message.delete()
    if f.ratio(message.text, "pidor") > 35 or "pidor" in message.text:
        await message.delete()
    if f.ratio(message.text, "nahuy") > 35 or "nahuy" in message.text:
        await message.delete()
    if f.ratio(message.text, "nahui") > 35 or "nahui" in message.text:
        await message.delete()
    if f.ratio(message.text, "zaebal") > 35 or "zaebal" in message.text:
        await message.delete()
    if f.ratio(message.text, "fuck") > 35 or "fuck" in message.text:
        await message.delete()
    if f.ratio(message.text, "suck") > 35 or "suck" in message.text:
        await message.delete()
    if f.ratio(message.text, "жопа") > 35 or "жопа" in message.text:
        await message.delete()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
