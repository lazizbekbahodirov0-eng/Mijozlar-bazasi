import streamlit as st
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- SAHIFANI SOZLASH ---
st.set_page_config(page_title="Rasmiy Shartnoma Generator", layout="wide", page_icon="📄")

# --- LOGIN TIZIMI ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 Tizimga kirish")
    u = st.text_input("Login:")
    p = st.text_input("Parol:", type="password")
    if st.button("Kirish"):
        if u == "admin" and p == "12345":
            st.session_state['logged_in'] = True
            st.rerun()
        else: st.error("Login yoki parol xato!")
    st.stop()

# --- WORD GENERATOR (RAZMERLAR TO'G'IRLANGAN) ---
def create_exact_docx(d):
    doc = Document()
    
    # --- A4 FORMAT VA POLYALARNI SOZLASH ---
    section = doc.sections[0]
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.left_margin = Mm(25)
    section.right_margin = Mm(15)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)

    # Standart shrift sozlamalari
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12) # Razmer 12 qilib kattalashtirildi

    def add_p(text, bold=False, align="justify", size=12):
        p = doc.add_paragraph()
        # Qatorlar orasini ochish (Line spacing)
        p.paragraph_format.line_spacing = 1.15
        # Paragrafdan keyingi bo'shliq
        p.paragraph_format.space_after = Pt(10)
        
        if align == "center": p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else: p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        run = p.add_run(text)
        run.bold = bold
        run.font.size = Pt(size)
        return p

    # --- 1-SAHIFA ---
    add_p("Махсулот қийматини бўлиб тўлаш шарти билан тузилган", True, "center", 14)
    add_p(f"№ {d['nomer']}- сонли олди сотди", True, "center", 13)
    add_p("ШАРТНОМА", True, "center", 16)
    add_p(f"{d['sana']}", True, "center", 12)

    intro = doc.add_paragraph()
    intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    intro.paragraph_format.line_spacing = 1.15
    intro.add_run(f"           Мен  {d['ism']}     Узбекистон  Фукароси,  паспорт № {d['pasport']} {d['pas_sana']}  {d['pas_joy']}   томонидан берилган   {d['manzil']} истиқомат қилувчи, телефон   {d['tel']}“Харидор” бир тарафдан ва OOO \"NEW DREAMS STAR\" номидан Устав асосида фаолият юритувчи ва кейинги ўринларда “Сотувчи” деб номланувчи директор Нурбеков У.Ю. иккинчи тарафдан ушбу шартномани қуйидагилар ҳақида туздик: ").font.size = Pt(12)

    # 1-BANDDAN 4-BANDGACHA
    add_p("1. Шартнома предмети", True, "center")
    add_p("1.1. Ушбу Шартномага асосан “Сотувчи” товарларни “Харидор”нинг эгалигига топшириш, “Харидор” эса ушбу товарларни қабул қилиб олиш ва улар учун белгиланган қийматни бўлиб тўлаш мажбуриятини ўз зиммаларига оладилар. \n1.2. Товарлар харидорга тўлик топширилган вақтдан бошлаб, унинг қиймати тўлиқ тўланишига қадар, сотилган товарлар xaридорнинг қарзини тўлаш мажбуриятини бажаришини таъминлаш учун сотувчи томонидан гаровга олинган деб тан олинади.")

    add_p("2. Шартнома суммаси ва ҳисоб-китоблар тартиби", True, "center")
    add_p(f"2.1. Ушбу Шартноманинг суммаси 1-иловада.\n2.2. Товар “Харидор”га муддатли тўлов шартларида, ушбу Шартномада кўзда тутилган тартибда топширилади. \n2.4. Сўровга асосан товарлар етказиб берилганда, “Харидор” товарларни қабул қилишдан асоссиз бош тортса, ёки Қабул қилиш-топшириш далолатномасига имзо қўйишни рад этса, “Харидор” “Сотувчи” аванс тўловининг 50 % миқдорида жарима тўлайди.")

    add_p("4. Товарларга тўлов киритиш тартиби", True, "center")
    add_p(f"4.1. Товарларга тўлов “Харидор” томонидан, тарафлар томонидан келишилган ва ушбу Шартноманинг ажралмас қисми бўлган 2-иловада белгиланган жадвалга мувофиқ амалга оширилади.\n4.4. Тўланган пул маблағлари, аввало, тўловларни ўз вақтида тўламаaganлик учун жарима тўловига, сўнгра қарздорликни қоплашга йўналтирилади.")

    # --- 2-6 SAHIFALAR (HAMMA BANDLAR TO'LIQ) ---
    doc.add_page_break()
    add_p("5. Сотувчининг назорати", True, "center")
    add_p("5.1. “Харидор” унга нисбатан қўйилган барча даъволар, паспорт маълумотлари, турар жой манзили ўзгариши ҳақида Сотувчини хабардор қилиши шарт.")

    add_p("10. Тарафларнинг масъулияти", True, "center")
    add_p(f"10.5. Тўлов кечиктирилса, ҳар бир кун учун 2,0 % миқдорида жарима ундирилади. 10.8. Агар тўлов бўлмаса, Сотувчи телефонни Идентификатор (Apple ID/Gmail) орқали масофадан туриб қулфлаб қўйиш ҳуқуқига эга.")

    add_p("14. Низоларни хал қилиш", True, "center")
    add_p("14.1. Шартноманинг умумий шартлар бўйича мажбуриятларни бажармаганлик билан боглиқ барча низоларни томонлар музокаралар вақтида хал қилишга ҳаракат қилишади. 14.2. Низолар Фуқаролик ишлари бўйича Сирдарё вилояти туманлараро судларида кўриб чиқилади.")

    add_p("15. Якуний қоидалар", True, "center")
    add_p("15.1. Харидор ўз мажбуриятларини Сотувчининг розилигисиз бошқа шахсга ўтказиши мумкин эмас. 15.7. Ушбу Шартнома 2 нусхада тузилди ва иккаласи ҳам бир хил юридик кучга эга.")

    # --- JADVAL (1-ILOVA) ---
    doc.add_page_break()
    add_p("1-илова\nТовар спецификацияси", True, "center", 14)
    t1 = doc.add_table(rows=1, cols=6, style='Table Grid')
    h1 = ["№", "Махсулот номи", "Улчов", "Микдори", "Нархи", "Суммаси"]
    for i, txt in enumerate(h1): t1.rows[0].cells[i].text = txt
    r1 = t1.add_row().cells
    val = f"{d['summa']} ({d['summa_soz']}) SO’M"
    r1[0].text, r1[1].text, r1[2].text, r1[3].text, r1[4].text, r1[5].text = "1", d['mahsulot'], "дона", "1", val, val

    # --- GRAFIK (2-ILOVA) ---
    doc.add_page_break()
    add_p("2-илова\nТўловлар жадвали", True, "center", 14)
    t2 = doc.add_table(rows=1, cols=3, style='Table Grid')
    h2 = ["Тўлов тури", "Муддати", "Сумма (сўм)"]
    for i, txt in enumerate(h2): t2.rows[0].cells[i].text = txt
    for i in range(1, int(d['oylar']) + 1):
        row = t2.add_row().cells
        row[0].text, row[1].text, row[2].text = f"{i}-тўлов", f"27.{i:02d}.2026 гача", d['oylik']

    # --- IMZOLAR ---
    doc.add_page_break()
    add_p("ТАРАФЛАРНИНГ РЕКВИЗИТЛАРИ", True, "center", 14)
    sig = doc.add_table(rows=2, cols=2)
    sig.rows[0].cells[0].text, sig.rows[0].cells[1].text = "ХАРИДОР", "СОТУВЧИ"
    b = sig.rows[1].cells
    b[0].text = f"Ф.И.Ш: {d['ism']}\nПаспорт №: {d['pasport']}\nМанзил: {d['manzil']}\nТел: {d['tel']}\n\nИмзо: ___________"
    b[1].text = "OOO \"NEW DREAMS STAR\"\nИНН: 306547414\nҲ/р: 20208000305108101001\nДиректор: Нурбеков У.Ю.\n\nИмзо: ___________"

    # --- DALOLATNOMA ---
    doc.add_page_break()
    add_p("Қабул қилиш – топшириш далолатномаси", True, "center", 14)
    add_p("\nБарча товарлар сифат ва яроқлилик муддатига мувофиқдир, ҳеч қандай камчилик мавжуд эмас. Эътирозим йўқ.")
    add_p("\n\nТоварларни қабул қилдим: ______________________ (имзо)")

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- INTERFEYS ---
st.header("📄 Rasmiy Shartnoma Generatori (Standart Razmer)")

