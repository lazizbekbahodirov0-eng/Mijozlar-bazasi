import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- SAHIFANI SOZLASH ---
st.set_page_config(page_title="Mijozlar Baza Cloud", layout="wide", page_icon="📝")

# --- GOOGLE SHEETS ULANISH ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Secrets sozlamalarini tekshiring!")
    st.stop()

# --- LOGIN TIZIMI ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 Tizimga kirish")
    user = st.text_input("Login:")
    pas = st.text_input("Parol:", type="password")
    if st.button("Kirish"):
        if user == "admin" and pas == "12345":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Xato!")
    st.stop()

# --- WORD SHABLON YARATISH FUNKSIYASI ---
def shartnoma_yaratish(data):
    doc = Document()
    
    # Stil sozlamalari
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    # Sarlavha
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"Махсулот қийматини бўлиб тўлаш шарти билан тузилган\n№ {data['nomer']}- сонли олди сотди\nШАРТНОМА")
    run.bold = True
    
    doc.add_paragraph(f"\n{data['sana']} yil").alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Kirish qismi
    p2 = doc.add_paragraph()
    p2.add_run(f"Мен {data['ism']}, ").bold = True
    p2.add_run(f"Узбекистон Фукароси, паспорт № {data['pasport']}, {data['pasport_sana']}da {data['pasport_joy']} томонидан берилган, {data['manzil']} манзилда истиқомат қилувчи, телефон {data['tel']} «Харидор» бир тарафдан ва OOO \"NEW DREAMS STAR\" номидан директор Нурбеков У.Ю. иккинчи тарафдан...")

    # Bu yerga shartnomaning qolgan 15 ta bandini matnini qo'shish mumkin
    doc.add_heading('1. Шартнома предмети', level=1)
    doc.add_paragraph(f"1.1. Сотувчи {data['mahsulot']}ни Харидорга топширади...")

    doc.add_heading('Нарх ва Тўлов', level=1)
    doc.add_paragraph(f"Жами сумма: {data['summa']} сўм. Ойлик тўлов: {data['oylik']} сўм.")

    # Faylni xotiraga saqlash
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- ASOSIY MENYU ---
st.sidebar.markdown("# 🚀 Boshqaruv")
tanlov = st.sidebar.radio("Bo'limni tanlang:", ["📊 Statistika", "📋 Ro'yxat", "📄 Shartnoma yaratish"])

if tanlov == "📊 Statistika":
    df = conn.read(ttl=0)
    st.metric("Jami mijozlar", len(df))
    st.dataframe(df, width='stretch')

elif tanlov == "📋 Ro'yxat":
    df = conn.read(ttl=0)
    st.table(df)

elif tanlov == "📄 Shartnoma yaratish":
    st.header("📄 Yangi Shartnoma tayyorlash")
    st.info("Qizil harflar bilan yozilgan ma'lumotlarni kiriting")
    
    col1, col2 = st.columns(2)
    with col1:
        nomer = st.text_input("Shartnoma №:", "3080")
        sana = st.text_input("Sana:", "27.12.2025")
        fio = st.text_input("Mijoz F.I.SH:", "URINBAYEB SHOHJAHON SHAROF O’G’LI")
        pas_num = st.text_input("Pasport seriya:", "AD6259891")
        pas_sana = st.text_input("Berilgan sana:", "23.02.2024Y")
    with col2:
        pas_joy = st.text_input("Kim tomonidan berilgan:", "JIZZAX VILOYATI JIZZAX SHAXAR IIV")
        manzil = st.text_area("Yashash manzili:", "JIZZAX VILOYATI JIZZAX SHAXAR TOSHLOQ QFY")
        tel = st.text_input("Telefon:", "90 487 97 77")
        mahsulot = st.text_input("Mahsulot nomi:", "IPHONE 13 PRO")
        summa = st.text_input("Jami summa:", "5 436 000")
        oylik = st.text_input("Oylik to'lov:", "906 000")

    if st.button("Word faylni tayyorlash"):
        data = {
            'nomer': nomer, 'sana': sana, 'ism': fio, 'pasport': pas_num,
            'pasport_sana': pas_sana, 'pasport_joy': pas_joy, 'manzil': manzil,
            'tel': tel, 'mahsulot': mahsulot, 'summa': summa, 'oylik': oylik
        }
        word_fayl = shartnoma_yaratish(data)
        st.download_button(
            label="📥 Shartnomani yuklab olish (.docx)",
            data=word_fayl,
            file_name=f"Shartnoma_{nomer}_{fio}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
