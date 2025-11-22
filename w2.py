import streamlit as st
import pandas as pd
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# --- STEP 1: City data directly inside code ---


@st.cache_data
def load_monthly_data():
	df_aug = pd.read_csv("august.csv")
	df_sep = pd.read_csv("september.csv")
	df_oct = pd.read_csv("october.csv")
	return df_aug, df_sep, df_oct

df_aug, df_sep, df_oct = load_monthly_data()


# --- STEP 2: Streamlit Dashboard ---
st.title("🏙️ Sucess Story Area Dashboard & PDF Generator")






city_list = sorted(set(df_aug["area"]).union(df_sep["area"]).union(df_oct["area"]))
selected_city = st.selectbox("Select a Area", city_list)
country_name = df_aug.loc[df_aug["area"] == selected_city, "DIV_CODE_x"].values[0]




	











# Fetch data for the selected city from each month
aug_data = df_aug[df_aug["area"] == selected_city].iloc[0]
sep_data = df_sep[df_sep["area"] == selected_city].iloc[0]
oct_data = df_oct[df_oct["area"] == selected_city].iloc[0]

# --- STEP 3: Create comparison table ---
table_data = {
	"Parameter": ["TOTAL_CONSUMER", "TOTAL_BILLABLE", "1PHASE_TOTAL","3PHASE_TOTAL","HT_TOTAL","1PHASE_SM","3PHASE_SM","HT_SM","MOBILE_NO_FEED","TAGGED","TD COUNT","TOTAL_BILLED","MU_BILLED","MRI_BILLED","OCR_BILLED","IDF","RDF","POSITIVE_INF_BILL","NEGATIVE_INF_BILL","BILLED_UNIT","CURRENT_ASSESSMENT","PAID_COUNT","PAID_AMOUNT","ABOVE_10K","REM_NEVER_PAID","REM_LONG_UNPAID","CE%","TURN_UP%"],
	"August": [aug_data["total"], aug_data["billable"], aug_data["1ph_tot"],aug_data["3ph_tot"], aug_data["HT_tot"], aug_data["1ph_sm"],aug_data["3ph_sm"], aug_data["HT_sm"], aug_data["mobile_no"],aug_data["tagged"], aug_data["td_cnt"], aug_data["total_billed"],aug_data["mu_billed"], aug_data["mri_billing"], aug_data["ocr_billing"],aug_data["idf"], aug_data["rdf"], aug_data["pos_inf"],aug_data["neg_inf"], aug_data["CONSUMPTION_CURR_MNTH"], aug_data["CURRENT_ASSESSMENT"], aug_data["turn_up"],aug_data["real"], aug_data["slab_abv_10k"], aug_data["rem_np"],aug_data["rem_luc"],aug_data["ce%"], aug_data["turn_up %"]],
	"September":[sep_data["total"], sep_data["billable"], sep_data["1ph_tot"],sep_data["3ph_tot"], sep_data["HT_tot"], sep_data["1ph_sm"],sep_data["3ph_sm"], sep_data["HT_sm"], sep_data["mobile_no"],sep_data["tagged"], sep_data["td_cnt"], sep_data["total_billed"],sep_data["mu_billed"], sep_data["mri_billing"], sep_data["ocr_billing"],sep_data["idf"], sep_data["rdf"], sep_data["pos_inf"],sep_data["neg_inf"], sep_data["CONSUMPTION_CURR_MNTH"], sep_data["CURRENT_ASSESSMENT"], sep_data["turn_up"],sep_data["real"], sep_data["slab_abv_10k"], sep_data["rem_np"],sep_data["rem_luc"],sep_data["ce%"], sep_data["turn_up %"]],
	"October": [oct_data["total"], oct_data["billable"], oct_data["1ph_tot"],oct_data["3ph_tot"], oct_data["HT_tot"], oct_data["1ph_sm"],oct_data["3ph_sm"], oct_data["HT_sm"], oct_data["mobile_no"],oct_data["tagged"], oct_data["td_cnt"], oct_data["total_billed"],oct_data["mu_billed"], oct_data["mri_billing"], oct_data["ocr_billing"],oct_data["idf"], oct_data["rdf"], oct_data["pos_inf"],oct_data["neg_inf"], oct_data["CONSUMPTION_CURR_MNTH"], oct_data["CURRENT_ASSESSMENT"], oct_data["turn_up"],oct_data["real"], oct_data["slab_abv_10k"], oct_data["rem_np"],oct_data["rem_luc"],oct_data["ce%"], oct_data["turn_up %"]],
}
table_df = pd.DataFrame(table_data)

# Display table nicely

st.markdown(f"<h2 style='font-size:20px;color:#0D47A1;'>📍 {selected_city} — Monthly Overview</h2>", unsafe_allow_html=True)




info_table_data = [
["Zone", aug_data["ZONE"], "Circle", aug_data["CIRCLE"],"Division", aug_data["DIVISION"]],
	

]

info_df = pd.DataFrame(info_table_data)
st.table(info_df)



st.subheader("🔹 Area Details")


st.table(table_df)

# --- STEP 3: PDF Generator ---
def generate_pdf(area_name, aug_data, sep_data, oct_data):
    styles = getSampleStyleSheet()
    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in area_name)
    file_path = os.path.join("city_reports", f"{safe_name}.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    # Header
    elements.append(Paragraph(f"<b>{area_name}</b>", styles["Title"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Info Table
    info_data = [
        ["Zone", aug_data["ZONE"], "Circle", aug_data["CIRCLE"], "Division", aug_data["DIVISION"]],
    ]
    info_table = Table(info_data)
    info_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Data Table
    data = [["Parameter", "August", "September", "October"]]
    for i in range(len(table_df)):
        data.append([
            table_df.iloc[i, 0],
            table_df.iloc[i, 1],
            table_df.iloc[i, 2],
            table_df.iloc[i, 3],
        ])

    t = Table(data)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))
    elements.append(t)

    doc.build(elements)

# --- STEP 5: Auto Generate PDFs for All Areas ---
if st.button("📄 Generate PDFs for All Areas"):
    os.makedirs("city_reports", exist_ok=True)

    # ✅ FIX: Define areas first
    areas = df_aug["area"].unique()

    for area in areas:
        aug = df_aug[df_aug["area"] == area].iloc[0]
        sep = df_sep[df_sep["area"] == area].iloc[0]
        oct_ = df_oct[df_oct["area"] == area].iloc[0]
        generate_pdf(area, aug, sep, oct_)

    st.success("✅ PDFs generated successfully for all areas (portrait mode)!")