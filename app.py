import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- SAHIFANI SOZLASH (2026 yangi standartida) ---
st.set_page_config(page_title="Mijozlar Baza Cloud", layout="wide", page_icon="☁️")

# --- GOOGLE SHEETS BILAN ULANISH ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Xato: Secrets sozlamalarida Google Sheets linki topilmadi!")
    st.stop()

# --- LOGIN TIZIMI ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 Bulutli tizimga kirish")
    user = st.text_input("Login:")
    pas = st.text_input("Parol:", type="password")
    if st.button("Kirish"):
        if user == "admin" and pas == "12345":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Login yoki parol xato!")
    st.stop()

# --- ASOSIY DASTUR ---
st.sidebar.markdown("# ☁️ Cloud Baza 2026")
tanlov = st.sidebar.radio("Bo'lim:", ["📊 Statistika", "🆕 Yangi qo'shish", "📋 Ro'yxat"])

if st.sidebar.button("Chiqish"):
    st.session_state['logged_in'] = False
    st.rerun()

# Ma'lumotlarni olish
try:
    df = conn.read(ttl=0)
except Exception as e:
    st.error(f"Ma'lumotlarni o'qib bo'lmadi. Secrets-ni tekshiring! Xato: {e}")
    st.stop()

if tanlov == "📊 Statistika":
    st.header("📊 Umumiy holat")
    st.metric("Jami mijozlar", len(df))
    st.dataframe(df, width='stretch')

elif tanlov == "🆕 Yangi qo'shish":
    st.subheader("🆕 Yangi mijoz qo'shish")
    with st.form("shakl"):
        ism = st.text_input("Ism:")
        tel = st.text_input("Telefon:")
        manzil = st.text_area("Manzil:")
        submit = st.form_submit_button("Google Sheets-ga saqlash")
        
        if submit:
            if ism and tel:
                yangi_mijoz = pd.DataFrame([{"ism": ism, "telefon": tel, "manzil": manzil}])
                yangilangan_df = pd.concat([df, yangi_mijoz], ignore_index=True)
                conn.update(data=yangilangan_df)
                st.success("✅ Ma'lumot Google Sheets-ga saqlandi!")
                st.rerun()
            else:
                st.warning("Ism va telefonni kiriting!")

elif tanlov == "📋 Ro'yxat":
    st.subheader("📋 Mijozlar ro'yxati")
    qidiruv = st.text_input("🔍 Ism bo'yicha qidirish:")
    if qidiruv:
        df = df[df['ism'].str.contains(qidiruv, case=False, na=False)]
    st.dataframe(df, width='stretch')
