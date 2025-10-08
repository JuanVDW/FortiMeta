import streamlit as st
import pandas as pd
from jinja2 import Template
import io
import zipfile

# --- Page setup ---
st.set_page_config(page_title="FortiMeta", page_icon="logo.png", layout="centered")

# --- Header with logo and title ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=120)
with col2:
    st.markdown(
        "<h1 style='margin-top: 7px;margin-left:-20px;'>Generate metadata variables</h1>",
        unsafe_allow_html=True
    )

# --- Global style for labels and layout ---
st.markdown("""
    <style>
        .upload-label {
            font-size: 22px !important;
            font-weight: bold !important;
            margin-bottom: -30px !important;
        }
        .section {
            background-color: #f7f7f7;
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
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
    """Render a gray-background section with a label and widget"""
    with st.container():
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown(f"<p class='upload-label'>{label}</p>", unsafe_allow_html=True)
        value = widget_func("", *args, **kwargs)
        st.markdown("</div>", unsafe_allow_html=True)
        return value

# --- README Section (Show/Hide) ---
try:
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()
    with st.expander("📘 Show/Hide Instructions / README"):
        st.markdown(readme_content, unsafe_allow_html=True)
except FileNotFoundError:
    st.info("README.md not found. Instructions will appear here once available.")

# --- Template upload ---
uploaded_template = labeled_section("📄 Upload Template file", st.file_uploader, type=["txt"])

# --- Excel/CSV upload ---
uploaded_excel = labeled_section("🗃️ Upload Excel/CSV file", st.file_uploader, type=["xlsx", "xls", "csv"])

# --- Mode selection ---
mode = labeled_section("⚙️ Generation mode", st.radio, options=["One file per row", "All in a single file"])

# --- File generation ---
if uploaded_excel and uploaded_template:
    template_text = uploaded_template.read().decode("utf-8")
    template = Template(template_text)
    file_name = uploaded_excel.name.lower()
    
    try:
        if file_name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_excel, engine="openpyxl")
        elif file_name.endswith(".xls"):
            data = pd.read_excel(uploaded_excel, engine="xlrd")  # xlrd<2.0
        elif file_name.endswith(".csv"):
            data = pd.read_csv(uploaded_excel)
        else:
            st.error("Unsupported file format")
            st.stop()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()
    
    # --- Generate button in stylized section ---
    def generate_button(label):
        return st.button(label)
    
    generate_clicked = labeled_section("🚀 Generate files", generate_button, "Generate files")
    
    if generate_clicked:
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
else:
    st.info("⬆️ Please upload both the Excel/CSV and the Template files to continue.")
