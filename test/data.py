import os
import glob
import datetime
import unittest
from dateutil.relativedelta import relativedelta

class TestData(unittest.TestCase):

    def test_check_data_files_integrity(self):
        first_date_of_first_data = None
        last_date_of_first_data = None
        for i, data_file_path in enumerate(sorted(glob.glob('*.csv'))):
            print(data_file_path)
            data_name = os.path.splitext(os.path.basename(data_file_path))[0]
            _, _, candle_unit = self.parse_data_name(data_name)

            # Test new line character integrity
            with open(data_file_path, 'rb') as file:
                records = file.readlines()
                for record in records:
                    self.assertEqual(b'\r\n', record[-2:])

            # Test date continuity
            # All date intervals should be same
            with open(data_file_path, 'r') as file:
                records = file.readlines()
                first_date = datetime.datetime.fromisoformat(records[1].split(',')[0]) # Skip the head record
                acc_date = first_date
                for record in records[1:]:
                    cur_date = datetime.datetime.fromisoformat(record.split(',')[0])
                    self.assertEqual(acc_date, cur_date)
                    acc_date += self.func_relativedelta(candle_unit)(1)
                last_date = acc_date

            # Test date consistency
            # All data files should be in same data range
            if i == 0:
                first_date_of_first_data = first_date
                last_date_of_first_data = last_date
            else:
                self.assertEqual(first_date_of_first_data, first_date)
                self.assertEqual(last_date_of_first_data, last_date)

    def parse_data_name(self, data_name):
        # data_name is no less than 3 group words like 'upbit-btc-240' or 'upbit-btc-240-chart'
        groups = data_name.split('-')
        assert 3 <= len(groups)
        exchange = groups[0]
        market = groups[1]
        candle_unit = groups[2]
        return exchange, market, candle_unit

    def func_relativedelta(self, candle_unit):
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

    def check_next_date_integrity(self, data_file_path, date_next_expected):
        if date_next_expected is None: return 0
        date_next_expected = datetime.datetime.fromisoformat(date_next_expected)

        # Fetch the actual next date
        data_name = os.path.splitext(os.path.basename(data_file_path))[0]
        _, _, candle_unit = self.parse_data_name(data_name)
        file = open(data_file_path, 'r')
        for record in file.readlines(): continue
        file.close()
        date_latest = datetime.datetime.fromisoformat(record.split(',')[0])
        date_next_actual = date_latest + self.func_relativedelta(candle_unit)(1)
        print(f'Expected Next Date: {date_next_expected.isoformat()} / Actual Next Date: {date_next_actual.isoformat()}')

        # Compare the next dates
        if date_next_actual < date_next_expected:
            return -1
        elif date_next_actual == date_next_expected:
            return 0
        else:
            return 1