with st.form("contract_input_form"):
    col1, col2 = st.columns(2)
    with col1:
        nomer = st.text_input("Shartnoma №:", "3080")
        sana = st.text_input("Sana:", "27.12.2025")
        ism = st.text_input("Харидор Ф.И.Ш:", "URINBAYEV SHOHJAHON SHAROF O’G’LI")
        pas = st.text_input("Pasport №:", "AD6259891")
        p_sana = st.text_input("Berilgan sana:", "23.02.2024Y")
    with col2:
        p_joy = st.text_input("Bergan tashkilot:", "JIZZAX VILOYATI JIZZAX TUMANI IIV")
        manzil = st.text_area("Yashash manzili:", "JIZZAX VILOYATI TOSHLOQ QFY 17-UY")
        tel = st.text_input("Telefonlar:", "90 487 97 77 / 33 016 05 75")
        mahsulot = st.text_input("Mahsulot nomi:", "IPHONE 13 PRO")
        summa = st.text_input("Jami summa (raqamda):", "5 436 000")
        summa_soz = st.text_input("Jami summa (so'zda):", "BESH MILLION TO’RT YUZ O’TIZ OLTI MING")
        oylar = st.number_input("Muddat (oy):", 1, 24, 6)
        oylik = st.text_input("Oylik to'lov:", "906 000")
    
    submitted = st.form_submit_button("Shartnomani tayyorlash")

if submitted:
    data = {'nomer':nomer,'sana':sana,'ism':ism,'pasport':pas,'pas_sana':p_sana,'pas_joy':p_joy,'manzil':manzil,'tel':tel,'mahsulot':mahsulot,'summa':summa,'summa_soz':summa_soz,'oylar':oylar,'oylik':oylik}
    file = create_exact_docx(data)
    st.success("✅ Shartnoma asil nusxadagidek tayyorlandi!")
    st.download_button("📥 WORD FAYLNI YUKLAB OLISH", file, f"Shartnoma_{nomer}.docx")
