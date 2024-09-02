import objects
from datetime import datetime, timedelta

def minute_seconds_now():

	'''
	returns the miuntes and seconds of the current time
	'''

	now = datetime.now()

	return now.minute, now.second

def time_in_datetime(time):

    '''
    Transforms a time string to datetime
    '''

    time = time.split('.')[0]

    return datetime.strptime(time, objects.TIME_FMT)

def time_in_string(time):

    '''
    Transforms a datetime to a time string
    '''

    isoformat = time.isoformat()

    if '.' in isoformat:
        return isoformat[:-7].split('.')[0]

    else:
        return isoformat

def past_time(time, n, gap=objects.PERIOD_DATA_MIN):

	'''
	Returns a past time relative to time, n times the gap (minutes)
	'''

	time_datetime = time_in_datetime(time)
	past_datetime = time_datetime - timedelta(minutes=n*gap)
	past = time_in_string(past_datetime)

	return past

def future_time(time, n, gap=objects.PERIOD_DATA_MIN):

	'''
	Returns a future time relative to time, n times the gap (minutes)
	'''

	time_datetime = time_in_datetime(time)
	future_datetime = time_datetime + timedelta(minutes=n*gap)
	future = time_in_string(future_datetime)

	return future