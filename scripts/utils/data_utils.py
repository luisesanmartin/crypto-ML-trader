import numpy as np
import pickle
import objects
import torch
import time_utils

def make_data_dic(data):

    '''
    Transforms the JSON data to a dictionary
    with period end as key
    '''

    data_dic = {}

    for data_point in data:

    	key = data_point['time_period_end'].split('.')[0]
    	data_dic[key] = data_point

    return data_dic

def price_increased(data_dic, time):

	'''
	Price increased by the end of "time" for that observation
	'''

	try:
		price_open = data_dic[time]['price_open']
		price_close = data_dic[time]['price_close']
	except KeyError:
		return np.nan

	if price_close > price_open:
		return 1
	else:
		return 0

def price_increased_next(data_dic, time, n, gap=objects.PERIOD_DATA_MIN):

	future_time = time_utils.future_time(time, n, gap)
	increased = price_increased(data_dic, future_time)

	return increased

def attribute_increased_for_time(data_dic, time, attribute, gap=objects.PERIOD_DATA_MIN):

	'''
	Attribute increased for 'time' with respect of its previous observation
	'''

	previous_time = time_utils.past_time(time, 1, gap)
	
	try:
		attribute_now = data_dic[time][attribute]
		attribute_past = data_dic[previous_time][attribute]
	except KeyError:
		return np.nan

	if attribute_now > attribute_past:
		return 1
	else:
		return 0

def volume_increased_past(data_dic, time, n, gap=objects.PERIOD_DATA_MIN):

	'''
	Volume increased n times ago with respect of its previous (n-1) observation
	'''

	initial_time = time_utils.past_time(time, n, gap)
	result = attribute_increased_for_time(data_dic, initial_time, 'volume_traded', gap)

	return result

def trades_increased_past(data_dic, time, n, gap=objects.PERIOD_DATA_MIN):

	'''
	Trades increased n times ago with respect of its previous (n-1) observation
	'''

	initial_time = time_utils.past_time(time, n, gap)
	result = attribute_increased_for_time(data_dic, initial_time, 'trades_count', gap)

	return result

def standardize(vector, standardizer):

	array = np.array(vector).reshape(-1, 1)
	result = standardizer.transform(array).flatten()

	return result

def max_price_is_open_fn(data_dic, time):

	try:
		max_price = data_dic[time]['price_high']
		open_price = data_dic[time]['price_open']
		if open_price == max_price:
			return 1
		else:
			return 0
	except KeyError:
		return np.nan

def min_price_is_open_fn(data_dic, time):

	try:
		min_price = data_dic[time]['price_low']
		open_price = data_dic[time]['price_open']
		if open_price == min_price:
			return 1
		else:
			return 0
	except KeyError:
		return np.nan

def max_price_is_close_fn(data_dic, time):

	try:
		max_price = data_dic[time]['price_high']
		close_price = data_dic[time]['price_close']
		if close_price == max_price:
			return 1
		else:
			return 0
	except KeyError:
		return np.nan

def min_price_is_close_fn(data_dic, time):

	try:
		min_price = data_dic[time]['price_low']
		close_price = data_dic[time]['price_close']
		if close_price == min_price:
			return 1
		else:
			return 0
	except KeyError:
		return np.nan

