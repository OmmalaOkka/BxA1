from pyrogram import enums
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot import LOGGER, DATABASE_URL, PRE_DICT, LEECH_DICT, dispatcher, PAID_USERS, OWNER_ID, CAP_DICT
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.ext_utils.db_handler import DbManger


def prename_set(update, context):
    lm = sendMessage(f"<b>Please Wait....Processing👾</b>", context.bot, update.message)
    pre_send = update.message.text.split(" ", maxsplit=1)
    reply_to = update.message.reply_to_message
    if len(pre_send) > 1:
        txt = pre_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
        prefix_ = txt
        PRE_DICT[user_id_] = prefix_
        if DATABASE_URL:
            DbManger().user_pre(user_id_, prefix_)
            LOGGER.info(f"User : {user_id_} Prename is Saved in DB")
        editMessage(f"<b>{u_men} Prename for the file is done🎯</b>\n\n<b>Your Prename Text: </b><code>{txt}</code>", lm)
        
def userlog_set(update, context):
    user_id_ = update.message.from_user.id 
    u_men = update.message.from_user.first_name
    if user_id_ in PAID_USERS:
        if (BotCommands.UserLogCommand in update.message.text) and (len(update.message.text.split(' ')) == 1):
            sendMessage(f'Send Your Backup Channel ID alone with command like \n\n{BotCommands.UserLogCommand} -100xxxxxxx', context.bot, update.message)
        else:
            lm = sendMessage("Please wait...", context.bot, update.message)          
            pre_send = update.message.text.split(" ", maxsplit=1)
            reply_to = update.message.reply_to_message
            if len(pre_send) > 1:
                txt = pre_send[1]
            elif reply_to is not None:
                txt = reply_to.text
            else:
                txt = ""
            dumpid_ = txt
            LEECH_DICT[user_id_] = dumpid_
            if DATABASE_URL:
                DbManger().user_dump(user_id_, dumpid_)
                LOGGER.info(f"User : {user_id_} LeechLog ID Saved in DB")
            editMessage(f"<b>{u_men} your Channel ID Saved...</b>", lm)
    else:
        sendMessage(f"Buy Paid Service to use Feature.", context.bot, update.message)
        
def caption_set(update, context):
    user_id_ = update.message.from_user.id 
    u_men = update.message.from_user.first_name
    if user_id_ in PAID_USERS:
        if (BotCommands.CaptionCommand in update.message.text) and (len(update.message.text.split(' ')) == 1):
            sendMessage(f'<b>Set Caption Like👇 \n/{BotCommands.CaptionCommand}\n\n📥 JOIN : @MSPmoviesOffl</b>', context.bot, update.message)
        else:
            lm = sendMessage(f"<b>Please Wait....Processing👾</b>", context.bot, update.message)
            pre_send = update.message.text.split(" ", maxsplit=1)
            reply_to = update.message.reply_to_message
            if len(pre_send) > 1:
                txt = pre_send[1]
            elif reply_to is not None:
                txt = reply_to.text
            else:
                txt = ""
            caption_ = txt
            CAP_DICT[user_id_] = caption_
            if DATABASE_URL:
                DbManger().user_cap(user_id_, caption_)
                LOGGER.info(f"User : {user_id_} Caption Saved in DB")
            editMessage(f"<b>{u_men} Caption for the file is done🎯</b>\n\n<b>Your Caption Text: </b><code>{txt}</code>", lm)
    else:
        sendMessage(f"Buy Paid Service to use Feature.", context.bot, update.message)
        
prename_set_handler = CommandHandler(BotCommands.PreNameCommand, prename_set,
                                       filters=(CustomFilters.authorized_chat | CustomFilters.authorized_user), run_async=True)
userlog_set_handler = CommandHandler(BotCommands.UserLogCommand, userlog_set,
                                       filters=(CustomFilters.authorized_chat | CustomFilters.authorized_user), run_async=True) 
caption_set_handler = CommandHandler(BotCommands.CaptionCommand, caption_set,
                                       filters=(CustomFilters.authorized_chat | CustomFilters.authorized_user), run_async=True)

dispatcher.add_handler(prename_set_handler)
dispatcher.add_handler(userlog_set_handler)
dispatcher.add_handler(caption_set_handler)
