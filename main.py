#enable logger
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

from _bottoken import bot_token #private bot token
from _defaults import *
from dbhelper import DBHelper
from converters import *
import threading
import datetime
from time import sleep
from telegram.ext import (
	Updater, 
	CommandHandler, 
	ConversationHandler, 
	MessageHandler, 
	Filters,
	CallbackQueryHandler,)
from telegram import (
	ReplyKeyboardMarkup,
	InlineKeyboardButton,
	InlineKeyboardMarkup,)

logger = logging.getLogger(__name__)


'''GLOBALS'''
main_updater = Updater(token=bot_token, use_context=True)


def start_bot(update, context):
	logger.info('start command called')
	update.message.reply_text(
		'Привет, я - бот, который поможет тебе поставить напоминания или планировать дела на будущее.\n\nВыбери что ты хочешь сейчас сделать',
		reply_markup=ReplyKeyboardMarkup([['Напоминание', 'План']], one_time_keyboard=False, resize_keyboard=True))
	return SELECTING_TYPE

def reminder(update, context):
	logger.info('user wants to interact with reminder')
	buttons = [
		[
			InlineKeyboardButton(text='Добавить', callback_data=str(ADDING_REMINDER)), 
		],
		[
			InlineKeyboardButton(text='Удалить', callback_data=str(DELETING_REMINDER)),
			InlineKeyboardButton(text='Показать', callback_data=str(SHOWING_REMINDER)),
		],
	]
	keyboard = InlineKeyboardMarkup(buttons)

	update.message.reply_text('Ок, что делать с напоминаниями?', reply_markup=keyboard)
	return SELECTING_REMINDER_ACTION

def planner(update, context):
	logger.info('user wants to interact with planner')
	buttons = [
		[
			InlineKeyboardButton(text='Добавить', callback_data=str(ADDING_PLANNER)), 
		],
		[
			InlineKeyboardButton(text='Удалить', callback_data=str(DELETING_PLANNER)),
			InlineKeyboardButton(text='Показать', callback_data=str(SHOWING_PLANNER)),
		],
	]
	keyboard = InlineKeyboardMarkup(buttons)

	update.message.reply_text(text='Ок, что делать с планами?', reply_markup=keyboard)
	return SELECTING_PLANNER_ACTION

def add_reminder(update, context):
	logger.info('user wants to add a remind')
	buttons = [[InlineKeyboardButton(text='Отмена', callback_data=str(GO_BACK))]]
	keyboard = InlineKeyboardMarkup(buttons)
	update.callback_query.answer()
	update.callback_query.edit_message_text('Добавляем напоминание...\n\nВведите текст напоминалки', reply_markup=keyboard)
	return PROMPT_REMINDER_TEXT

def add_reminder_text(update, context):
	user_reminder_text = update.message.text
	logger.info('user entered reminder text: ' + user_reminder_text)
	context.user_data[REMINDER_TEXT] = user_reminder_text
	update.message.reply_text('Теперь введите дату напоминания')
	return PROMPT_REMINDER_DATE

def add_reminder_date(update, context):
	user_reminder_date = update.message.text
	parsed_date = convert_date(user_reminder_date)
	if parsed_date:
		logger.info('user entered date: ' + parsed_date)
		context.user_data[REMINDER_DATE] = parsed_date
		update.message.reply_text('Теперь время, в которое вам прийдёт напоминание')
		return PROMPT_REMINDER_TIME
	else:
		logger.info('incorrect date!')
		update.message.reply_text('Не понимаю такой формат даты, введите ещё раз')
		return PROMPT_REMINDER_DATE

def add_reminder_time(update, context):
	user_reminder_time = update.message.text
	parsed_time = convert_time(user_reminder_time)
	if parsed_time:
		ud = context.user_data
		logger.info('user entered time: ' + parsed_time)
		ud[REMINDER_TIME] = parsed_time
		update.message.reply_text('Готово! Напоминание успешно добавлено.\nДата: {} {}\nТекст: {}'.format(
			ud[REMINDER_DATE], ud[REMINDER_TIME], ud[REMINDER_TEXT]))

		#create reminder argument for database
		
		reminder = {
			'chat_id' : update.message.chat_id,
			'text' : ud[REMINDER_TEXT],
			'datetime' : ud[REMINDER_DATE] + ' ' + ud[REMINDER_TIME]
		}
		DBHelper.add_reminder(reminder)
		return ConversationHandler.END
	else:
		logger.info('incorrect time!')
		update.message.reply_text('Не понимаю такой формат времени, введите ещё раз')
		return PROMPT_REMINDER_TIME

