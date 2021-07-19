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
    f = open("./kick.jpg", "rb")
    await message.reply_to_message.reply("Пользователь кикнут!")
    await bot.send_photo(message.chat.id, f)
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

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

@dp.message_handler(commands=["like"], commands_prefix="!/")
async def likePerson(message: types.Message):
    if not message.reply_to_message:
        await message.bot.delete_message(config.GROUP_ID, message.message_id)
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.answer("Пользователь {} {} поставил 👍 {} {}".format(message.from_user.first_name,message.from_user.last_name, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name))

@dp.message_handler(commands=["dislike"], commands_prefix="!/")
async def likePerson(message: types.Message):
    if not message.reply_to_message:
        await message.bot.delete_message(config.GROUP_ID, message.message_id)
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.answer("Пользователь {} {} поставил 👎 {} {}".format(message.from_user.first_name,message.from_user.last_name, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name))

@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_member(message: types.Message):
    await message.delete()

@dp.message_handler(content_types=["text"])
async def text_handler(message: types.Message):
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
