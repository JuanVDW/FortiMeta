import streamlit as st
import pandas as pd
from jinja2 import Template
import io
import zipfile
import xlrd

st.set_page_config(page_title="FortiMeta", page_icon="logo.png", layout="centered")

import streamlit as st

col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=60)
with col2:
    st.markdown("<h1 style='padding-top: 10px;'>FortiMeta</h1>", unsafe_allow_html=True)

st.title("❇️ Generate metadata variables")

# --- Files upload ---
uploaded_excel = st.file_uploader("🗃️ Import the Excel file", type=["xlsx", "xls"])
uploaded_template = st.file_uploader("📄 Import the Template file", type=["txt"])

mode = st.radio("Mode de génération :", ["Un fichier par ligne", "Tout dans un seul fichier"])

if uploaded_excel and uploaded_template:
    data = pd.read_excel(uploaded_excel)
    template_text = uploaded_template.read().decode("utf-8")
    template = Template(template_text)

    if st.button("🚀 Générer les fichiers"):
        if mode == "Un fichier par ligne":
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for i, row in data.iterrows():
                    context = row.to_dict()
                    output_text = template.render(**context)
                    base_name = str(row[data.columns[0]]).replace(" ", "_")
                    zf.writestr(f"output_{base_name}.txt", output_text)
            zip_buffer.seek(0)
            st.success(f"{len(data)} fichiers générés ✅")
            st.download_button(
                label="📦 Télécharger le ZIP",
                data=zip_buffer,
                file_name="sorties.zip",
                mime="application/zip",
            )

        else:
            all_texts = []
            for i, row in data.iterrows():
                context = row.to_dict()
                output_text = template.render(**context)
                all_texts.append(output_text)
            final_text = "\n".join(all_texts)
            st.success("Fichier unique généré ✅")
            st.download_button(
                label="📄 Télécharger le fichier",
                data=final_text,
                file_name="output_unique.txt",
                mime="text/plain",
            )
