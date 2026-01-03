import streamlit as st
import sqlite3
import pandas as pd

# --- SAHIFANI SOZLASH ---
st.set_page_config(page_title="Mijozlar Baza Pro", layout="wide", page_icon="💼")

# --- MA'LUMOTLAR BAZASI ---
def baza_yaratish():
    conn = sqlite3.connect('malumotlar.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mijozlar 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, ism TEXT, telefon TEXT, manzil TEXT)''')
    conn.commit()
    conn.close()

def malumotlarni_olish():
    conn = sqlite3.connect('malumotlar.db')
    df = pd.read_sql_query("SELECT * FROM mijozlar", conn)
    conn.close()
    return df

# --- LOGIN TIZIMI ---
def login():
    st.title("🔐 Tizimga kirish")
    st.info("Login: admin | Parol: 12345")
    
    username = st.text_input("Loginni kiriting:")
    password = st.text_input("Parolni kiriting:", type="password")
    
    if st.button("Kirish"):
        if username == "admin" and password == "12345":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Login yoki parol xato!")

# --- ASOSIY DASTUR ---
def asosiy_dastur():
    baza_yaratish()
    
    st.sidebar.markdown("# 🚀 Boshqaruv")
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    
    tanlov = st.sidebar.radio("Bo'limni tanlang:", ["📊 Statistika", "🆕 Yangi qo'shish", "📋 Ro'yxat va Qidiruv", "🗑 O'chirish"])
    
    if st.sidebar.button("Chiqish (Logout)"):
        st.session_state['logged_in'] = False
        st.rerun()

    if tanlov == "📊 Statistika":
        st.header("📊 Umumiy statistika")
        df = malumotlarni_olish()
        st.metric(label="Jami mijozlar soni", value=len(df))

    elif tanlov == "🆕 Yangi qo'shish":
        st.subheader("🆕 Yangi mijoz kiritish")
        with st.form("shakl"):
            ism = st.text_input("Mijozning ismi:")
            tel = st.text_input("Telefon raqami:")
            manzil = st.text_area("Manzili:")
            saqlash = st.form_submit_button("Bazaga saqlash")
            
            if saqlash:
                if ism and tel:
                    conn = sqlite3.connect('malumotlar.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO mijozlar (ism, telefon, manzil) VALUES (?, ?, ?)', (ism, tel, manzil))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ {ism} saqlandi!")
                else:
                    st.warning("Ism va telefonni to'ldiring!")

    elif tanlov == "📋 Ro'yxat va Qidiruv":
        st.subheader("📋 Mijozlar ro'yxati")
        df = malumotlarni_olish()
        if not df.empty:
            qidiruv = st.text_input("🔍 Qidirish:")
            if qidiruv:
                df = df[df['ism'].str.contains(qidiruv, case=False) | df['telefon'].str.contains(qidiruv)]
            st.dataframe(df[['ism', 'telefon', 'manzil']], use_container_width=True)
        else:
            st.info("Baza bo'sh.")

    elif tanlov == "🗑 O'chirish":
        st.subheader("🗑 Ma'lumotni o'chirish")
        df = malumotlarni_olish()
        if not df.empty:
            tanlov_och = st.selectbox("O'chirmoqchi bo'lgan mijozni tanlang:", df['ism'].tolist())
            if st.button("O'chirishni tasdiqlash", type="primary"):
                conn = sqlite3.connect('malumotlar.db')
                c = conn.cursor()
                c.execute('DELETE FROM mijozlar WHERE ism = ?', (tanlov_och,))
                conn.commit()
                conn.close()
                st.success(f"{tanlov_och} o'chirildi!")
                st.rerun()

# --- DASTURNI BOSHQARISH ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    asosiy_dastur()
else:
    login()