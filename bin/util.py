import os
import csv
import datetime
from dateutil.relativedelta import relativedelta

def parse_data_name(data_name):
    # data_name is no less than 3 group words like 'upbit-btc-240' or 'upbit-btc-240-chart'
    groups = data_name.split('-')
    assert 3 <= len(groups)
    exchange = groups[0]
    market = groups[1]
    candle_unit = groups[2]
    return exchange, market, candle_unit

def func_relativedelta(candle_unit):
    if candle_unit.isnumeric():
        return lambda cnt : relativedelta(minutes=cnt*int(candle_unit))
    elif candle_unit == 'day':
        return lambda cnt : relativedelta(days=cnt)
    elif candle_unit == 'week':
        return lambda cnt : relativedelta(weeks=cnt)
    elif candle_unit == 'month':
        return lambda cnt : relativedelta(months=cnt)
    else:
        raise Exception(candle_unit)

def open_csv_file(path, title_columns, append):
    if not append:
        file = open(path, 'w', newline='', buffering=1)
        csv_writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(title_columns)
    else:
        first_append = not os.path.exists(path)
        file = open(path, 'a', newline='', buffering=1)
        csv_writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if first_append:
            csv_writer.writerow(title_columns)
    return file, csv_writer

def to_simple_str(value):
    if value is None:
        return ''
    if isinstance(value, str):
        return value
    elif isinstance(value, datetime.date):
        return value.isoformat()
    elif isinstance(value, int):
        return f'{value:d}'
    elif isinstance(value, float):
        return f'{value:f}'.rstrip('0').rstrip('.')
    else:
        return str(value)
