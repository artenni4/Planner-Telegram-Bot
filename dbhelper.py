import logging
import sqlite3 as sqlite

logger = logging.getLogger(__name__)

class _DBHelper:
	def __init__(self):
		logger.info('Database helper initialized')
		cur = sqlite.connect('timetable.db').cursor()
		cur.execute(
			'''CREATE TABLE IF NOT EXISTS 
			Reminders(ReminderID integer primary key autoincrement, ChatID integer not null, ReminderText varchar, ReminderDatetime varchar)
			''')
		#cur.execute('CREATE TABLE IF NOT EXISTS Test(ID integer primary key autoincrement, Test1 text, Test2 text, Test3 text)')

	def add_reminder(self, reminder):
		'''
		Arguments:
			reminder = {'chat_id' : ... , 'text' : ... , 'datetime' : ...}

		Function adds a reminder to database
		'''
		conn = sqlite.connect('timetable.db')
		cur = conn.cursor()

		cur.execute('INSERT INTO Reminders(ChatID, ReminderText, ReminderDatetime) VALUES(?,?,?)', (reminder['chat_id'], reminder['text'], reminder['datetime']))
		conn.commit()
		cur.close()
		conn.close()
		logger.info('Reminder added')

	def get_reminders(self, chat_id=None):
		'''
		Returns
		'''
		logger.info('Getting reminders list')
		conn = sqlite.connect('timetable.db')
		cur = conn.cursor()
		if chat_id != None:
			cur.execute('SELECT * FROM Reminders WHERE ChatID = ?', (chat_id,))
		else:
			cur.execute('SELECT * FROM Reminders')
		reminders_list = cur.fetchall()

		return reminders_list

DBHelper = _DBHelper()