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
   - The first row must contain variable names (e.g. `hostname`, `vdom`, `siteID`).

2. **Upload your Template file**  
   - Example template:
     ```
edit siteID
  config dynamic_mapping
    edit "{{hostname}}"-"{{vdom}}"
      set value {{siteID}}
    next
  end
next
     ```

3. **Choose the generation mode**
   - **One file per row** → each Excel row produces one `.txt` output  
   - **All in a single file** → merges all generated texts into one file  

4. **Click “Generate files”**  
   - You’ll get a ZIP archive (if multiple files) or a single `.txt` file to download.

---

## 🧩 Example

**Excel file (example.xlsx):**

| hostname           | vdom   | deviceLicense| siteID | posACsubnet | routerID      |
|--------------------|--------|--------------|--------|-------------|---------------|
| mult03-hassel      | global | Care         | 688    | 10.6.88     | 1.10.97.116   |
| mult03-heiodb003   | global | Care         | 613    | 10.6.13     | 1.10.97.114   |
| mult03-ieper       | global | Care         | 696    | 10.6.96     | 1.10.97.118   |
| mult03-kastrl      | global | Care         | 676    | 10.6.76     | 1.10.97.115   |
| mult03-koerse      | global | Care         | 602    | 10.6.2      | 1.10.97.111   |
| mult03-leuven002   | global | Care         | 638    | 10.6.38     | 1.10.97.108   |
| mult03-lier003     | global | Care         | 662    | 10.6.62     | 1.10.97.105   |
| mult03-mol         | global | Care         | 668    | 10.6.68     | 1.10.97.107   |

**Template (template.txt):**
```text
config fmg variable
  edit hostname
    config dynamic_mapping
      edit "{{hostname}}"-"{{vdom}}"
        set value {{hostname}}
      next
    end
  next
  edit deviceLicense
    config dynamic_mapping
      edit "{{hostname}}"-"{{vdom}}"
        set value {{deviceLicense}}
      next
    end
  next
  edit siteID
    config dynamic_mapping
      edit "{{hostname}}"-"{{vdom}}"
        set value {{siteID}}
      next
    end
  next
  edit posACsubnet
    config dynamic_mapping
      edit "{{hostname}}"-"{{vdom}}"
        set value {{posACsubnet}}
      next
    end
  next
  edit routerID
    config dynamic_mapping
      edit "{{hostname}}"-"{{vdom}}"
        set value {{routerID}}
      next
    end
  next
end
```
---

## 🧑‍💻 Author

Developed by Juan Van de Walle  
📅 Version 1.0 — 2025  
💡 Built with Streamlit

