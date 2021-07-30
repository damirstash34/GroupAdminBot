from aiogram import Bot, Dispatcher, types, executor
from fuzzywuzzy import fuzz as f
from fuzzywuzzy import process as p
import logging
import config
import json
import os
import asyncio

from filters import IsAdminFilter

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
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

@dp.message_handler(commands=["del"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return
    
    stat = open("./stats/"+str(message.from_user.id)+".json", "r+")
    stats = json.load(stat)
    if stats["status"] < 1:
        await bot.send_message(message.from_user.id, "У вас нет на это прав!")
        return

    stat.close()
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.delete_message(config.GROUP_ID, message.reply_to_message.message_id)

@dp.message_handler(is_admin=True, commands=["warn"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return

    username = message.from_user.id
    stat = open("./stats/" + str(username) + ".json", "r")
    stats = json.load(stat)
    wrn_counts = stats["warns"]
    stats["warns"] = wrn_counts
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.answer("<b>{} {}</b> - вам было вынесено предупреждение!\nПосле 3-х вы будете выгнаны!\n\n{}/3".format(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name, stats["warns"]), parse_mode="html")
    stat.close()

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

@dp.message_handler(commands=["dislike"], commands_prefix="!/")
async def dislikeUser(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.answer("{} {} - поставил дизлайк {} {}".format(message.from_user.first_name, message.from_user.last_name, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name))
    stat_file = open("./stats/" + str(message.reply_to_message.from_user.id) + ".json", "r+")
    user_stat = json.load(stat_file)
    user_stat["likes"] -= 1
    stat_file.seek(0)
    stat_file.truncate()
    json.dump(user_stat, stat_file)
    stat_file.close()

@dp.message_handler(commands=["like"], commands_prefix="!/")
async def likeUser(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.answer("{} {} - поставил лайк {} {}".format(message.from_user.first_name, message.from_user.last_name, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name))
    stat_file = open("./stats/" + str(message.reply_to_message.from_user.id) + ".json", "r+")
    user_stat = json.load(stat_file)
    user_stat["likes"] += 1
    stat_file.seek(0)
    stat_file.truncate()
    json.dump(user_stat, stat_file)
    stat_file.close()

@dp.message_handler(commands=["stat"], commands_prefix="!/")
async def statistic(message: types.Message):
    group = message.chat.title
    stat_file = open("./stats/" + str(message.from_user.id) + ".json", "r+")
    user_stat = json.load(stat_file)
    likes = user_stat["likes"]
    muted = user_stat["mute"]
    warns = user_stat["warns"]
    await message.delete()
    await bot.send_message(message.from_user.id, "Ваша статистика в группе <u>{}</u>:\nНикнейм: <b>{}</b>\nЛайки: <b>{}</b>\nПредупреждения: <b>{}/3</b>\nСтатус мута: <b>{}</b>".format(group, message.from_user.username,str(likes), str(warns), str(muted)), parse_mode="html")
    stat_file.close()

@dp.message_handler(is_admin=True, commands=["mute"], commands_prefix="!/")
async def mute(message: types.Message):
    if message.reply_to_message:
        await message.bot.delete_message(config.GROUP_ID, message.message_id)
        stat_file = open("./stats/" + str(message.reply_to_message.from_user.id) + ".json", "r+")
        user_stat = json.load(stat_file)
        user_stat["mute"] = 1
        stat_file.seek(0)
        stat_file.truncate()
        json.dump(user_stat, stat_file)
        stat_file.close()
        await message.answer("Пользователь {} получил мут".format(message.reply_to_message.from_user.username))
    else:
        await message.bot.delete_message(config.GROUP_ID, message.message_id)
        inv = message.text.replace("!mute","").strip()
        stat_file = open("./stats/" + inv + ".json", "r+")
        user_stat = json.load(stat_file)
        user_stat["mute"] = 1
        stat_file.seek(0)
        stat_file.truncate()
        json.dump(user_stat, stat_file)
        stat_file.close()
        await message.answer("Пользователь {} получил мут".format(inv))

@dp.message_handler(commands=["mute"], commands_prefix="!/")
async def mute(message: types.Message):
    stat = open("./stas/"+str(message.from_user.id)+".json", "r+")
    stats = json.load(stat)
    if stats["status"] < 2:
        await bot.send_message(message.from_user.id, "У вас нет на это прав!")
        return

    stat.close()

    if message.reply_to_message:
        await message.bot.delete_message(config.GROUP_ID, message.message_id)
        stat_file = open("./stats/" + str(message.reply_to_message.from_user.id) + ".json", "r+")
        user_stat = json.load(stat_file)
        user_stat["mute"] = 1
        stat_file.seek(0)
        stat_file.truncate()
        json.dump(user_stat, stat_file)
        stat_file.close()
        await message.answer("Пользователь {} получил мут".format(message.reply_to_message.from_user.username))
    else:
        await message.bot.delete_message(config.GROUP_ID, message.message_id)
        inv = message.text.replace("!mute","").strip()
        stat_file = open("./stats/" + inv + ".json", "r+")
        user_stat = json.load(stat_file)
        user_stat["mute"] = 1
        stat_file.seek(0)
        stat_file.truncate()
        json.dump(user_stat, stat_file)
        stat_file.close()
        await message.answer("Пользователь {} получил мут".format(inv))

@dp.message_handler(is_admin=True, commands=["unmute"], commands_prefix="!/")
async def mute(message: types.Message):
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    inv = message.text.replace("!unmute","").strip()
    stat_file = open("./stats/" + inv + ".json", "r+")
    user_stat = json.load(stat_file)
    user_stat["mute"] = 0
    stat_file.seek(0)
    stat_file.truncate()
    json.dump(user_stat, stat_file)
    stat_file.close()
    await message.answer("Пользователь {} может снова общаться!".format(inv))

@dp.message_handler(commands=["unmute"], commands_prefix="!/")
async def mute(message: types.Message):
    stat = open("./stas/"+str(message.from_user.id)+".json", "r+")
    stats = json.load(stat)
    if stats["status"] < 2:
        await bot.send_message(message.from_user.id, "У вас нет на это прав!")
        return

    stat.close()
    
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    inv = message.text.replace("!unmute","").strip()
    stat_file = open("./stats/" + inv + ".json", "r+")
    user_stat = json.load(stat_file)
    user_stat["mute"] = 0
    stat_file.seek(0)
    stat_file.truncate()
    json.dump(user_stat, stat_file)
    stat_file.close()
    await message.answer("Пользователь {} может снова общаться!".format(inv))

@dp.message_handler(commands=["yn"], commands_prefix="!/")
async def yn(message: types.Message):
    inline_btn_1 = types.InlineKeyboardButton('Да - !y', callback_data='y')
    inline_btn_2 = types.InlineKeyboardButton('Нет - !n', callback_data='n')
    inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn_1,inline_btn_2)
    inv = message.text.replace("!yn","").strip()
    await message.delete()
    await message.answer("<b>{} {}</b> предлагает:\n{}\n\nВы можете предложить своё коммандой !yn (предложение)".format(message.from_user.first_name, message.from_user.last_name, inv), parse_mode="html", reply_markup=inline_kb1)

@dp.message_handler(is_admin=True, commands=["lvl"], commands_prefix="!/")
async def chnglevel(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return
    
    inv = message.text.replace("!lvl","").strip()
    stat_file = open("./stats/"+str(message.reply_to_message.from_user.id)+".json", "r+")
    user_stat = json.load(stat_file)
    user_stat["status"] = str(inv)
    stat_file.seek(0)
    stat_file.truncate()
    json.dump(user_stat, stat_file)
    await message.delete()
    if inv == "1":
        await message.answer("Теперь у пользователя {} {} привилегия = DELETER\nDELETER - может удалять сообщения".format(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name))
    elif inv == "2":
        await message.answer("Теперь у пользователя {} {} привилегия = MUTER\nMUTER - может удалять сообщения + вводить пользователей в режим чтения".format(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name))
    elif inv == "0":
        await message.answer("Теперь у пользователя {} {} привилегия = MEMBER\n MEMBER может только общаться в чате".format(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name))
    else:
        await bot.send_message(message.from_user.id, "Неизвестный уровень {}!".format(inv))
    
    stat_file.close()

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

@dp.message_handler(commands=["delme"], commands_prefix="!/")
async def delme(message: types.Message):
    username = message.from_user.id
    os.remove("./stats/" + str(username) + ".json")
    await message.delete()
    await message.answer("Пользователь {} был удалён!".format(message.from_user.username))

@dp.message_handler(commands=['report', 'rep'], commands_prefix="!/")
async def report_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на сообщение!")
        return
    
    rep_owner = message.from_user.first_name + " " + message.from_user.last_name + " - " + str(message.from_user.id)
    rep_cut = message.text.replace("!report","").strip()
    rep_n = rep_cut.replace("!rep", "").strip()
    to_rep = message.reply_to_message.from_user.first_name + " " + message.reply_to_message.from_user.last_name + " - " + str(message.reply_to_message.from_user.id)
    rep_msg = "Получен репорт от: <b>{}</b>\nРепорт на: <b>{}</b>\nПричина репорта: <em>{}</em>".format(rep_owner, to_rep, rep_n)
    await message.delete()
    await bot.send_message(config.forReportId, rep_msg, parse_mode="html")
    


@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_member(message: types.Message):
    await message.delete()

@dp.message_handler(content_types=["text"])
async def text_handler(message: types.Message):

    #reg new user
    try:
        userid = message.from_user.id
        stat = open("./stats/" + str(userid) + ".json", "r")
        stats = json.load(stat)
        if stats["mute"] == 1:
            await message.delete()
        if stats["warns"] >= 3:
            await message.answer("{} {} - число предупреждений достигло 3-х!\nСейчас вы будете выгнаны!")
            await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.from_user.id)


        stat.close()
    except:
        userid = message.from_user.id
        user_stat = {
            "username": message.from_user.username,
            "id": userid,
            "mute": 0,
            "likes": 0,
            "warns": 0,
            "status": 0
        }

        # status:
        # 0 - member
        # 1 - deleter
        # 2 - muter


        new_user = open("./stats/" + str(userid) + ".json", "w+")
        json.dump(user_stat, new_user)
        new_user.close()
        await message.answer("Зарегистрирован новый пользователь - <b>{} {}</b>".format(message.from_user.first_name, message.from_user.last_name), parse_mode="html")
        goose = open(config.helloIMG, "rb")
        await bot.send_photo(message.chat.id, goose)
        goose.close()

    #hello
    if f.ratio(message.text, "Привет") > 50:
        goose = open(config.helloIMG, "rb")
        await bot.send_photo(message.chat.id, goose)
        goose.close()
    if f.ratio(message.text, "Здравствуйте") > 50:
        goose = open(config.helloIMG, "rb")
        await bot.send_photo(message.chat.id, goose)
        goose.close()
    if f.ratio(message.text, "Дарова") > 50:
        goose = open(config.helloIMG, "rb")
        await bot.send_photo(message.chat.id, goose)
        goose.close()


    #stop chat
    if config.stoppedc:
        await message.bot.delete_message(config.GROUP_ID, message.message_id)

    #helper
    if f.ratio(message.text, "Хочу есть") > 40 or f.ratio(message.text, "Вот бы поесть") > 40 or f.ratio(message.text, "Что поедим?") > 40 or f.ratio(message.text, "Надо заказать") > 40 or f.ratio(message.text, "Можеть поедим?") > 40:
        await message.answer("Мне показалось что вы хотите есть, вот варианты:\n1.Заказать пиццу на Рустерс, Пекарня34, Диливери Клаб, Яндекс Еда, Жар Пицца\n2. Купить шаурму\n3.Заказать роллы или вок на СушиВёсла, СушиДаром, Яндекс Еда, Диливери клаб\n3. Самое простое отварить пельмеши :)")

    #filter of messages
    msg_filter = """if f.ratio(message.text, "блять") > 35 or "блять" in message.text:
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
        await message.delete()"""


#long polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
