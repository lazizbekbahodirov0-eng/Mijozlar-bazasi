import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from docx import Document
from docx.shared import Pt
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

# --- SHARTNOMA YARATISH FUNKSIYASI (TO'LIQ MATN) ---
def generate_contract(d):
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)

    def add_centered_bold(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True

    def add_justified(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(text)

    # SARLAVHA
    add_centered_bold(f"Махсулот қийматини бўлиб тўлаш шарти билан тузилган\n№ {d['nomer']}- сонли олди сотди\nШАРТНОМА")
    doc.add_paragraph(f"{d['sana']} йил").alignment = WD_ALIGN_PARAGRAPH.CENTER

    # KIRISH
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run("Мен ")
    p.add_run(d['ism']).bold = True
    p.add_run(f" Узбекистон Фукароси, паспорт № {d['pasport']} {d['pas_sana']} йилда {d['pas_joy']} томонидан берилган, {d['manzil']} истиқомат қилувчи, телефон {d['tel']} «Харидор» бир тарафдан ва OOO \"NEW DREAMS STAR\" номидан директор Нурбеков У.Ю. иккинчи тарафдан ушбу шартномани туздик.")

    # BARCHA BANDLAR
    sections = [
        ("1. Шартнома предмети", "1.1. Сотувчи товарларни Харидорнинг эгалигига топшириш, Харидор эса қийматини бўлиб тўлаш мажбуриятини олади. 1.2. Товар тўлиқ тўлангунга қадар гаровда ҳисобланади."),
        ("2. Шартнома суммаси ва ҳисоб-китоблар", "2.1. Шартнома суммаси 1-иловада. 2.5. Қолган сумма тўлов графиги (2-илова) асосида тўлаб борилади."),
        ("3. Товарни тақдим қилиш тартиби", "3.1. Сотувчи ҳужжатлар расмийлаштирилгач товарни етказиб беради."),
        ("4. Товарларга тўлов киритиш тартиби", "4.3. Тўлов карта, нақд пул ёки банк ўтказмаси орқали амалга оширилади."),
        ("5. Сотувчининг назорати", "5.1. Харидор маълумотлари ўзгарса, Сотувчини хабардор қилиши шарт."),
        ("6. Кафолатлар", "6.1. Харидор тўловларни кафолатлайди."),
        ("7. Муддатдан олдин қайтариш", "7.1. Тўлов кечикса, Сотувчи қарзни тўлиқ қайтаришни талаб қилишга ҳақли."),
        ("8. Тарафларнинг мажбуриятлари", "8.1. Сотувчи сифатли товар етказиши, Харидор эса ўз вақтида тўлаши шарт."),
        ("9. Тарафларнинг ҳуқуқлари", "9.1. Сотувчи тўловни талаб қилиш, Харидор эса товар сифатини текшириш ҳуқуқига эга."),
        ("10. Тарафларнинг масъулияти", f"10.5. Тўлов кечиктирилган ҳар бир кун учун {d['summa']} сўмдан 2.0 % жарима ҳисобланади."),
        ("11. Товарни топшириш шартлари", "11.1. Товар фақат Харидорга ҳужжат асосида берилади."),
        ("12. Форс-мажор", "12.1. Енгиб бўлмас кучлар таъсирида масъулият чекланади."),
        ("13. Шартномани ўзгартириш", "13.1. Ўзгартиришлар фақат ёзма равишда амалга оширилади."),
        ("14. Низоларни ҳал қилиш", "14.1. Низолар музокара ёки суд йўли билан ҳал этилади."),
        ("15. Якуний қоидалар", "15.4. Ушбу шартнома имзоланган кундан кучга киради.")
    ]

    for title, body in sections:
        p_title = doc.add_paragraph()
        p_title.add_run(title).bold = True
        add_justified(body)

    # ILOVALAR
    doc.add_page_break()
    add_centered_bold("1-илова\nТовар спецификацияси")
    table = doc.add_table(rows=2, cols=4)
    table.style = 'Table Grid'
    cells = table.rows[0].cells
    cells[0].text, cells[1].text, cells[2].text, cells[3].text = "Махсулот", "Микдор", "Нарх", "Жами"
    row = table.rows[1].cells
    row[0].text, row[1].text, row[2].text, row[3].text = d['mahsulot'], "1", d['summa'], d['summa']

    # FAYLNI SAQLASH
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFEYS ---
st.sidebar.markdown("# 🚀 Boshqaruv")
tanlov = st.sidebar.radio("Bo'lim:", ["📊 Statistika", "📋 Ro'yxat", "📄 Shartnoma yaratish"])

if tanlov == "📄 Shartnoma yaratish":
    st.header("📄 Shartnoma generatori")
    
    # Formadan tashqarida ma'lumotlarni yig'amiz
    with st.form("contract_form"):
        col1, col2 = st.columns(2)
        with col1:
            nomer = st.text_input("Shartnoma №:", "3080")
            sana = st.text_input("Sana:", "27.12.2025")
            ism = st.text_input("Mijoz F.I.SH:", "URINBAYEB SHOHJAHON SHAROF O’G’LI")
            pas = st.text_input("Pasport:", "AD6259891")
            pas_sana = st.text_input("Berilgan sana:", "23.02.2024")
        with col2:
            pas_joy = st.text_input("Bergan joy:", "JIZZAX VILOYATI IIV")
            manzil = st.text_area("Manzil:", "JIZZAX VILOYATI TOSHLOQ QFY")
            tel = st.text_input("Tel:", "90 487 97 77")
            mahsulot = st.text_input("Mahsulot:", "IPHONE 13 PRO")
            summa = st.text_input("Summa:", "5 436 000")
            oylik = st.text_input("Oylik:", "906 000")
        
        submitted = st.form_submit_button("Ma'lumotlarni tasdiqlash")

    # TUGMA FORMADAN TASHQARIDA
    if submitted:
        data = {
            'nomer': nomer, 'sana': sana, 'ism': ism, 'pasport': pas,
            'pas_sana': pas_sana, 'pas_joy': pas_joy, 'manzil': manzil,
            'tel': tel, 'mahsulot': mahsulot, 'summa': summa, 'oylik': oylik
        }
        word_file = generate_contract(data)
        st.success("✅ Shartnoma tayyor! Pastdagi tugmani bosing.")
        st.download_button(
            label="📥 Tayyor Word faylni yuklab olish",
            data=word_file,
            file_name=f"Shartnoma_{nomer}_{ism}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
