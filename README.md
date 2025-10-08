# FortiMeta

**FortiMeta** is a simple Streamlit web application that automatically generates text files from a text template and an Excel sheet.

---

## 🚀 Features

- 📄 Upload a **Template file (.txt)** using `{{Variable}}` placeholders
- 🗃️ Upload an **Excel file** containing variables  
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
   ```text
   to configure metadata
     edit "{{hostname}}"-"global"
       set {{siteID}}
       set {{subnet}}.0/24
     next
   end
```
---

## 🧑‍💻 Author

Developed by Juan Van de Walle  
📅 Version 1.0 — 2025  
💡 Built with Streamlit

