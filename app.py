import streamlit as st
import pandas as pd
import re
import io
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Student Data Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { margin: 0; font-size: 2.2rem; font-weight: 700; }
    .main-header p  { margin: 0.4rem 0 0; opacity: 0.85; font-size: 1rem; }
    .metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.07);
    }
    .metric-card .val  { font-size: 2rem; font-weight: 700; color: #1a237e; }
    .metric-card .lbl  { font-size: 0.85rem; color: #666; margin-top: 4px; }
    .section-header {
        background: #f5f5f5;
        border-left: 4px solid #3949ab;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        margin: 1rem 0 0.5rem;
        font-weight: 600;
        color: #1a237e;
    }
    .stTabs [data-baseweb="tab"] { font-size: 0.95rem; font-weight: 600; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .download-btn { margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ─── Degree lists per programme ──────────────────────────────────────────────
CONFIGS = {
    "UG / Integrated": {
        "year_from": 2020, "year_to": 2024,
        "degrees": [
            "Master of Science",
            "Bachelor of Science (Res)",
            "B.Tech (Mathematics and Computing)",
            "Bachelor of Science (Res)_2022",
        ]
    },
    "PG 2-Year": {
        "year_from": 2023, "year_to": 2024,
        "degrees": [
            "M.Sc in Chemical Sciences",
            "M.Sc in Life Sciences_2023",
            "M.Tech in Quantum Technology_23",
            "M.Tech in Electronics & Communication_21",
            "M.Tech in Artificial Intelligence_23",
            "Masters in Management_22",
            "M.Tech in Inst and App Phy_24",
            "MTech in Robotics and Autonomous Syst_24",
            "M.Tech in Civil Engg_24",
            "M.Tech in Electrical Engg_2024",
            "M.Tech in Electronic Systems Engg_2020",
            "M.Tech in Electronic Product Design",
            "M.Tech in Climate and Earth Sciences",
            "M.Tech in Smart Manufacturing_2023",
            "M.Tech in Microelectronics & VLSI Design",
            "M.Tech in Materials Engg_22",
            "M Des in Prod Des, Develop and Managment",
            "M.Tech in Mechanical Engg_2020",
            "M.Tech in Sustainable Technologies",
            "M.Tech in Comp Sc Engg",
            "M.Tech in Chemical Engg",
            "M.Tech in Semiconductor Technology_24",
            "M.Tech in Signal Processing_2022",
            "Master of Technology in Bioengineering",
            "M.Tech in Aerospace Engineering_24",
            "M.Tech in Comp and Data Sc_2022",
            "M.Tech in Semiconductor Technology",
            "M.Tech in Civil Engg_21",
            "M.Tech in Electrical Engg_2020",
            "M.Tech in Mobility Engineering",
            "MTech in Robotics and Autonomous Systems",
            "M Des in Prod Des and Engg_2021",
            "M.Tech in Inst and App Phy",
            "M.Tech in Aerospace Engineering",
        ]
    },
    "PG 3-Year (M.Tech Res)": {
        "year_from": 2016, "year_to": 2024,
        "degrees": [
            "M.Tech (Res) in Materials Engg",
            "M.Tech (Res) in Electrical Engg",
            "M.Tech (Res) in Electronic Systems Engg",
            "M.Tech (Res) in Comp Sc Engg",
            "M.Tech (Res) ER",
            "M.Tech (Res) in Earth Sciences",
            "M.Tech Res in Cyber Physical System",
            "M.Tech (Res) in Comp and Data Sc",
            "M.Tech (Res) in Civil Engg",
            "M.Tech (Res) in Aerospace Engineering",
            "M.Tech (Res) in Mechanical Engg",
            "M.Tech (Res) in Inst and App Phy",
            "M.Tech (Res) in Sustainable Technologies",
            "M.Tech (Res) in Chemical Engg",
            "M.Tech (Res) in Prod Des and Manf_19",
            "M.Tech (Res) AOS",
            "M.Tech (Res) in Elec Comm Engg",
            "M.Tech (Res) in Prod Des and Engg",
        ]
    },
    "PhD": {
        "year_from": 2012, "year_to": 2024,
        "degrees": [
            "Ph.D. (Engg) in Materials Engg",
            "Ph.D. (Sc) in High Energy Physics_23",
            "Ph.D. (Sc) in Neuroscience",
            "Ph.D. (Engg) in Cyber Phy Sys",
            "Ph.D. (Engg) in Comp Sc Engg",
            "Ph.D. (Engg) in Brain, Computation, and",
            "Ph.D. (Engg) in Comp and Data Sc",
            "Ph.D. (Engg) in Energy",
            "Ph.D. (Engg) in Nanoscience and Engg",
            "Ph.D. (Engg) in Mechanical Engg",
            "Ph.D. (Engg) in Inst and App Phy",
            "Ph.D. (Engg) in Electrical Engg",
            "Ph.D. (Sc) in Physics",
            "Ph.D. (Engg) in  Elec Comm Engg",
            "Ph.D. (Sc) in Solid State and Struc Chem",
            "Ph.D. (Sc) in Materials Research",
            "Ph.D. (Engg) in Electronic Systems Engg",
            "Ph.D. (Sc) in Inorganic and Phy Chem",
            "Ph.D. (Engg) in Aerospace Engineering",
            "Ph.D. (Engg) in Earth Sciences",
            "Ph.D. (Engg) in Chemical Engg",
            "Ph.D. (Sc) in Organic Chemistry",
            "PhD (Sc) in Developmental Biology and Ge",
            "Ph.D. (Engg) in Prod Des and Engg",
            "Ph.D. (Engg) in Civil Engineering",
            "Ph.D. (Engg) in Management",
            "Int. Ph.D. in Mathematical Sc",
            "Int. Ph.D. in Biological Sc",
            "Int. Ph.D. in Physical Sciences",
            "Ph.D. (Engg) in Bioengineering",
            "Ph.D. (Sc) in Microbiology and Cell Bio",
            "Ph.D. (Sc) in Biochemistry",
            "Ph.D. (Sc) in Ecological Sc",
            "Ph.D. (Engg) in Water Research",
            "Ph.D. (Engg) in Atmospheric and Oc Sc",
            "Ph.D. (Engg) in Sustainable Technologies",
            "Ph.D. (Engg) in Mathematics Initiative",
            "Ph.D. (Sc) in Molecular Biophysics",
            "Ph.D. (Engg) in Climate Change",
            "Int. Ph.D. in Chemical Sciences",
            "Ph.D. (Sc) in Astronomy and Astrophysics",
            "Ph.D. (Engg) in Prod Des and Manf_19",
            "Ph.D. (Sc) in Mathematics",
            "Ph.D. (Sc) in High Energy Physics",
            "Ph.D. (Sc) in Mathematics Initiative",
        ]
    },
}

# ─── Helper functions (shared logic from original scripts) ────────────────────
def normalize_text(s):
    if pd.isna(s): return ""
    s = str(s).replace("\xa0", " ")
    return re.sub(r"\s+", " ", s.strip()).lower()

def find_col(df, key):
    key_norm = re.sub(r'[\s_]+', '', key.lower())
    for col in df.columns:
        if key_norm in re.sub(r'[\s_]+', '', col.lower()):
            return col
    return None

def extract_year(value):
    if pd.isna(value): return None
    m = re.search(r'\b(19|20)\d{2}\b', str(value))
    return int(m.group(0)) if m else None

def program_mask(series, allowed_labels):
    allowed_norm = {normalize_text(x) for x in allowed_labels}
    return series.apply(lambda x: normalize_text(x) in allowed_norm)

def compute_degree_counts(df_deg, program_col, allowed_degrees):
    norm_to_canon = {normalize_text(k): k for k in allowed_degrees}
    canon_series = df_deg[program_col].apply(
        lambda x: norm_to_canon.get(normalize_text(x), "Other/Unmapped")
    )
    counts = canon_series.value_counts(dropna=False).rename_axis("Program Name").reset_index(name="Count")
    for lab in allowed_degrees:
        if lab not in set(counts["Program Name"]):
            counts.loc[len(counts)] = [lab, 0]
    counts = counts[counts["Program Name"].isin(allowed_degrees)]
    counts["Program Name"] = pd.Categorical(counts["Program Name"], categories=allowed_degrees, ordered=True)
    counts = counts.sort_values("Program Name").reset_index(drop=True)
    counts.loc[len(counts)] = ["Total (selected degrees)", counts["Count"].sum()]
    return counts

def build_summary_metrics(df_deg):
    gender_col = find_col(df_deg, "Gender")
    dom_col    = find_col(df_deg, "Domicile State")
    nat_col    = find_col(df_deg, "Nationality")
    social_col = find_col(df_deg, "Social Category")

    male   = (df_deg[gender_col] == "Male").sum()   if gender_col else 0
    female = (df_deg[gender_col] == "Female").sum() if gender_col else 0
    other  = (~df_deg[gender_col].isin(["Male","Female"])).sum() if gender_col else 0
    total  = len(df_deg)

    if nat_col:
        nat_series  = df_deg[nat_col].astype(str).str.strip().str.lower()
        indian_only = nat_series.eq("indian")
    else:
        indian_only = pd.Series([False]*len(df_deg), index=df_deg.index)

    within_state  = ((df_deg[dom_col] == "Karnataka") & indian_only).sum() if dom_col else 0
    outside_state = ((df_deg[dom_col] != "Karnataka") & indian_only).sum() if dom_col else 0
    outside_country = (~indian_only).sum() if nat_col else 0

    if social_col:
        eco_backward = df_deg[social_col].astype(str).str.contains(r"(economically|ews)", case=False, na=False).sum()
        soc_challenged = df_deg[social_col].isin(["SC","ST","OBC-NCL","OBC-CL"]).sum()
    else:
        eco_backward = soc_challenged = 0

    return pd.DataFrame({
        "Metric": [
            "No. of Male students", "No. of Female students", "No. of Other students", "Total students",
            "Within State (Karnataka) [Indian only]", "Outside State (Except Karnataka) [Indian only]",
            "Outside Country (Except India)", "Economically Backward",
            "Socially Challenged (SC+ST+OBC)",
            "Receiving fee reimbursement from State/Central",
            "Receiving fee reimbursement from Institute Funds",
            "Receiving fee reimbursement from Private Bodies",
            "Not receiving reimbursement",
        ],
        "Count": [
            male, female, other, total,
            within_state, outside_state, outside_country,
            eco_backward, soc_challenged,
            0, 0, soc_challenged, eco_backward,
        ]
    })

def run_analysis(df, cfg, year_from, year_to):
    batch_col   = find_col(df, "Student Batch")
    program_col = find_col(df, "Program Name")
    if not batch_col or not program_col:
        return None, None, None, "Required columns not found."

    years = df[batch_col].apply(extract_year)
    df_year = df[years.between(year_from, year_to, inclusive="both")].copy()
    if df_year.empty:
        return None, None, None, f"No rows for batch years {year_from}–{year_to}."

    mask = program_mask(df_year[program_col], cfg["degrees"])
    df_deg = df_year[mask].copy()
    if df_deg.empty:
        return None, None, df_year, f"No rows matched the selected programs."

    counts  = compute_degree_counts(df_deg, program_col, cfg["degrees"])
    summary = build_summary_metrics(df_deg)
    return counts, summary, df_deg, None

def to_excel_bytes(counts_df, rows_df, summary_df, label):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        counts_df.to_excel(writer,  sheet_name=f"DegreeCounts_{label}",  index=False)
        rows_df.to_excel(writer,    sheet_name=f"FilteredRows_{label}",   index=False)
        summary_df.to_excel(writer, sheet_name=f"Summary_{label}",        index=False)
    return buf.getvalue()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://materials.iisc.ac.in/assets/images/IISclogo.png", width=80)
    st.markdown("## 🎓 Student Analyzer")
    st.markdown("---")
    uploaded = st.file_uploader(
        "📂 Upload Student Data (.xlsx)",
        type=["xlsx"],
        help="Upload the active-students Excel file. Column headers must match the expected format."
    )
    st.markdown("---")
    st.markdown("**Programme Type**")
    prog_choice = st.radio("", list(CONFIGS.keys()), label_visibility="collapsed")
    st.markdown("---")

    cfg = CONFIGS[prog_choice]
    st.markdown("**Year Range**")
    col1, col2 = st.columns(2)
    year_from = col1.number_input("From", min_value=2000, max_value=2030, value=cfg["year_from"])
    year_to   = col2.number_input("To",   min_value=2000, max_value=2030, value=cfg["year_to"])
    run_btn = st.button("▶ Run Analysis", use_container_width=True, type="primary")
    st.markdown("---")
    st.caption("Built with Streamlit · All 4 scripts unified")

# ─── Main area ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🎓 Student Data Dashboard</h1>
  <p>Upload your Active Students Excel file and analyse by programme type, year range, gender, domicile & social category.</p>
</div>
""", unsafe_allow_html=True)

if uploaded is None:
    st.info("👈 Upload an Excel file from the sidebar to get started.")
    st.markdown("### What this app does")
    cols = st.columns(4)
    for col, (name, c) in zip(cols, CONFIGS.items()):
        col.markdown(f"""
        <div class="metric-card">
          <div class="val">{len(c['degrees'])}</div>
          <div class="lbl">{name}<br>programmes</div>
        </div>""", unsafe_allow_html=True)
    st.stop()

# ─── Load data ────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Reading Excel file…")
def load_data(file_bytes):
    df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
    df.columns = df.columns.str.strip().str.replace('\xa0', ' ', regex=True)
    return df

df = load_data(uploaded.read())

st.success(f"✅ File loaded: **{uploaded.name}** — {len(df):,} rows × {len(df.columns)} columns")

# Quick file overview
with st.expander("📋 File Preview (first 5 rows)"):
    st.dataframe(df.head(5), use_container_width=True)
    st.caption(f"Columns: {', '.join(df.columns)}")

# ─── Run analysis when button clicked ────────────────────────────────────────
if run_btn or "last_result" in st.session_state:
    if run_btn:
        counts, summary, df_filtered, err = run_analysis(df, cfg, year_from, year_to)
        st.session_state["last_result"] = (counts, summary, df_filtered, err, prog_choice, year_from, year_to)
    else:
        counts, summary, df_filtered, err, prog_choice, year_from, year_to = st.session_state["last_result"]

    if err:
        st.error(f"⚠️ {err}")
    else:
        label = prog_choice.replace(" ", "_").replace("/", "-")

        # ── Top-level metrics ────────────────────────────────────────────────
        total = int(summary.loc[summary["Metric"] == "Total students", "Count"].values[0])
        male  = int(summary.loc[summary["Metric"] == "No. of Male students", "Count"].values[0])
        female= int(summary.loc[summary["Metric"] == "No. of Female students", "Count"].values[0])
        outside_country = int(summary.loc[summary["Metric"] == "Outside Country (Except India)", "Count"].values[0])
        soc_chal = int(summary.loc[summary["Metric"] == "Socially Challenged (SC+ST+OBC)", "Count"].values[0])

        c1, c2, c3, c4, c5 = st.columns(5)
        for col, val, lbl in zip(
            [c1,c2,c3,c4,c5],
            [total, male, female, outside_country, soc_chal],
            ["Total Students","Male","Female","International","SC/ST/OBC"]
        ):
            col.markdown(f"""
            <div class="metric-card">
              <div class="val">{val}</div>
              <div class="lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Tabs ─────────────────────────────────────────────────────────────
        t1, t2, t3, t4, t5 = st.tabs([
            "📊 Degree Counts", "📋 Summary Metrics",
            "📈 Charts", "🗂️ Filtered Data", "⬇️ Export"
        ])

        # Tab 1 – Degree counts
        with t1:
            st.markdown(f'<div class="section-header">Programme: {prog_choice} · Batch {year_from}–{year_to}</div>', unsafe_allow_html=True)
            display_counts = counts[counts["Program Name"] != "Total (selected degrees)"].copy()
            display_counts = display_counts[display_counts["Count"] > 0]
            st.dataframe(counts, use_container_width=True, height=600)

        # Tab 2 – Summary
        with t2:
            st.markdown(f'<div class="section-header">Summary Metrics · {prog_choice}</div>', unsafe_allow_html=True)
            col_a, col_b = st.columns([1.2, 1])
            with col_a:
                st.dataframe(summary, use_container_width=True)
            with col_b:
                gender_data = summary[summary["Metric"].isin(["No. of Male students","No. of Female students","No. of Other students"])]
                fig_g = px.pie(
                    gender_data, values="Count", names="Metric",
                    title="Gender Distribution",
                    color_discrete_sequence=["#1a237e","#e91e63","#43a047"],
                    hole=0.4
                )
                fig_g.update_layout(margin=dict(t=40,b=0,l=0,r=0), height=280)
                st.plotly_chart(fig_g, use_container_width=True)

        # Tab 3 – Charts
        with t3:
            chart_data = counts[counts["Program Name"] != "Total (selected degrees)"].copy()
            chart_data = chart_data[chart_data["Count"] > 0].sort_values("Count", ascending=True)

            fig_bar = px.bar(
                chart_data, x="Count", y="Program Name", orientation="h",
                title=f"Students per Programme — {prog_choice} ({year_from}–{year_to})",
                color="Count", color_continuous_scale="Blues",
                text="Count"
            )
            fig_bar.update_traces(textposition="outside")
            fig_bar.update_layout(
                height=max(400, len(chart_data)*28 + 100),
                showlegend=False,
                coloraxis_showscale=False,
                yaxis_title="", xaxis_title="Number of Students",
                margin=dict(l=10, r=40, t=50, b=40)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            # Domicile breakdown
            st.markdown("#### Domicile & Nationality")
            dom_metrics = ["Within State (Karnataka) [Indian only]",
                           "Outside State (Except Karnataka) [Indian only]",
                           "Outside Country (Except India)"]
            dom_data = summary[summary["Metric"].isin(dom_metrics)].copy()
            dom_data["Metric"] = dom_data["Metric"].str.replace(" \[Indian only\]", "", regex=True)
            fig_dom = px.pie(
                dom_data, values="Count", names="Metric",
                color_discrete_sequence=["#1565c0","#42a5f5","#90caf9"],
                hole=0.35, title="Domicile Distribution"
            )
            fig_dom.update_layout(height=320, margin=dict(t=40,b=0,l=0,r=0))

            # Social category
            soc_metrics = ["Socially Challenged (SC+ST+OBC)", "Economically Backward"]
            soc_data = summary[summary["Metric"].isin(soc_metrics)]
            fig_soc = px.bar(
                soc_data, x="Metric", y="Count",
                title="Social Category Breakdown",
                color="Metric",
                color_discrete_sequence=["#e53935","#fb8c00"],
                text="Count"
            )
            fig_soc.update_traces(textposition="outside")
            fig_soc.update_layout(showlegend=False, height=320,
                                   margin=dict(t=40,b=40,l=10,r=10))

            c_d, c_s = st.columns(2)
            with c_d: st.plotly_chart(fig_dom, use_container_width=True)
            with c_s: st.plotly_chart(fig_soc, use_container_width=True)

            # Batch-year distribution
            if df_filtered is not None and not df_filtered.empty:
                batch_col_name = find_col(df_filtered, "Student Batch")
                if batch_col_name:
                    yr_series = df_filtered[batch_col_name].apply(extract_year).dropna().astype(int)
                    yr_counts = yr_series.value_counts().sort_index().reset_index()
                    yr_counts.columns = ["Batch Year", "Count"]
                    fig_yr = px.bar(
                        yr_counts, x="Batch Year", y="Count",
                        title="Students by Batch Year",
                        color="Count", color_continuous_scale="Teal",
                        text="Count"
                    )
                    fig_yr.update_traces(textposition="outside")
                    fig_yr.update_layout(showlegend=False, coloraxis_showscale=False,
                                          height=320, margin=dict(t=40,b=40,l=10,r=10))
                    st.plotly_chart(fig_yr, use_container_width=True)

        # Tab 4 – Filtered rows
        with t4:
            st.markdown(f'<div class="section-header">Filtered Rows — {len(df_filtered):,} students</div>', unsafe_allow_html=True)

            # Quick search
            search = st.text_input("🔍 Search in table", placeholder="Name, department, batch…")
            display_df = df_filtered.copy()
            if search.strip():
                mask_s = display_df.apply(
                    lambda r: r.astype(str).str.contains(search, case=False, na=False).any(), axis=1
                )
                display_df = display_df[mask_s]
                st.caption(f"Showing {len(display_df):,} of {len(df_filtered):,} rows")

            # Column selector
            all_cols = list(df_filtered.columns)
            default_cols = [c for c in ["Student Name","Department Name","Student Batch","Gender",
                                         "Nationality","Domicile State","Social Category","Program Name"]
                            if c in all_cols]
            sel_cols = st.multiselect("Show columns", all_cols, default=default_cols or all_cols[:8])
            if sel_cols:
                st.dataframe(display_df[sel_cols], use_container_width=True, height=500)
            else:
                st.dataframe(display_df, use_container_width=True, height=500)

        # Tab 5 – Export
        with t5:
            st.markdown("#### Download Results")
            xlsx_bytes = to_excel_bytes(counts, df_filtered, summary, label)
            st.download_button(
                label="⬇️ Download Full Excel Report",
                data=xlsx_bytes,
                file_name=f"StudentSummary_{label}_{year_from}_{year_to}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.caption("The Excel file contains 3 sheets: DegreeCounts, FilteredRows, Summary.")

            col_l, col_r = st.columns(2)
            with col_l:
                csv_counts = counts.to_csv(index=False).encode()
                st.download_button("📥 Degree Counts (CSV)", csv_counts,
                                   f"DegreeCounts_{label}.csv", "text/csv", use_container_width=True)
            with col_r:
                csv_summary = summary.to_csv(index=False).encode()
                st.download_button("📥 Summary Metrics (CSV)", csv_summary,
                                   f"Summary_{label}.csv", "text/csv", use_container_width=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Student Data Analyzer · IISc · Powered by Streamlit & Plotly")