def make_x(data_dic):

	'''
	Creates the complete data row for producing predictions
	'''

	# ID variable: end time of period
	times = list(data_dic.keys())[0:1]
	print('Estimating features for: {}'.format(times[0]))

	# Price increased in this observation
	inc_price = [price_increased_next(data_dic, time, 0) for time in times]

	# Standardized close price
	close_prices = [data_dic[time]['price_close'] for time in times]
	with open('../data/standardizer_prices.pkl', 'rb') as f:
		standardizer = pickle.load(f)
	close_prices_standardized = standardize(close_prices, standardizer)

	# Price increase in last X observations
	inc_price_last1 = [price_increased_next(data_dic, time, -1) for time in times]
	inc_price_last2 = [price_increased_next(data_dic, time, -2) for time in times]
	inc_price_last3 = [price_increased_next(data_dic, time, -3) for time in times]
	inc_price_last4 = [price_increased_next(data_dic, time, -4) for time in times]
	inc_price_last5 = [price_increased_next(data_dic, time, -5) for time in times]
	inc_price_last6 = [price_increased_next(data_dic, time, -6) for time in times]

	# Volume increased in this observation
	inc_vol = [attribute_increased_for_time(data_dic, time, 'volume_traded') for time in times]

	# Standardized volume traded
	volumes = [data_dic[time]['volume_traded'] for time in times]
	with open('../data/standardizer_volumes.pkl', 'rb') as f:
		standardizer = pickle.load(f)
	volumes_standardized = standardize(volumes, standardizer)

	# Volume increased in last X observations
	inc_vol_last1 = [volume_increased_past(data_dic, time, 1) for time in times]
	inc_vol_last2 = [volume_increased_past(data_dic, time, 2) for time in times]
	inc_vol_last3 = [volume_increased_past(data_dic, time, 3) for time in times]
	inc_vol_last4 = [volume_increased_past(data_dic, time, 4) for time in times]
	inc_vol_last5 = [volume_increased_past(data_dic, time, 5) for time in times]
	inc_vol_last6 = [volume_increased_past(data_dic, time, 6) for time in times]

	# Trade increased in this observation
	inc_trades = [attribute_increased_for_time(data_dic, time, 'trades_count') for time in times]

	# Standardized N of trades
	trades = [data_dic[time]['trades_count'] for time in times]
	with open('../data/standardizer_trades.pkl', 'rb') as f:
		standardizer = pickle.load(f)
	trades_standardized = standardize(trades, standardizer)

	# Trade increased in last X observations
	inc_trade_last1 = [trades_increased_past(data_dic, time, 1) for time in times]
	inc_trade_last2 = [trades_increased_past(data_dic, time, 1) for time in times]
	inc_trade_last3 = [trades_increased_past(data_dic, time, 1) for time in times]
	inc_trade_last4 = [trades_increased_past(data_dic, time, 1) for time in times]
	inc_trade_last5 = [trades_increased_past(data_dic, time, 1) for time in times]
	inc_trade_last6 = [trades_increased_past(data_dic, time, 1) for time in times]

	# Max price is open price
	max_price_is_open = [max_price_is_open_fn(data_dic, time) for time in times]

	# Max price is close price
	max_price_is_close = [max_price_is_close_fn(data_dic, time) for time in times]

	# Min price is open price
	min_price_is_open = [min_price_is_open_fn(data_dic, time) for time in times]

	# Min price is close price
	min_price_is_close = [min_price_is_close_fn(data_dic, time) for time in times]

	# Putting all together
	data = np.array([
		close_prices_standardized,
		inc_price_last1,
		inc_price_last2,
		inc_price_last3,
		inc_price_last4,
		inc_price_last5,
		inc_price_last6,
		volumes_standardized,
		inc_vol_last1,
		inc_vol_last2,
		inc_vol_last3,
		inc_vol_last4,
		inc_vol_last5,
		inc_vol_last6,
		trades_standardized,
		inc_trade_last1,
		inc_trade_last2,
		inc_trade_last3,
		inc_trade_last4,
		inc_trade_last5,
		inc_trade_last6,
		max_price_is_open,
		max_price_is_close,
		min_price_is_open,
		min_price_is_close,
		inc_price,
		inc_vol,
		inc_trades
	]).flatten()

	return data

def prediction_from_net(X, model):

	'''
	Estimate price increase prediction
	'''

	X = torch.tensor(X).float()

	with torch.no_grad():
		pred_logit = model(X).squeeze()
		pred = torch.round(torch.sigmoid(pred_logit))

	return pred.item()


