import argparse
import datetime
import pandas as pd
from bin import util

COLUMNS_OHLC_CHART = ['date', 'open', 'high', 'low', 'close', 'volume']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--rollup_window', type=int, required=True)
    args = parser.parse_args()

    print(f'Converting from {args.input_path} to {args.output_path}')

    data = pd.read_csv(args.input_path, header=0, converters={'date': lambda x: datetime.datetime.fromisoformat(x)})

    # Roll up the OHLC candles
    data['high'] = pd.DataFrame({'high': [ data.loc[row:row+args.rollup_window-1, 'high'].max() for row in range(len(data)) ]})
    data['low'] = pd.DataFrame({'low': [ data.loc[row:row+args.rollup_window-1, 'low'].min() for row in range(len(data)) ]})
    data['close'] = pd.DataFrame({'close': [ data.loc[min(row+args.rollup_window-1, len(data)-1), 'close'] for row in range(len(data)) ]})
    data['volume'] = pd.DataFrame({'volume': [ data.loc[row:row+args.rollup_window-1, 'volume'].sum() for row in range(len(data)) ]})
    data_out = data[data.index % args.rollup_window == 0]

    # Open the output file
    output_file, output_cw = util.open_csv_file(args.output_path, COLUMNS_OHLC_CHART, True)

    # Write values
    for _, row in data_out[COLUMNS_OHLC_CHART].iterrows():
        output_cw.writerow([ util.to_simple_str(value) for value in row ])
    output_file.close()

    print('Converted')
