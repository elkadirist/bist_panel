import streamlit as st
import pandas as pd

st.set_page_config(page_title="BIST Robot", layout="wide")

st.title("📊 BIST ROBOT (STABLE MODE)")

st.success("Uygulama çalışıyor - sistem OK")

data = {
    "Hisse": ["THYAO", "ASELS", "TUPRS", "ASTOR"],
    "Durum": ["🟢 AL", "🟡 BEKLE", "🔴 SAT", "🟢 AL"],
    "Skor": [80, 55, 30, 90]
}

df = pd.DataFrame(data)

st.dataframe(df)
