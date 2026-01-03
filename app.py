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

# --- ASIL NUSXADAGI SHARTNOMA GENERATORI ---
def generate_full_contract(d):
    doc = Document()
    
    # Umumiy shrift sozlamalari
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)

    def add_para(text, bold=False, align="justify", size=11):
        p = doc.add_paragraph()
        if align == "center": p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif align == "right": p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else: p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        run = p.add_run(text)
        run.bold = bold
        run.font.size = Pt(size)
        return p

    # 1-SAHIFA
    add_para("Махсулот қийматини бўлиб тўлаш шарти билан тузилган", bold=True, align="center", size=12)
    add_para(f"№ {d['nomer']}- сонli олди сотди", bold=True, align="center", size=12)
    add_para("ШАРТНОМА", bold=True, align="center", size=14)
    add_para(f"{d['sana']}", bold=True, align="center")

    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p1.add_run("Мен ")
    p1.add_run(d['ism']).bold = True
    p1.add_run(f" Узбекистон Фукароси, паспорт № {d['pasport']} {d['pas_sana']} йилда {d['pas_joy']} томониdan berilgan, {d['manzil']} истиқомат қилувчи, телефон {d['tel']} «Харидор» бир тарафдан ва OOO \"NEW DREAMS STAR\" номидан Устав асосида фаолият юритувчи ва кейинги ўринларда “Сотувчи” деб номланувчи директор Нурбеков У.Ю. иккинчи тарафдан ушбу шартномани қуйидагилар ҳақида туздик:")

    # 1-BAND
    add_para("1. Шартнома предмети", bold=True, align="center")
    add_para("1.1. Ушбу Шартномага асосан “Сотувчи” товарларни “Харидор”нинг эгалигига топшириш, “Харидор” эса ушбу товарларни қабул қилиб олиш ва уlar учун белгиланган қийматни бўлиб тўлаш мажбуриятини ўз зиммаларига оладилар.")
    add_para("1.2. Товарлар харидорга тўлик топширилган вақтдан бошлаб, унинг қиймати тўлиқ тўланишига қадар, сотилgan товарлар харидорнинг қарзини тўлаш мажбуриятини бажаришини таъминлаш учун сотувчи томонидан гаровга олинган деб тан олинади.")

    # 2-BAND
    add_para("2. Шартнома суммаси ва ҳисоб-китоблар тартиби", bold=True, align="center")
    add_para(f"2.1. Ушбу Шартноманинг суммаси 1-иловада. 2.2. Товар “Харидор”га муддатли тўлов шартларида топширилади. 2.4. Харидор товарни қабул қилишдан асоссиз бош тортса, аванс тўловининг 50% миқдорида жарима тўлайди.")

    # 3-4 BANDLAR
    add_para("3. Товарни тақдим қилиш тартиби", bold=True, align="center")
    add_para("3.1. Сотувчи ҳужжатlar расмийлаштирилгач товарни етказиб беради. 3.2. Товар топширилган сана далолатнома билан тасдиқланади.")
    
    add_para("4. Товарларга тўлов киритиш тартиби", bold=True, align="center")
    add_para(f"4.1. Тўлов 2-иловадаги жадвал асосида қилинади. 4.4. Тўланган пуллар аввало жарима тўловига, сўнгра қарздорликни қоплашга йўналтирилади.")

    # 5-10 BANDLAR (To'liq matn bilan)
    doc.add_page_break()
    add_para("5. Сотувчининг назорати", bold=True, align="center")
    add_para("5.1. Харидор паспорт маълумотлари ёки манзили ўзгарса 3 кун ichida хабар бериши шарт.")
    
    add_para("7. Қарзнинг қолган қисмини муддатдан олдин қайтарилиши", bold=True, align="center")
    add_para("7.1. Тўлов кечиктирилса Сотувчи қарзни тўлиқ қайтаришни талаб қилишга ҳақли.")

    add_para("10. Тарафларнинг масъулияти", bold=True, align="center")
    add_para(f"10.5. Тўлов муддати ўтса, Харидор ҳар бир кун учун {d['summa']} сўмдан 2.0 % жарима тўлайди.")
    add_para("10.8. Сотувчи уяли алоқа воситасини масофадан туриб (Apple ID/Gmail) орқали қулфлаб қўйиш ҳуқуқига эга.")

    # ILOVALAR
    doc.add_page_break()
    add_para("1-илова", bold=True, align="center")
    add_para("Товар спецификацияси", bold=True, align="center")
    table1 = doc.add_table(rows=2, cols=4, style='Table Grid')
    cols = table1.rows[0].cells
    cols[0].text, cols[1].text, cols[2].text, cols[3].text = "Махсулот", "Микдор", "Нарх", "Сумма"
    r = table1.rows[1].cells
    r[0].text, r[1].text, r[2].text, r[3].text = d['mahsulot'], "1", d['summa'], d['summa']
    add_para(f"ЖАМИ: {d['summa']} ({d['summa_soz']}) сўм.", bold=True)

    doc.add_page_break()
    add_para("2-илова", bold=True, align="center")
    add_para("Тўловлар жадвали", bold=True, align="center")
    table2 = doc.add_table(rows=1, cols=3, style='Table Grid')
    h2 = table2.rows[0].cells
    h2[0].text, h2[1].text, h2[2].text = "Тўлов тури", "Муддати", "Сумма"
    for i in range(1, int(d['oylar']) + 1):
        row = table2.add_row().cells
        row[0].text, row[1].text, row[2].text = f"{i}-тўлов", f"27.{i:02d}.2026 гача", d['oylik']

    # IMZOLAR
    doc.add_page_break()
    add_para("ТАРАФЛАРНИNG ИМЗОЛАРИ", bold=True, align="center")
    sig_t = doc.add_table(rows=2, cols=2)
    sig_t.rows[0].cells[0].text, sig_t.rows[0].cells[1].text = "ХАРИДОР", "СОТУВЧИ"
    b_r = sig_t.rows[1].cells
    b_r[0].text = f"{d['ism']}\nПаспорт: {d['pasport']}\nТел: {d['tel']}\n\n________ (имзо)"
    b_r[1].text = "OOO 'NEW DREAMS STAR'\nИНН: 306547414\nДиректор: Нурбеков У.Ю.\n\n________ (имзо)"

    # QABUL QILISH DALOLATNOMASI (Page 7)
    doc.add_page_break()
    add_para("Қабул қилиш – топшириш далолатномаси", bold=True, align="center", size=14)
    add_para("Барча товарлар сиfat ва яроқлилик муддатига мувофиқдир, ҳеч қандай камчилик мавжуд эмас. Эътирозим йўқ.")
    add_para("\nТоварларни қабул қилдим: _________________ (имзо)")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFEYS ---
st.sidebar.title("🚀 Contract Generator 2026")
menu = st.sidebar.radio("Bo'lim:", ["📝 Shartnoma yaratish", "📊 Statistika"])

if menu == "📝 Shartnoma yaratish":
    st.header("📄 Rasmiy 7 sahifali shartnoma")
    with st.form("main_form"):
        c1, c2 = st.columns(2)
        with c1:
            nomer = st.text_input("Shartnoma №:", "3080")
            sana = st.text_input("Sana:", "27.12.2025")
            ism = st.text_input("F.I.SH:", "URINBAYEV SHOHJAHON SHAROF O’G’LI")
            pas = st.text_input("Pasport №:", "AD6259891")
            pas_sana = st.text_input("Berilgan sana:", "23.02.2024")
        with c2:
            pas_joy = st.text_input("Bergan joy:", "JIZZAX VILOYATI II
