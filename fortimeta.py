import streamlit as st
import pandas as pd
from jinja2 import Template
import io
import zipfile
import xlrd

st.set_page_config(page_title="Générateur Excel → Template", page_icon="🧩", layout="centered")

st.title("🧩 Générateur de fichiers depuis Excel et Template")

# --- Upload des fichiers ---
uploaded_excel = st.file_uploader("📊 Importer le fichier Excel", type=["xlsx", "xls"])
uploaded_template = st.file_uploader("📄 Importer le fichier Template", type=["txt"])

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
                all_texts.append("\n" + "-"*50 + "\n")
            final_text = "\n".join(all_texts)
            st.success("Fichier unique généré ✅")
            st.download_button(
                label="📄 Télécharger le fichier",
                data=final_text,
                file_name="output_unique.txt",
                mime="text/plain",
            )
