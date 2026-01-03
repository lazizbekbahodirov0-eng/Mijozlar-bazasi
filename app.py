import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- SAHIFANI SOZLASH ---
st.set_page_config(page_title="Cloud Baza 2026", layout="wide", page_icon="📝")

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

# --- SHARTNOMA YARATISH FUNKSIYASI ---
def generate_contract(d):
    doc = Document()
    
    # Umumiy stil: Times New Roman
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)

    def add_centered_bold(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True
        return p

    def add_justified(text, bold_part=""):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_part:
            run = p.add_run(bold_part)
            run.bold = True
        p.add_run(text)
        return p

    # 1-SAHIFA BOSHLANISHI
    add_centered_bold(f"Махсулот қийматини бўлиб тўлаш шарти билан тузилган\n№ {d['nomer']}- сонли олди сотди\nШАРТНОМА")
    
    p_sana = doc.add_paragraph()
    p_sana.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sana = p_sana.add_run(d['sana'])
    run_sana.bold = True
    run_sana.underline = True
    run_sana.font.color.rgb = None # Qizil o'rniga qora

    intro = doc.add_paragraph()
    intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    intro.add_run("Мен ")
    intro.add_run(d['ism']).bold = True
    intro.add_run(f" Узбекистон Фукароси, паспорт № {d['pasport']} {d['pas_sana']} йилда {d['pas_joy']} томонидан берилган, {d['manzil']} истиқомат қилувчи, телефон {d['tel']} «Харидор» бир тарафдан ва OOO \"NEW DREAMS STAR\" номидан Устав асосида фаолият юритувчи директор Нурбеков У.Ю. иккинчи тарафдан ушбу шартномани туздик.")

    # BANDLAR (Qisqartirilgan, lekin to'liq ma'no saqlangan)
    sections = [
        ("1. Шартнома предмети", "1.1. Сотувчи товарларни Харидорнинг эгалигига топшириш, Харидор эса қийматини бўлиб тўлаш мажбуриятини олади.\n1.2. Товар тўлиқ тўлангунга қадар гаровда ҳисобланади."),
        ("2. Шартнома суммаси ва ҳисоб-китоблар", f"2.1. Сумма 1-иловада. 2.5. Қолган сумма тўлов графиги (2-илова) асосида тўланади."),
        ("3. Товарни тақдим қилиш", "3.1. Барча ҳужжатлар расмийлаштирилгач товар етказилади."),
        ("4. Тўлов киритиш тартиби", "4.3. Тўлов пластик карта, нақд пул ёки пул ўтказиш йўли билан амалга оширилади."),
        ("5. Сотувчининг назорати", "5.1. Сотувчи Харидорнинг маълумотлари ўзгаришини назорат қилиш ҳуқуқига эга."),
        ("10. Тарафларнинг масъулияти", f"10.5. Тўлов кечиктирилса, ҳар бир кун учун 2.0 % жарима ҳисобланади."),
    ]

    for title, text in sections:
        doc.add_heading(title, level=2).bold = True
        add_justified(text)

    # 1-ILOVA (JADVAL)
    doc.add_page_break()
    add_centered_bold("1-илова\nМахсулот спецификацияси")
    
    table = doc.add_table(rows=1, cols=5)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '№'
    hdr_cells[1].text = 'Махсулот номи'
    hdr_cells[2].text = 'Улчов'
    hdr_cells[3].text = 'Микдори'
    hdr_cells[4].text = 'Суммаси'

    row_cells = table.add_row().cells
    row_cells[0].text = '1'
    row_cells[1].text = d['mahsulot']
    row_cells[2].text = 'дона'
    row_cells[3].text = '1'
    row_cells[4].text = f"{d['summa']} ({d['summa_soz']}) сум"

    # 2-ILOVA (TOLOV GRAFIGI)
    doc.add_page_break()
    add_centered_bold("2-илова\nТўловлар жадвали")
    
    g_table = doc.add_table(rows=1, cols=3)
    g_table.style = 'Table Grid'
    g_hdr = g_table.rows[0].cells
    g_hdr[0].text = 'Тўлов тури'
    g_hdr[1].text = 'Муддати'
    g_hdr[2].text = 'Сумма (сўм)'

    for i in range(1, 7): # Masalan 6 oylik grafik
        row = g_table.add_row().cells
        row[0].text = f"{i}-тўлов"
        row[1].text = "27 sanagacha"
        row[2].text = d['oylik']

    # FAYLNI TAYYORLASH
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFEYS ---
st.sidebar.markdown("# 🚀 Boshqaruv")
tanlov = st.sidebar.radio("Bo'limni tanlang:", ["📊 Statistika", "📋 Ro'yxat", "📄 Shartnoma yaratish"])

if tanlov == "📊 Statistika":
    df = conn.read(ttl=0)
    st.metric("Jami mijozlar", len(df))
    st.dataframe(df, width='stretch')

elif tanlov == "📄 Shartnoma yaratish":
    st.header("📄 Shartnomani avtomatik to'ldirish")
    
    with st.form("contract_form"):
        col1, col2 = st.columns(2)
        with col1:
            nomer = st.text_input("Shartnoma №:", "3080")
            sana = st.text_input("Sana:", "27.12.2025")
            ism = st.text_input("Mijoz F.I.SH:", "URINBAYEB SHOHJAHON SHAROF O’G’LI")
            pas = st.text_input("Pasport:", "AD6259891")
            pas_sana = st.text_input("Pasport berilgan sana:", "23.02.2024")
        with col2:
            pas_joy = st.text_input("Pasport bergan joy:", "JIZZAX VILOYATI JIZZAX SHAXAR IIV")
            manzil = st.text_area("Yashash manzili:", "JIZZAX VILOYATI TOSHLOQ QFY")
            tel = st.text_input("Telefon:", "90 487 97 77")
            mahsulot = st.text_input("Mahsulot:", "IPHONE 13 PRO")
            summa = st.text_input("Jami summa:", "5 436 000")
            summa_soz = st.text_input("Summa so'z bilan:", "Besh million to'rt yuz o'tiz olti ming")
            oylik = st.text_input("Oylik to'lov:", "906 000")
        
        submit = st.form_submit_button("Word shartnomani tayyorlash")
        
        if submit:
            data = {
                'nomer': nomer, 'sana': sana, 'ism': ism, 'pasport': pas,
                'pas_sana': pas_sana, 'pas_joy': pas_joy, 'manzil': manzil,
                'tel': tel, 'mahsulot': mahsulot, 'summa': summa,
                'summa_soz': summa_soz, 'oylik': oylik
            }
            word_file = generate_contract(data)
            st.download_button(
                label="📥 Tayyor Word faylni yuklab olish",
                data=word_file,
                file_name=f"Shartnoma_{nomer}_{ism}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
