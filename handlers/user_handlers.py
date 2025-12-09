import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject, and_f, invert_f
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from utils.transfer_funcs import transfer_stars
from database.action_data_class import DataInteraction
from states.state_groups import startSG, adminSG

from config_data.config import Config, load_config


emojies = {
    '🎰': 'slots',
    '🎲': 'cube',
    '🎯': 'darts',
    '⚽': 'football',
    '🏀': 'basketball',
    '🎳': 'bowling'
}


topics = {
    '🎰': 31,
    '🎲': 26,
    '🎯': 30,
    '⚽': 24,
    '🏀': 22,
    '🎳': 47
}

topics_list = [31, 26, 30, 24, 22, 47]


user_router = Router()

config: Config = load_config()


@user_router.message(CommandStart(), F.chat.type == 'private')
async def start_dialog(msg: Message, dialog_manager: DialogManager, session: DataInteraction, command: CommandObject):
    admins = [*config.bot.admin_ids]
    admins.extend([admin.user_id for admin in await session.get_admins()])
    if msg.from_user.id in admins:
        await dialog_manager.start(state=adminSG.start, mode=StartMode.RESET_STACK)


@user_router.message(F.dice, invert_f(F.forward_from), invert_f(F.forward_from_chat), F.chat.id == config.bot.chat_id, F.message_thread_id.in_(topics_list))
async def handle_dice(msg: Message, session: DataInteraction):
    user_id = msg.from_user.id
    dice = msg.dice
    topic_id = msg.message_thread_id

    await session.add_static_value('spent', 25)

    emoji = dice.emoji
    value = dice.value

    print(f"Эмодзи: {emoji}, Значение: {value}")

    if not topics[emoji] or topics[emoji] != topic_id:
         await msg.delete()
         return

    prize = None
    if emoji == "🎲":  # Обычный кубик
        if value == 6:
            await msg.reply("<b>🎲 Вы настоящий везунчик! 🎲</b>\n\n<b>⭐️ Попробуйте удачу ещё раз и получите "
                            "<em>бонус 60⭐️</em></b>\n<b>Играйте и наслаждайтесь!</b>")
            prize = 60

    elif emoji == '🎰':
        touches = await session.get_user_touches(user_id, emojies[emoji], value)
        if value == 64:  # семерки
            await msg.reply('<b>🎊 Крупный выигрыш! 🎉</b> Вы сорвали <b>NFT-подарок</b>, '
                            '<em>для его получения напишите менеджеру: @CybersSupport</em>')
            return
        elif value == 22:  # виноград
            if not touches:
                await msg.reply('<b>💣 Джекпот эмоций! 💣</b>\n\n<b><em><u>⭐️ Ваша награда: 55⭐️</u></em></b>\n'
                                '<b>Испытайте удачу ещё раз и почувствуйте вкус победы! 😎</b>')
                prize = 55
            elif len(touches) == 1:
                await msg.reply('<b>🏆 Фортуна на вашей стороне! 🏆</b>\n\n<b><em>⭐️ Бонус: 65⭐️</em></b>\n'
                                '<b>Продолжайте путь к вершинам успеха! ☝️</b>')
                prize = 65
            else:
                await msg.reply('<b>🍬 Сладкий вкус победы! 🍬</b>\n\n⭐️ <b><em>Повторите успех с бонусом 75⭐️!</em></b>')
                prize = 75
                await session.del_touches_by_value(user_id, emojies[emoji], value)
        elif value == 43:  # лимон
            if not touches:
                await msg.reply('<b>🎰 Удача улыбнулась! 🎰</b>\n\n<b><em>⭐️ Ваш бонус: 55⭐️</em></b>\n'
                                'Продолжайте играть и везти! 🍀')
                prize = 55
            elif len(touches) == 1:
                await msg.reply('<b>💪 Очередная победа! 💪</b>\n\nПонравилась игра?\n<b>⭐️ Увеличьте шансы</b> на крупный приз '
                                '<b><em>с бонусом 65⭐️!</em></b>')
                prize = 65
            else:
                await msg.reply('<b>💥 Невероятный успех! 💥</b>\n\n⭐️ <b><em><u>Повторите триумф с бонусом 75⭐️!</u></em></b>\n'
                                'Делайте ставки увереннее и <b><em>выигрывайте больше!</em></b>')
                prize = 75
                await session.del_touches_by_value(user_id, emojies[emoji], value)
        elif value == 1:  # бар
            if not touches:
                await msg.reply('<b>🌊 Волна удачи на подходе! 🌊</b>\n\n<b><em>⭐️ Заберите бонус 50⭐️</em> и '
                                'продолжайте игру!</b>\nГотовы поймать большую волну? 🍀')
                prize = 50
            elif len(touches) == 1:
                await msg.reply('<b>🚀 Старт дан — к победе! 🚀</b>\n\n<b>⭐️ Вперёд к новым высотам с '
                                '<em>бонусом 55⭐️!</em></b>')
                prize = 55
            else:
                await msg.reply('<b>😎🛠 Становитесь мастером игры! 🛠😎</b>\n\n⭐️ <b><em><u>Забирайте 65⭐️!</u></em></b>\n'
                                '<b>Чем активнее играете, тем ближе крупный выигрыш!</b>')
                prize = 65
                await session.del_touches_by_value(user_id, emojies[emoji], value)

    elif emoji == "🎯":  # Дартс
        touches = await session.get_user_touches(user_id, emojies[emoji], value)
        if value == 6:
            if not touches:
                await msg.reply('<b>🔥 Добро пожаловать в клуб победителей! 🔥</b>\n\n<b><em>Ваш бонус: '
                                '60⭐️</em></b> — вы теперь наш VIP-гость!')
                prize = 60
            elif len(touches) == 1:
                await msg.reply('<b>✨ Искры успеха зажглись! ✨</b>\n\n<b><em>⭐️ Бонус 50⭐️ спешит к герою! </em></b>\n'
                                '🔥 Зарядитесь энергией — следующая победа уже близко! 🔥')
                prize = 50
            else:
                await msg.reply('<b>✨ Золотой дождь удачи! ✨</b>\n\n<b>Ощутите мощь своей фортуны '
                                '<em>с бонусом 65⭐️!</em></b>')
                prize = 65
                await session.del_touches_by_value(user_id, emojies[emoji], value)

    elif emoji == "🎳":  # боулинг
        touches = await session.get_user_touches(user_id, emojies[emoji], value)
        if value == 6:
            await msg.reply('<b>🏆 Фортуна выбрала <u>именно вас!</u> 🏆</b>\n\n<b><em><u>⭐️ Ваш бонус: 50⭐️</u></em></b>\n'
                            '<b>🤑 Начинайте восхождение к вершинам успеха! 🤑</b>')
            prize = 50
            await session.del_touches_by_value(user_id, emojies[emoji], value)

    elif emoji == "⚽":  # Футбол
        if value in [4, 5]:
            touches = [*(await session.get_user_touches(user_id, emojies[emoji], 4)), *(await session.get_user_touches(user_id, emojies[emoji], 5))]
            await session.add_touch(user_id, emojies[emoji], value)
            if not touches:
                await msg.reply("<b>🦁 Победители не сбавляют темп! 🦁</b> <b>Забейте ещё один гол и получите 55⭐️</b>")
                return
            await msg.reply('<b>👑 Корона победителя ваша! 👑</b>\n\n<b><em><u>⭐️ Забирайте бонус 55⭐️!</u></em></b>\n'
                            '<b>Докажите, кто настоящий король игры! 👑</b>')
            prize = 55
            await session.del_touches_by_value(user_id, emojies[emoji], value)
        else:
            await session.del_touches_by_value(user_id, emojies[emoji], value)

    elif emoji == "🏀":  # Баскетбол
        if value in [4, 5]:
            touches = [*(await session.get_user_touches(user_id, emojies[emoji], 4)), *(await session.get_user_touches(user_id, emojies[emoji], 5))]
            await session.add_touch(user_id, emojies[emoji], value)
            if not touches:
                await msg.reply("<b>🦁 Победители не останавливаются! 🦁</b> <b>Забросьте ещё один мяч и получите 55⭐️</b>")
                return
            await msg.reply('<b>🦁 Победители идут до конца! 🦁</b>\n\n<b><em>С бонусом 55⭐️</em> ваша игровая карьера '
                            'станет легендой!</b>\n🎉 Бонус уже в пути!\n\n<b>Забрасывайте мячи и выигрывайте ещё ⭐️</b>')
            prize = 55
            await session.del_touches_by_value(user_id, emojies[emoji], value)
        else:
            await session.del_touches_by_value(user_id, emojies[emoji], value)

    if prize:
        await session.add_static_value('payouts', prize)
        if emojies[emoji] not in ['basketball', 'football']:
            await session.add_touch(user_id, emojies[emoji], value)
        await session.add_victory(msg.from_user.id, msg.from_user.full_name, msg.from_user.username, prize)
        status = False
        counter = 0
        while not status:
            status = await transfer_stars(msg.from_user.username, prize)
            await asyncio.sleep(5)
            counter += 1
            if counter >= 5:
                break


# @user_router.message(F.chat.id == config.bot.chat_id)
# async def del_text_message(msg: Message):
#     try:
#         await msg.delete()
#     except Exception:
#         ...
