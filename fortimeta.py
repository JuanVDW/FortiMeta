import streamlit as st
import pandas as pd
from jinja2 import Template
import io
import zipfile
import xlrd

st.set_page_config(page_title="FortiMeta", page_icon="logo.png", layout="centered")

col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=120)
with col2:
    st.markdown("<h1 style='margin-top: 7px;margin-left:-20px;'>Generate metadata variables</h1>", unsafe_allow_html=True)

# --- File uploads ---
uploaded_excel = st.file_uploader("🗃️ Upload Excel file", type=["xlsx", "xls"])
uploaded_template = st.file_uploader("📄 Upload Template file", type=["txt"])

mode = st.radio("Generation mode:", ["One file per row", "All in a single file"])

if uploaded_excel and uploaded_template:
    data = pd.read_excel(uploaded_excel)
    template_text = uploaded_template.read().decode("utf-8")
    template = Template(template_text)

    if st.button("🚀 Generate files"):
        if mode == "One file per row":
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for i, row in data.iterrows():
                    context = row.to_dict()
                    output_text = template.render(**context)
                    base_name = str(row[data.columns[0]]).replace(" ", "_")
                    zf.writestr(f"output_{base_name}.txt", output_text)
            zip_buffer.seek(0)
            st.success(f"{len(data)} files generated ✅")
            st.download_button(
                label="📦 Download ZIP",
                data=zip_buffer,
                file_name="outputs.zip",
                mime="application/zip",
            )

        else:
            all_texts = []
            for i, row in data.iterrows():
                context = row.to_dict()
                output_text = template.render(**context)
                all_texts.append(output_text)
            final_text = "\n".join(all_texts)
            st.success("Single file generated ✅")
            st.download_button(
                label="📄 Download file",
                data=final_text,
                file_name="output_single.txt",
                mime="text/plain",
            )
