from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import sqlite3
import random
import time


def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    with sqlite3.connect('bugurts.db') as conn:
        c = conn.cursor()
        c.execute('SELECT last_command_time FROM users WHERE id = ?', (user_id,))
        last_command_time = c.fetchone()
        if last_command_time is None or time.time() - last_command_time[0] > 15:
            update.message.reply_text('Привет! Напиши /bugurt или /bugurt [номер бугурта]. Например "/bugurt 11765" выведет бугурт под номером 11765. Также можно посмотреть актуальный топ бугуртов по запросу /top. \nРаз в 15 секунд можно вызвать /bugurt, раз в 60 секунд /top.')
            current_time = time.time()
            c.execute('INSERT OR REPLACE INTO users (id, last_command_time) VALUES (?, ?)', (user_id, current_time))
            conn.commit()
        else:
            update.message.reply_text('Команда не может быть выполнена. Попробуйте позже.')


def bugurt(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    with sqlite3.connect('bugurts.db') as conn:
        c = conn.cursor()
        c.execute('SELECT last_command_time FROM users WHERE id = ?', (user_id,))
        last_command_time = c.fetchone()
        if last_command_time is None or time.time() - last_command_time[0] > 15:
            # Rest of the code
            c.execute('INSERT OR REPLACE INTO users (id, last_command_time) VALUES (?, ?)', (user_id, current_time))
            conn.commit()
        else:
            update.message.reply_text('Команда не может быть выполнена. Попробуйте позже.')


def top(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    with sqlite3.connect('bugurts.db') as conn:
        c = conn.cursor()
        c.execute('SELECT last_command_time FROM users WHERE id = ?', (user_id,))
        last_command_time = c.fetchone()
        if last_command_time is None or time.time() - last_command_time[0] > 60:
            # Rest of the code
            c.execute('INSERT OR REPLACE INTO users (id, last_command_time) VALUES (?, ?)', (user_id, current_time))
            conn.commit()
        else:
            update.message.reply_text('Команда не может быть выполнена. Попробуйте позже.')


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    bugurt_id, mark = map(int, query.data.split(':'))

    with sqlite3.connect('bugurts.db') as conn:
        c = conn.cursor()
        c.execute('SELECT mark, message_id FROM marks WHERE user_id = ? AND bugurt_id = ?', (user_id, bugurt_id))
        existing_mark = c.fetchone()

        if existing_mark is None:
            # Rest of the code
            conn.commit()
            query.answer()
        else:
            if existing_mark[0] != mark:
                # Rest of the code
                conn.commit()
                query.answer()
            else:
                query.answer('Вы уже поставили эту оценку.')


def main() -> None:
    updater = Updater("810490361:AAGj8tqtrW38L1C2KnQ_NXA1FYAViXEVe3w")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("bugurt", bugurt))
    dispatcher.add_handler(CommandHandler("top", top))
    dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
