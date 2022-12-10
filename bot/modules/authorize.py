from telegram.ext import CommandHandler

from bot import user_data, dispatcher, DATABASE_URL, PAID_USERS
from bot.helper.telegram_helper.message_utils import sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.db_handler import DbManger
from bot.helper.ext_utils.bot_utils import update_user_ldata


def authorize(update, context):
    reply_message = update.message.reply_to_message
    if len(context.args) == 1:
        id_ = int(context.args[0])
    elif reply_message:
        id_ = reply_message.from_user.id
    else:
        id_ = update.effective_chat.id
    if id_ in user_data and user_data[id_].get('is_auth'):
        msg = 'Already Authorized!'
    else:
        update_user_ldata(id_, 'is_auth', True)
        if DATABASE_URL:
            DbManger().update_user_data(id_)
        msg = 'Authorized'
    sendMessage(msg, context.bot, update.message)

def unauthorize(update, context):
    reply_message = update.message.reply_to_message
    if len(context.args) == 1:
        id_ = int(context.args[0])
    elif reply_message:
        id_ = reply_message.from_user.id
    else:
        id_ = update.effective_chat.id
    if id_ not in user_data or user_data[id_].get('is_auth'):
        update_user_ldata(id_, 'is_auth', False)
        if DATABASE_URL:
            DbManger().update_user_data(id_)
        msg = 'Unauthorized'
    else:
        msg = 'Already Unauthorized!'
    sendMessage(msg, context.bot, update.message)

def addSudo(update, context):
    id_ = ""
    reply_message = update.message.reply_to_message
    if len(context.args) == 1:
        id_ = int(context.args[0])
    elif reply_message:
        id_ = reply_message.from_user.id
    if id_:
        if id_ in user_data and user_data[id_].get('is_sudo'):
            msg = 'Already Sudo!'
        else:
            update_user_ldata(id_, 'is_sudo', True)
            if DATABASE_URL:
                DbManger().update_user_data(id_)
            msg = 'Promoted as Sudo'
    else:
        msg = "Give ID or Reply To message of whom you want to Promote."
    sendMessage(msg, context.bot, update.message)

def removeSudo(update, context):
    id_ = ""
    reply_message = update.message.reply_to_message
    if len(context.args) == 1:
        id_ = int(context.args[0])
    elif reply_message:
        id_ = reply_message.from_user.id
    if id_ and id_ not in user_data or user_data[id_].get('is_sudo'):
        update_user_ldata(id_, 'is_sudo', False)
        if DATABASE_URL:
            DbManger().update_user_data(id_)
        msg = 'Demoted'
    else:
        msg = "Give ID or Reply To message of whom you want to remove from Sudo"
    sendMessage(msg, context.bot, update.message)

def addPaid(update, context):
    user_id = ""
    reply_message = update.message.reply_to_message
    if len(context.args) == 1:
        user_id = int(context.args[0])
    elif reply_message:
        user_id = reply_message.from_user.id
    if user_id:
        if user_id in PAID_USERS:
            msg = 'Already a Paid User!'
        elif DATABASE_URL is not None:
            msg = DbManger().user_addpaid(user_id)
            PAID_USERS.add(user_id)
        else:
            PAID_USERS.add(user_id)
            msg = 'Promoted as Paid User'
    else:
        msg = "Give ID or Reply To message of whom you want to Promote as Paid User"
    sendMessage(msg, context.bot, update.message)

def removePaid(update, context):
    user_id = ""
    reply_message = update.message.reply_to_message
    if len(context.args) == 1:
        user_id = int(context.args[0])
    elif reply_message:
        user_id = reply_message.from_user.id
    if user_id and user_id in PAID_USERS:
        msg = DbManger().user_rmpaid(user_id) if DATABASE_URL is not None else 'Removed from Paid Subscription'
        PAID_USERS.remove(user_id)
    else:
        msg = "Give ID or Reply To message of whom you want to remove from Paid User"
    sendMessage(msg, context.bot, update.message)

def sendPaidDetails(update, context):
    paid = ''
    paid += '\n'.join(f"<code>{uid}</code>" for uid in PAID_USERS)
    sendMessage(f'<b><u>Paid Users:</u></b>\n{paid}', context.bot, update.message)
    
pdetails_handler = CommandHandler(command=BotCommands.PaidUsersCommand, callback=sendPaidDetails,
                                    filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
authorize_handler = CommandHandler(BotCommands.AuthorizeCommand, authorize,
                                   filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
unauthorize_handler = CommandHandler(BotCommands.UnAuthorizeCommand, unauthorize,
                                   filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
addsudo_handler = CommandHandler(BotCommands.AddSudoCommand, addSudo,
                                   filters=CustomFilters.owner_filter, run_async=True)
removesudo_handler = CommandHandler(BotCommands.RmSudoCommand, removeSudo,
                                   filters=CustomFilters.owner_filter, run_async=True)
addpaid_handler = CommandHandler(command=BotCommands.AddPaidCommand, callback=addPaid,
                                    filters=CustomFilters.owner_filter, run_async=True)
removepaid_handler = CommandHandler(command=BotCommands.RmPaidCommand, callback=removePaid,
                                    filters=CustomFilters.owner_filter, run_async=True)

dispatcher.add_handler(pdetails_handler)
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(unauthorize_handler)
dispatcher.add_handler(addsudo_handler)
dispatcher.add_handler(removesudo_handler)
dispatcher.add_handler(addpaid_handler)
dispatcher.add_handler(removepaid_handler)
