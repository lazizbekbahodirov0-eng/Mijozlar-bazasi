import streamlit as st
from docx import Document
from docx.shared import Pt
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
        else: 
            st.error("Login yoki parol xato!")
    st.stop()

# --- WORD GENERATOR (XATOLIKLAR TUZATILGAN) ---
def create_docx(d):
    doc = Document()
    
    # Standart shrift sozlamalari
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)

    # Matn qo'shish funksiyasi (Hamma parametrlar to'g'ri qo'shildi)
    def add_p(text, bold=False, align="justify", size=11):
        p = doc.add_paragraph()
        if align == "center":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        run = p.add_run(text)
        run.bold = bold
        run.font.size = Pt(size)
        return p

    # 1-SAHIFA
    add_p("Махсулот қийматини бўлиб тўлаш шарти билан тузилган", True, "center", 12)
    add_p(f"№ {d['nomer']}- сонли олди сотди", True, "center", 12)
    add_p("ШАРТНОМА", True, "center", 14)
    add_p(f"{d['sana']}", True, "center", 11)

    intro = doc.add_paragraph()
    intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    intro.add_run("Мен ")
    intro.add_run(d['ism']).bold = True
    intro.add_run(f" Узбекистон Фукароси, паспорт № {d['pasport']} {d['pas_sana']} йилда {d['pas_joy']} томонидан берилган, {d['manzil']} манзилда истиқомат қилувчи, телефон {d['tel']} «Харидор» бир тарафдан ва OOO \"NEW DREAMS STAR\" номидан Устав асосида фаолият юритувчи ва кейинги ўринларда “Сотувчи” деб номланувчи директор Нурбеков У.Ю. иккинчи тарафдан ушбу шартномани қуйидагилар ҳақида туздик:")

    # BANDLAR 1-4
    add_p("1. Шартнома предмети", True, "center")
    add_p("1.1. Ушбу Шартномага асосан “Сотувчи” товарларни “Харидор”нинг эгалигига топшириш, “Харидор” эса ушбу товарларни қабул қилиб олиш ва улар учун белгиланган қийматни бўлиб тўлаш мажбуриятини ўз зиммаларига оладилар.")
    add_p("1.2. Товарлар харидорга тўлик топширилган вақтдан бошлаб, унинг қиймати тўлиқ тўланишига қадар, сотилган товарлар харидорнинг қарзини тўлаш мажбуриятини бажаришини таъминлаш учун сотувчи томонидан гаровга олинган деб тан олинади.")

    add_p("2. Шартнома суммаси va ҳисоб-китоблар тартиби", True, "center")
    add_p(f"2.1. Ушбу Шартноманинг суммаси 1-иловада. 2.2. Товар “Харидор”га муддатли тўлов шартларида, ушбу Шартномада кўзда тутилган тартибда топширилади.")
    add_p("2.4. Сўровга асосан товарлар етказиб берилганда, “Харидор” товарларни қабул қилишдан асоссиз бош тортса, аванс тўловининг 50 % миқдорида жарима тўлайди.")

    add_p("4. Товарларга тўлов киритиш тартиби", True, "center")
    add_p(f"4.1. Товарларга тўлов “Харидор” томонидан 2-иловада белгиланган жадвалга мувофиқ амалга оширилади. 4.4. Тўланган пул маблағлари, аввало, тўловларни ўз вақтида тўламаганлик учун жарима тўловига, сўнгра қарздорликни қоплашга йўналтирилади.")

    # 2-SAHIFA
    doc.add_page_break()
    add_p("5. Сотувчининг назорати", True, "center")
    add_p("5.1. “Харидор” унга нисбатан қўйилган барча даъволар, паспорт маълумотларининг ўзгариши, яшаш манзили ўзгариши ҳақида маълумот бериши шарт.")

    add_p("7. Қарзнинг қолган қисмини муддатдан олдин қайтарилиши", True, "center")
    add_p("7.1. Тўлов графиги бузилса ёки Харидорнинг молиявий ҳолати ёмонлашса, Сотувчи қарзни муддатдан олдин тўлиқ қайтаришни талаб қилишга ҳақli.")
    add_p("7.2. Бу ҳолда Харидор 3 (уч) календар куни ичида тўловни амалга ошириши лозим.")

    # 3-SAHIFA
    doc.add_page_break()
    add_p("10. Тарафларнинг масъулияти", True, "center")
    add_p(f"10.5. Тўлов муддатлари ўтганидан сўнг, “Харидор”дан кечиктирилган ҳар бир кун учун тўланмаган суммадан 2,0 % миқдорида жарима ундирилади.")
    add_p("10.8. Агар “Харидор” тўловни амалга оширмаса, “Сотувчи” масофадан туриб уяли алоқа воситасини Идентификатор (Apple ID/Gmail) орқали қулфлаб қўйиш ҳуқуқига эга.")

    # 4-SAHIFA: 1-ILOVA
    doc.add_page_break()
    add_p("1-илова\nТовар спецификацияси", True, "center", 12)
    t1 = doc.add_table(rows=2, cols=4, style='Table Grid')
    h = t1.rows[0].cells
    h[0].text, h[1].text, h[2].text, h[3].text = "Махсулот", "Микдор", "Нарх", "Сумма"
    r = t1.rows[1].cells
    r[0].text, r[1].text, r[2].text, r[3].text = d['mahsulot'], "1", d['summa'], d['summa']
    add_p(f"\nЖАМИ: {d['summa']} ({d['summa_soz']}) сўм.", True)

    # 5-SAHIFA: 2-ILOVA
    doc.add_page_break()
    add_p("2-илова\nТўловлар жадвали", True, "center", 12)
    t2 = doc.add_table(rows=1, cols=3, style='Table Grid')
    h2 = t2.rows[0].cells
    h2[0].text, h2[1].text, h2[2].text = "Тўлов тури", "Муддати", "Сумма (сўм)"
    for i in range(1, int(d['oylar']) + 1):
        row = t2.add_row().cells
        row[0].text, row[1].text, row[2].text = f"{i}-тўлов", f"27.{i:02d}.2026 гача", d['oylik']

    # 6-SAHIFA: REKVIZITLAR
    doc.add_page_break()
    add_p("ТАРАФЛАРНИНГ РЕКВИЗИТЛАРИ", True, "center")
    st_table = doc.add_table(rows=2, cols=2)
    st_table.rows[0].cells[0].text, st_table.rows[0].cells[1].text = "ХАРИДОР", "СОТУВЧИ"
    b_r = st_table.rows[1].cells
    b_r[0].text = f"{d['ism']}\nПаспорт: {d['pasport']}\nТел: {d['tel']}\nМанзил: {d['manzil']}\n\n________ (имзо)"
    b_r[1].text = "OOO 'NEW DREAMS STAR'\nИНН: 306547414\nДиректор: Нурбеков У.Ю.\n\n________ (имзо)"

    # 7-SAHIFA: DALOLATNOMA
    doc.add_page_break()
    add_p("Қабул қилиш – топшириш далолатномаси", True, "center", 14)
    add_p("\nБарча товарлар сифат ва яроқлилик муддатига мувофиқдир, ҳеч қандай камчилик мавжуд эмас. Эътирозим йўқ.")
    add_p("\n\nХаридор: _________________ (имзо)")

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- INTERFEYS ---
st.header("📑 Rasmiy Shartnoma Generatori")
with st.form("shablon_form"):
    col1, col2 = st.columns(2)
    with col1:
        nomer = st.text_input("Shartnoma №:", "3080")
        sana = st.text_input("Sana:", "27.12.2025")
        ism = st.text_input("F.I.SH:", "URINBAYEV SHOHJAHON SHAROF O’G’LI")
        pas = st.text_input("Pasport №:", "AD6259891")
        p_sana = st.text_input("Berilgan sana:", "23.02.2024")
    with col2:
        p_joy = st.text_input("Kim tomonidan berilgan:", "JIZZAX VILOYATI IIV")
        manzil = st.text_area("Manzil:", "JIZZAX VILOYATI TOSHLOQ QFY")
        tel = st.text_input("Tel:", "90 487 97 77")
        mahsulot = st.text_input("Mahsulot:", "IPHONE 13 PRO")
        summa = st.text_input("Summa:", "5 436 000")
        summa_soz = st.text_input("Summa so'zda:", "BESH MILLION TO’RT YUZ O’TIZ OLTI MING")
        oylar = st.number_input("Muddat (oy):", 1, 24, 6)
        oylik = st.text_input("Oylik to'lov:", "906 000")
    submitted = st.form_submit_button("Shartnomani tayyorlash")

if submitted:
    data = {'nomer':nomer,'sana':sana,'ism':ism,'pasport':pas,'pas_sana':p_sana,'pas_joy':p_joy,'manzil':manzil,'tel':tel,'mahsulot':mahsulot,'summa':summa,'summa_soz':summa_soz,'oylar':oylar,'oylik':oylik}
    file = create_docx(data)
    st.success("✅ Tayyor!")
    st.download_button("📥 WORD FAYLNI YUKLAB OLISH", file, f"Shartnoma_{nomer}.docx")