def show_reminders(update, context):
	reminders = DBHelper.get_reminders(update.callback_query.message.chat.id)
	logger.info(str(reminders))
	message_str = 'Вот твои напоминания\n\n'
	for i, r in enumerate(reminders):
		message_str += str(i + 1) + '. ' + r[3] + ' | ' + r[2] + '\n'

	update.callback_query.answer()
	update.callback_query.edit_message_text(message_str)
	return SELECTING_TYPE

def add_planner(update, context):
	logger.info('user wants to add a plan')
	update.callback_query.answer()
	update.callback_query.edit_message_text('Добавляем план...\n\nВведите текст плана')
	return PROMPT_PLANNER_TEXT

def cancel_action(update, context):
	logger.info('user cancelled last action')
	update.callback_query.answer()
	update.callback_query.edit_message_text('Отмена. Жду дальнейших указаний')
	return ConversationHandler.END

def start_reminders_daemon():
	logger.info('Reminders daemon started')
	last_time = datetime.datetime.now()
	while True:
		new_time = datetime.datetime.now()
		if last_time.minute == new_time.minute:
			sleep(1)
		else:
			last_time = new_time
			#check users' reminders
			reminders = DBHelper.get_reminders()
			logger.info('Compare to ' + datetime_to_string(new_time))
			for r in reminders:
				if r[3] == datetime_to_string(new_time):
					main_updater.bot.send_message(r[1], r[2])

def main():
	#create updater and dispatcher
	main_dispatcher = main_updater.dispatcher

	start_bot_handler = CommandHandler('start', start_bot)

	add_reminder_conversation = ConversationHandler(
		entry_points=[CallbackQueryHandler(add_reminder, pattern='^' + str(ADDING_REMINDER) + '$')],
		states={
			PROMPT_REMINDER_TEXT : [MessageHandler(Filters.all, add_reminder_text)], #user enters text of reminding. Example: Go to shop
			PROMPT_REMINDER_DATE : [MessageHandler(Filters.text, add_reminder_date)], #user enders date. Example: 12.04.2020 or 15 01 or tomorrow or 19(day)
			PROMPT_REMINDER_TIME : [MessageHandler(Filters.text, add_reminder_time)], #user enters time. Example: 12.30 or 12:50 or 20 50
		},
		fallbacks=[CallbackQueryHandler(cancel_action, pattern='^' + str(GO_BACK) + '$')])

	add_planner_conversation = ConversationHandler(
		entry_points=[CallbackQueryHandler(add_planner, pattern='^' + str(ADDING_PLANNER) + '$')],
		states={
			PROMPT_PLANNER_TEXT : [], #user enters text of plan
			PROMPT_PLANNER_DATE : [], #user enters date to what he have to do the plan
		},
		fallbacks=[])

	reminder_action_handlers = [
		add_reminder_conversation, #adding reminders conversation
		#delete reminders
		CallbackQueryHandler(show_reminders, pattern='^' + str(SHOWING_REMINDER) + '$') #show reminders
	]
	planner_action_handlers = [
		add_planner_conversation,
		#delete planners
		#show planners
	]

	main_handlers = [start_bot_handler, MessageHandler(Filters.regex('Напоминание'), reminder), MessageHandler(Filters.regex('План'), planner)]

	conversation_handler = ConversationHandler(
		entry_points=main_handlers,
		states={
			SELECTING_TYPE : main_handlers,
			SELECTING_REMINDER_ACTION : reminder_action_handlers,
			SELECTING_PLANNER_ACTION : planner_action_handlers,
		},
		fallbacks=main_handlers)

	main_dispatcher.add_handler(conversation_handler) # main conversation of bot


	reminders_daemon = threading.Thread(target=start_reminders_daemon, daemon=True).start()

	main_updater.start_polling() #start bot
	main_updater.idle() #idle for test use, close bot with Ctrl-C

	logger.info('Reached end')

if __name__ == '__main__':
	main()
