import os
import argparse
import datetime
import pandas as pd
from bin import util

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    args = parser.parse_args()

    print(f'Cleansing from {args.input_path} to {args.output_path}')

    # Open the input file
    data = pd.read_csv(args.input_path, header=0, converters={'date': lambda x: datetime.datetime.fromisoformat(x)})

    # Scan ranges for missing values
    missing_ranges = []
    i_prev_ok = None
    for i, row in data.iterrows():
        if row.isnull().values.any():
            if i_prev_ok is None:
                i_prev_ok = i-1
        else:
            if i_prev_ok is not None:
                i_next_ok = i
                missing_ranges.append((i_prev_ok, i_next_ok))
                i_prev_ok = None
    if i_prev_ok is not None:
        raise Exception(f'{missing_ranges} {i_prev_ok}')

    # Interpolate for each missing range
    for i_prev_ok, i_next_ok in missing_ranges:
        len_range = i_next_ok - i_prev_ok
        for col_name in data.columns[1:]: # Ignore 'date' column
            step_size = float(data.loc[i_next_ok, col_name] - data.loc[i_prev_ok, col_name]) / len_range
            for i_row in range(i_prev_ok+1, i_next_ok):
                data.loc[i_row, col_name] = data.loc[i_prev_ok, col_name] + step_size*(i_row-i_prev_ok)

    # Check the date integrity
    data_name = os.path.splitext(os.path.basename(args.input_path))[0]
    _, _, candle_unit = util.parse_data_name(data_name)
    acc_date = data['date'][0]
    for i, row in data.iterrows():
        cur_date = row['date']
        if acc_date != cur_date:
            raise Exception(acc_date, cur_date)
        acc_date += util.func_relativedelta(candle_unit)(1)

    # Write values
    output_file, output_cw = util.open_csv_file(args.output_path, data.columns, True)
    for _, row in data.iterrows():
        output_cw.writerow([ util.to_simple_str(value) for value in row ])
    output_file.close()

    print('Cleansed')
