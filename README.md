# DailyCrypto

![test workflow](https://github.com/whalequant/DailyCrypto/actions/workflows/test.yml/badge.svg)

### Example 1: Data Cleanse
```console
python3 -m bin.cleanser --input_path upbit-btc-5-raw.csv --output_path upbit-btc-5-chart.csv
```

### Example 2: Data Convert
```console
python3 -m bin.converter --input_path upbit-btc-5-chart.csv --output_path upbit-btc-30-chart.csv --rollup_window 6
```
