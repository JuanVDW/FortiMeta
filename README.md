<div style="display: flex; align-items: center;">
  <img src="logo.png" alt="FortiMeta Logo" width="50">
  <h1 style="margin-left: 15px;">FortiMeta</h1>
</div>



**FortiMeta** is a simple Streamlit web application that automatically generates text files from an Excel sheet and a text template.

---

## 🚀 Features

- 🗃️ Upload an **Excel file** containing variables  
- 📄 Upload a **Template file (.txt)** using `$Variable$` placeholders  
- ⚙️ Choose between:
  - One output file per Excel row
  - A single combined file
- 📦 Download your generated files as a `.zip` or a single `.txt`

---

## 🧠 How It Works

1. **Upload your Excel file**  
   - The first row must contain variable names (e.g. `Name`, `Email`, `Company`).

2. **Upload your Template file**  
   - Example template:
     ```
     Hello $Name$,
     Welcome to $Company$!
     ```

3. **Choose the generation mode**
   - **One file per row** → each Excel row produces one `.txt` output  
   - **All in a single file** → merges all generated texts into one file  

4. **Click “Generate files”**  
   - You’ll get a ZIP archive (if multiple files) or a single `.txt` file to download.

---

## 🧩 Example

**Excel file (example.xlsx):**

| Name  | Company   |
|-------|------------|
| Alice | Fortinet   |
| Bob   | OpenAI     |

**Template (template.txt):**
