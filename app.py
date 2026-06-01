import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="BIST AKILLI AL/SAT ROBOT", layout="wide")

st.title("📊 AKILLI AL/SAT ROBOTU (GÜÇLENDİRİLMİŞ)")

stocks = [
    "THYAO.IS","ASELS.IS","TUPRS.IS","ASTOR.IS",
    "KCHOL.IS","SISE.IS","BIMAS.IS","SAHOL.IS","EKGYO.IS"
]

def analyze(df):
    df = df.copy()

    close = df["Close"].squeeze()
    volume = df["Volume"].squeeze()

    if len(close) < 60:
        return 0

    # EMA trend
    ema20 = close.ewm(span=20).mean()
    ema50 = close.ewm(span=50).mean()

    # RSI
    rsi = ta.momentum.RSIIndicator(close=close).rsi()

    # MACD
    macd = ta.trend.MACD(close=close)
    macd_line = macd.macd()
    signal_line = macd.macd_signal()

    score = 0

    # Trend gücü
    if ema20.iloc[-1] > ema50.iloc[-1]:
        score += 35
    else:
        score -= 20

    # RSI filtre
    if 45 < rsi.iloc[-1] < 70:
        score += 25
    elif rsi.iloc[-1] > 75:
        score -= 25

    # MACD momentum
    if macd_line.iloc[-1] > signal_line.iloc[-1]:
        score += 25

    # Hacim
    if volume.iloc[-1] > volume.mean():
        score += 15

    return score


results = []

for stock in stocks:
    try:
        df = yf.download(stock, period="6mo", interval="1d")

        if df is None or len(df) < 60:
            continue

        score = analyze(df)

        if score >= 80:
            signal = "🟢 GÜÇLÜ AL"
        elif score >= 60:
            signal = "🟡 AL SINYALİ"
        elif score >= 40:
            signal = "🟠 ZAYIF"
        else:
            signal = "🔴 SAT / UZAK DUR"

        results.append([stock, score, signal])

    except:
        continue


table = pd.DataFrame(results, columns=["Hisse", "Skor", "Sinyal"])
table = table.sort_values("Skor", ascending=False)

st.dataframe(table, use_container_width=True)

st.subheader("🔥 Güçlü AL Adayları")
st.dataframe(table[table["Skor"] >= 80])
