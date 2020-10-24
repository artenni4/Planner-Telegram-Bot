import datetime as dt
import re

def convert_date(date_str):
	'''
	It takes string with user input date and returns date in format dd.mm.yyyy
	'''

	date_str = str(date_str)
	try:
		#if input was one number, that means day
		one_int = int(date_str)
		#append necessary data
		day = date_str
		month = str(dt.datetime.now().month) 
		year = str(dt.datetime.now().year)
		date = day + '.' + month + '.' + year
		return date
	except ValueError:
		pass

	#if input was dd mm or dd mm yyyy
	split_space = re.split(r' ', date_str)
	if len(split_space) == 2:
		#dd mm
		day = split_space[0]
		month = split_space[1]
		year = str(dt.datetime.now().year)
		date = day + '.' + month + '.' + year
		return date
	elif len(split_space) == 3:
		#dd mm yyyy
		day = split_space[0]
		month = split_space[1]
		year = split_space[2]
		date = day + '.' + month + '.' + year
		return date

	#if input was dd.mm or dd.mm.yyyy
	split_dots = re.split(r'.', date_str)
	if len(split_dots) == 2:
		# dd.mm
		day = split_dots[0]
		month = split_dots[1]
		year = str(dt.datetime.now().year)
		date = day + '.' + month + '.' + year
		return date
	elif len(split_dots) == 3:
		# dd.mm.yyyy
		day = split_dots[0]
		month = split_dots[1]
		year = split_dots[2]
		date = day + '.' + month + '.' + year
		return date

	#if input is 'today'
	if date_str == 'Сегодня' or date_str == 'сегодня':
		day = str(dt.datetime.now().day)
		month = str(dt.datetime.now().month)
		year = str(dt.datetime.now().year)
		date = day + '.' + month + '.' + year
		return date

	#if input is 'tomorrow'
	if date_str == 'Завтра' or date_str == 'завтра':
		day = str(dt.datetime.now().day + 1) # add one day
		month = str(dt.datetime.now().month)
		year = str(dt.datetime.now().year)
		date = day + '.' + month + '.' + year
		return date

	return None

def convert_time(time_str):
	'''
	Takes unput from user and returns formatted string hh.mm
	'''

	time_str = str(time_str)
	try:
		one_int = int(time_str)
		# if one int, means hour
		hour = time_str
		minute = '00'
		time = hour + ':' + minute
		return time
	except ValueError:
		pass

	split_space = re.split(r' ', time_str)
	if len(split_space) == 2:
		hour = split_space[0] if len(split_space) == 2 else '0' + split_space[0]
		minute = split_space[1] if len(split_space) == 2 else '0' + split_space[1]
		time = hour + ':' + minute
		return time

	split_dots = re.split(r'.', time_str)
	if len(split_dots) == 2:
		hour = split_dots[0]
		minute = split_dots[1]
		time = hour + ':' + minute
		return time

	split_double_dots = re.split(r':', time_str)
	if len(split_double_dots) == 2:
		hour = split_double_dots[0]
		minute = split_double_dots[1]
		time = hour + ':' + minute
		return time

	return None

def datetime_to_string(dt):
	return str(dt.day) + '.' + str(dt.month) + '.' + str(dt.year) + ' ' + str(dt.hour) + ':' + str(dt.minute)
