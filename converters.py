import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

import datetime as dt
import re

logger = logging.getLogger(__name__)

'''
Standart datetime format = dd.mm.yyyy hh:mm
Examples:
24.10.2020 15:00
01.01.2021 01:30
12.01.2023 13.05
'''

def _check_str_date(day_str, month_str, year_str):
	if day_str[0] == '0':
		day_str = day_str[1:]
	if month_str[0] == '0':
		month_str = month_str[1:]
	if len(year_str) == 2:
		year_str = '20' + year_str

	try:
		day = int(day_str)
		month = int(month_str)
		year = int(year_str)
	except ValueError:
		return False

	try:
		dt.datetime(day=day, month=month, year=year)
	except ValueError:
		return False

	logger.info('return true')
	return True

def _normalize_date_to_str(day, month, year):
	day_str = str(day) if len(str(day)) == 2 else '0' + str(day)
	month_str = str(month) if len(str(month)) == 2 else '0' + str(month)
	year_str = str(year)
	return day_str + '.' + month_str + '.' + year_str

def _check_str_time(hour_str, minute_str):
	if hour_str[0] == '0':
		hour_str = hour_str[1:]
	if minute_str[0] == '0':
		minute_str = minute_str[1:]

	try:
		hour = int(hour_str)
		minute = int(minute_str)
	except ValueError:
		return False

	if hour < 0 or hour > 23:
		return False
	if minute < 0 or minute > 59:
		return False

	return True

def _normalize_time(hour, minute):
	hour_str = str(hour) if len(str(hour)) == 2 else '0' + str(hour)
	minute_str = str(minute) if len(str(minute)) == 2 else '0' + str(minute)
	return hour_str + ':' + minute_str

def convert_date(date_str):
	'''
	It takes string with user input date and returns date in format dd.mm.yyyy
	'''

	date_str = str(date_str)

	
	#if input was one number, that means day
	day_str = date_str
	month_str = str(dt.datetime.now().month)
	year_str = str(dt.datetime.now().year)
	if _check_str_date(day_str, month_str, year_str):
		return _normalize_date_to_str(day_str, month_str, year_str)


	#if input was dd mm or dd mm yyyy
	split_space = re.split(r' ', date_str)
	if len(split_space) == 2:
		#dd mm
		day_str = split_space[0]
		month_str = split_space[1]
		year_str = str(dt.datetime.now().year)

		if _check_str_date(day_str, month_str, year_str):
			return _normalize_date_to_str(day_str, month_str, year_str)
	elif len(split_space) == 3:
		#dd mm yyyy
		day_str = split_space[0]
		month_str = split_space[1]
		year_str = split_space[2]

		if _check_str_date(day_str, month_str, year_str):
			return _normalize_date_to_str(day_str, month_str, year_str)

	#if input was dd.mm or dd.mm.yyyy
	split_dots = re.split(r'.', date_str)
	if len(split_dots) == 2:
		# dd.mm
		day_str = split_dots[0]
		month_str = split_dots[1]
		year_str = str(dt.datetime.now().year)

		if _check_str_date(day_str, month_str, year_str):
			return _normalize_date_to_str(day_str, month_str, year_str)
	elif len(split_dots) == 3:
		# dd.mm.yyyy
		day_str = split_dots[0]
		month_str = split_dots[1]
		year_str = split_dots[2]

		if _check_str_date(day_str, month_str, year_str):
			return _normalize_date_to_str(day_str, month_str, year_str)


	#if input is 'today'
	if date_str == 'Сегодня' or date_str == 'сегодня':
		day_str = str(dt.datetime.now().day)
		month_str = str(dt.datetime.now().month)
		year_str = str(dt.datetime.now().year)
		return _normalize_date_to_str(day_str, month_str, year_str)

	#if input is 'tomorrow'
	if date_str == 'Завтра' or date_str == 'завтра':
		day_str = str(dt.datetime.now().day + 1) # add one day
		month_str = str(dt.datetime.now().month)
		year_str = str(dt.datetime.now().year)
		return _normalize_date_to_str(day_str, month_str, year_str)

	return None

def convert_time(time_str):
	'''
	Takes unput from user and returns formatted string hh.mm
	'''

	time_str = str(time_str)

	hour_str = time_str
	if _check_str_time(hour_str, '00'):
		return _normalize_time(hour_str, '00')

	split_space = re.split(r' ', time_str)
	if len(split_space) == 2:
		hour_str = split_space[0]
		minute_str = split_space[1]

		if _check_str_time(hour_str, minute_str):
			return _normalize_time(hour_str, minute_str)

	split_dots = re.split(r'\.', time_str)
	if len(split_dots) == 2:
		hour_str = split_dots[0]
		minute_str = split_dots[1]

		if _check_str_time(hour_str, minute_str):
			return _normalize_time(hour_str, minute_str)

	split_double_dots = re.split(r':', time_str)
	if len(split_double_dots) == 2:
		hour_str = split_double_dots[0]
		minute_str = split_double_dots[1]

		if _check_str_time(hour_str, minute_str):
			return _normalize_time(hour_str, minute_str)

	return None

def datetime_to_string(dt):
	date = _normalize_date_to_str(dt.day, dt.month, dt.year)
	time = _normalize_time(dt.hour, dt.minute)
	return date + ' ' + time
