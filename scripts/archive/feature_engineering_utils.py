from datetime import timedelta
import pandas as pd
import data_fetching_utils as dfu

def filter_subset(subset, cols):

    '''
    '''

    start = subset[0]['time_period_end'].split('.')[0]
    data_return = [start]

    for obs in subset:

        data_return += [obs[attr] for attr in cols]

    return data_return

def standardize_df(df, stats=None, stats_out=False):

    '''
    Standardizes every column but the time column
    stats is a list of tuples with the mean and sd to be used for every column
    if stats_out is True, returns a list of tuples with the mean and sd
    '''

    df_sd = pd.DataFrame()
    df_sd['time'] = df['time']
    i = 0

    if stats_out:
        mean_sd_list = []

    for col in df:
        if col == 'time':
            continue
        else:
            if stats:
                df_sd[col] = pd.to_numeric(standardize(df[col], stats[i]))
            else:
                if stats_out:
                    standardized_results = standardize(df[col], stats_out=True)
                    df_sd[col] = standardized_results[0]
                    mean_sd_list.append(standardized_results[1])
                else:
                    df_sd[col] = standardize(df[col])
            i += 1

    if stats_out:
        return df_sd, mean_sd_list
    else:
        return df_sd

def standardize(col, stats=None, stats_out=False):

    '''
    standardizes a column if stats is not provided.
    stats is a tuple or list with the mean and sd to be used if provided
    if stats_out is True, returns a tuple with the mean and sd
    '''

    if stats:
        mean, sd = stats
    else:
        mean = col.mean()
        sd = col.std()

    rv = (col - mean) / sd

    if stats_out:
        return rv, (mean, sd)
    else:
        return rv

def arrange_deployment_data(data, price_cols, freq, time_delta):

    '''
    arranges data for deployment
    data: data as we get it from CoinAPI
    price_cols: list of column names that will contain our data
    freq: frequency of observations, in minutes
    time_delta: time we're retrieving data from, in hours
    '''

    # Number of times the price_cols will be repeated
    end = data[-1]['time_period_end'][:19]
    start = data[0]['time_period_end'][:19]
    n_col_iterations = dfu.calculate_observations(start, end, freq)

    # Data in reversed order, so most recent obs are first
    data_rev = data[::-1]
    relevant_data = filter_subset(data_rev, price_cols)

    # Cols
    cols = ['time']
    for i in range(n_col_iterations):
        cols += [col+str(i+1) for col in price_cols]

    # Dataframe
    df = pd.DataFrame(columns = cols)
    df.loc[0] = relevant_data
    # Note: this is not standardized

    return df
