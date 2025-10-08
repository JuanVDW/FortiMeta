import streamlit as st
import pandas as pd
from jinja2 import Template
import io
import zipfile
import xlrd

# --- Page setup ---
st.set_page_config(page_title="FortiMeta", page_icon="logo.png", layout="centered")

# --- Header with logo and title ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=120)
with col2:
    st.markdown("<h1 style='margin-top: 7px;margin-left:-20px;'>Generate metadata variables</h1>", unsafe_allow_html=True)

# --- Global style for labels and layout ---
st.markdown("""
    <style>
        .upload-label {
            font-size: 22px !important;
            font-weight: bold !important;
            margin-bottom: -30px !important;
        }
        .section {
            margin-top: 30px;
            margin-bottom: 15px;
        }   
        .separator {
            height: 20px;
            border: none;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# --- Helper function for consistent layout ---
def labeled_section(label, widget_func, *args, **kwargs):
    with st.container():
        st.markdown(f"<p class='upload-label'>{label}</p>", unsafe_allow_html=True)
        return widget_func("", *args, **kwargs)

# --- Section 1: Template upload ---
uploaded_template = labeled_section("📄 Upload Template file", st.file_uploader, type=["txt"])

# --- Separator ---
st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

# --- Section 2: Excel upload ---
uploaded_excel = labeled_section("🗃️ Upload Excel file", st.file_uploader, type=["xlsx", "xls"])

# --- Separator ---
st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

# --- Section 3: Options ---
mode = labeled_section("⚙️ Generation mode", st.radio, options=["One file per row", "All in a single file"])

# --- Separator ---
st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

# --- Section 4: File generation ---
if uploaded_excel and uploaded_template:
    template_text = uploaded_template.read().decode("utf-8")
    template = Template(template_text)
    data = pd.read_excel(uploaded_excel)

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
                file_name="output.txt",
                mime="text/plain",
            )
# --- Section 5: Info ---
else:
    st.info("⬆️ Please upload both the Excel and the Template files to continue.")

# --- README.md ---
with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

# --- Show/Hide Bouton ---
with st.expander("📘 Show/Hide Instructions"):
    st.markdown(readme_content, unsafe_allow_html=True)

