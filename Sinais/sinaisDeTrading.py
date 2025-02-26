# engolfo e inside bar

candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR)


def is_bullish_engulfing(prev_candle, curr_candle):
    return (prev_candle['close'] < prev_candle['open'] and
            curr_candle['close'] > curr_candle['open'] and
            curr_candle['close'] > prev_candle['open'] and
            curr_candle['open'] < prev_candle['close'])

def is_bearish_engulfing(prev_candle, curr_candle):
    return (prev_candle['close'] > prev_candle['open'] and
            curr_candle['close'] < curr_candle['open'] and
            curr_candle['open'] > prev_candle['close'] and
            curr_candle['close'] < prev_candle['open'])


def is_inside_bar(prev_candle, curr_candle):
    return (curr_candle['high'] < prev_candle['high'] and
            curr_candle['low'] > prev_candle['low'])

for i in range(1, len(candles)):
    prev_candle = {
        'open': float(candles[i-1][1]),
        'high': float(candles[i-1][2]),
        'low': float(candles[i-1][3]),
        'close': float(candles[i-1][4])
    }
    curr_candle = {
        'open': float(candles[i][1]),
        'high': float(candles[i][2]),
        'low': float(candles[i][3]),
        'close': float(candles[i][4])
    }

    if is_bullish_engulfing(prev_candle, curr_candle):
        print(f"Bullish Engulfing detected at index {i}")
    elif is_bearish_engulfing(prev_candle, curr_candle):
        print(f"Bearish Engulfing detected at index {i}")
    elif is_inside_bar(prev_candle, curr_candle):
        print(f"Inside Bar detected at index {i}")
