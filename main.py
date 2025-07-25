import yfinance as yf
import pandas as pd
import ta

def fetch_signals(ticker):
    df = yf.download(ticker, period='3mo', interval='1d')
    df.dropna(inplace=True)

    df['EMA21'] = ta.trend.ema_indicator(df['Close'], window=21).ema_indicator()
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd_diff()

    latest = df.iloc[-1]

    signal = None
    if (
        latest['Close'] > latest['EMA21']
        and latest['RSI'] < 40
        and latest['MACD'] > 0
    ):
        signal = "Buy CALL Option"

    strike_price = round(latest['Close'] * 1.02, 2)  # Recommend 2% OTM CALL
    expiry_days = 30  # Recommend 30 days from today
    from datetime import datetime, timedelta
    expiry_date = (datetime.now() + timedelta(days=expiry_days)).strftime('%Y-%m-%d')

    return {
        "ticker": ticker,
        "price": round(latest['Close'], 2),
        "signal": signal or "No Signal",
        "strike": strike_price,
        "expiry": expiry_date,
        "rsi": round(latest['RSI'], 2),
        "macd": round(latest['MACD'], 4)
    }

def scan_top_stocks():
    top10 = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "UNH", "JNJ"]
    results = []
    for ticker in top10:
        if ticker == "BRK-B":
            ticker = "BRK-B"
        result = fetch_signals(ticker)
        results.append(result)
    return results
