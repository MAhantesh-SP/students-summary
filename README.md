<div align="center">

<img src="https://materials.iisc.ac.in/assets/images/IISclogo.png" alt="IISc Logo" width="100"/>

# 🎓 Student Summary Dashboard

### A unified, interactive analytics platform for student data across UG, PG & PhD programmes

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://students-summary.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Repo Size](https://img.shields.io/github/repo-size/MAhantesh-SP/students-summary)](https://github.com/MAhantesh-SP/students-summary)

---

**[🚀 Live Demo](https://students-summary.streamlit.app/)** &nbsp;·&nbsp; **[📂 Repository](https://github.com/MAhantesh-SP/students-summary)** &nbsp;·&nbsp; **[🐛 Report Bug](https://github.com/MAhantesh-SP/students-summary/issues)** &nbsp;·&nbsp; **[✨ Request Feature](https://github.com/MAhantesh-SP/students-summary/issues)**

</div>

---

## Overview

**Student Summary Dashboard** is a powerful Streamlit web application that consolidates student data analytics for **Undergraduate (UG)**, **Postgraduate 2-Year (PG)**, **Postgraduate 3-Year / M.Tech (Res)**, and **PhD** programmes into a single, clean interface.

Upload your Active Students Excel file and instantly get:
- Per-programme student headcounts
- Gender, domicile & nationality breakdowns
- Social category analysis (SC / ST / OBC / EWS)
- Interactive charts and downloadable Excel/CSV reports

No more running four separate Python scripts — everything is one click away.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **File Upload** | Upload any `.xlsx` with the standard column format |
| 🎓 **4 Programme Types** | UG, PG 2-Year, PG 3-Year (M.Tech Res), PhD |
| 📅 **Dynamic Year Range** | Adjust batch year filter on-the-fly from the sidebar |
| 📊 **Degree Counts** | Full table of students per programme with totals |
| 📋 **Summary Metrics** | Gender, domicile, nationality & social category stats |
| 📈 **Interactive Charts** | Bar charts, pie charts (Plotly), and batch-year trends |
| 🔍 **Search & Filter** | Live search + column selector in the filtered-data view |
| ⬇️ **Export** | Download full Excel report (3 sheets) or individual CSVs |
| 🖥️ **Responsive UI** | Works on desktop, tablet, and mobile |

---

## 🗂️ Project Structure

```
students-summary/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
└── assets/                 # Screenshots / static assets (optional)
```

---

## 📊 Programme Configurations

Each programme type has a predefined list of degree names and a default batch year range:

| Programme | Default Year Range | No. of Degrees |
|---|:---:|:---:|
| UG / Integrated | 2020 – 2024 | 4 |
| PG 2-Year (M.Tech / M.Sc / M.Des) | 2023 – 2024 | 34 |
| PG 3-Year / M.Tech (Res) | 2016 – 2024 | 18 |
| PhD / Int. PhD | 2012 – 2024 | 45 |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/MAhantesh-SP/students-summary.git
cd students-summary

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 📋 Input File Format

Upload an `.xlsx` file with the following column headers *(extra columns are ignored)*:

| Column | Description |
|---|---|
| `Student Batch` | Admission year, e.g. `2023` |
| `Program Name` | Full programme name |
| `Gender` | `Male` / `Female` / Other |
| `Nationality` | e.g. `Indian`, `Foreign` |
| `Domicile State` | e.g. `Karnataka` |
| `Social Category` | `SC`, `ST`, `OBC-NCL`, `OBC-CL`, `EWS`, etc. |

> **Tip:** Column names are matched case-insensitively and tolerate extra whitespace, so minor formatting differences in the header row are handled automatically.

---

## 📤 Output / Export

After running an analysis, you can download:

- **Full Excel Report** (`.xlsx`) — contains three sheets:
  - `DegreeCounts_<programme>_<year_from>_<year_to>`
  - `FilteredRows_<programme>_<year_from>_<year_to>`
  - `Summary_<programme>_<year_from>_<year_to>`
- **Degree Counts CSV**
- **Summary Metrics CSV**

---

## 🛠️ Built With

- [**Streamlit**](https://streamlit.io/) — Web app framework
- [**Pandas**](https://pandas.pydata.org/) — Data processing
- [**Plotly**](https://plotly.com/python/) — Interactive visualisations
- [**OpenPyXL**](https://openpyxl.readthedocs.io/) — Excel read/write

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please open an issue first for major changes to discuss what you'd like to change.

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

---

## 👤 Author

**Mahantesh S P**

[![GitHub](https://img.shields.io/badge/GitHub-MAhantesh--SP-181717?logo=github)](https://github.com/MAhantesh-SP)

---

<div align="center">

Made with ❤️ · If this project helped you, please consider giving it a ⭐

</div>
