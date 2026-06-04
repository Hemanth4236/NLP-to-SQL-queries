import streamlit as st

from src.execute_query import run_query
from src.generate_sql import generate_sql

st.set_page_config(
    page_title="SQL Lens",
    page_icon="⌘",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --bg: #0b1020;
            --panel: rgba(15, 23, 42, 0.82);
            --panel-strong: rgba(15, 23, 42, 0.96);
            --line: rgba(148, 163, 184, 0.18);
            --text: #e5eefb;
            --muted: #9fb1cc;
            --accent: #7dd3fc;
            --accent-2: #c084fc;
            --good: #34d399;
            --warn: #fbbf24;
        }

        .stApp {
            background:
                radial-gradient(circle at 15% 20%, rgba(124, 58, 237, 0.30), transparent 30%),
                radial-gradient(circle at 85% 12%, rgba(14, 165, 233, 0.22), transparent 28%),
                linear-gradient(180deg, #080c18 0%, #0b1020 45%, #0f172a 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2rem;
        }

        .hero {
            position: relative;
            overflow: hidden;
            border: 1px solid var(--line);
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.72));
            border-radius: 28px;
            padding: 1.7rem 1.8rem 1.5rem 1.8rem;
            box-shadow: 0 22px 70px rgba(0, 0, 0, 0.35);
            margin-bottom: 1rem;
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: auto -12% -45% auto;
            width: 280px;
            height: 280px;
            background: radial-gradient(circle, rgba(125, 211, 252, 0.22), transparent 68%);
            pointer-events: none;
        }

        .eyebrow {
            color: var(--accent);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }

        .title {
            font-size: clamp(2.2rem, 5vw, 3.8rem);
            line-height: 1.0;
            margin: 0;
            color: var(--text);
            font-weight: 800;
        }

        .subtitle {
            max-width: 72ch;
            margin-top: 0.85rem;
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.65;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1rem;
        }

        .pill {
            border: 1px solid var(--line);
            background: rgba(255, 255, 255, 0.04);
            color: var(--text);
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            font-size: 0.88rem;
        }

        .panel {
            border: 1px solid var(--line);
            border-radius: 24px;
            background: var(--panel);
            box-shadow: 0 14px 50px rgba(0, 0, 0, 0.22);
            padding: 1.15rem 1.2rem;
        }

        .panel-strong {
            background: var(--panel-strong);
        }

        .section-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.65rem;
        }

        .sql-box pre {
            border-radius: 18px !important;
            border: 1px solid var(--line) !important;
            background: #0b1220 !important;
            padding: 1rem !important;
        }

        div[data-testid="stTextArea"] textarea,
        div[data-testid="stTextInput"] input {
            background: rgba(2, 6, 23, 0.8) !important;
            color: var(--text) !important;
            border: 1px solid rgba(148, 163, 184, 0.22) !important;
            border-radius: 16px !important;
            padding: 0.95rem 1rem !important;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid var(--line);
        }

        .stButton > button {
            border-radius: 14px;
            border: 1px solid rgba(125, 211, 252, 0.24);
            background: linear-gradient(135deg, rgba(125, 211, 252, 0.18), rgba(192, 132, 252, 0.18));
            color: var(--text);
            font-weight: 700;
            padding: 0.7rem 1rem;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: rgba(125, 211, 252, 0.55);
        }

        .metric-card {
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 1rem 1rem 0.85rem 1rem;
            background: rgba(15, 23, 42, 0.9);
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--text);
            font-size: 1.4rem;
            font-weight: 800;
            margin-top: 0.35rem;
        }

        .metric-note {
            color: var(--muted);
            font-size: 0.88rem;
            margin-top: 0.25rem;
        }

        .sidebar-card {
            border: 1px solid var(--line);
            border-radius: 20px;
            background: rgba(15, 23, 42, 0.75);
            padding: 1rem;
            margin-bottom: 0.8rem;
        }

        .sidebar-card h4 {
            margin: 0 0 0.4rem 0;
            color: var(--text);
            font-size: 0.98rem;
        }

        .sidebar-card p, .sidebar-card li {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.5;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "question" not in st.session_state:
    st.session_state.question = ""


def _set_question(value):
    st.session_state.question = value


st.sidebar.markdown(
    """
    <div class="sidebar-card">
        <h4>What this app understands</h4>
        <p>Natural-language questions over the employee demo database, including filters, counts, averages, joins, and hire-date lookups.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div class="sidebar-card">
        <h4>Quick examples</h4>
        <p>Click any example in the main panel to auto-fill the question box.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Natural Language to SQL</div>
        <h1 class="title">SQL Lens</h1>
        <p class="subtitle">
            Ask questions in plain English and turn them into live SQL queries.
            The interface is tuned for fast exploration, clean reading, and a more polished demo feel.
        </p>
        <div class="pill-row">
            <span class="pill">Filters</span>
            <span class="pill">Aggregates</span>
            <span class="pill">JOINs</span>
            <span class="pill">Hire dates</span>
            <span class="pill">Top N</span>
            <span class="pill">Ranking</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Dataset</div>
            <div class="metric-value">Employees</div>
            <div class="metric-note">with department details and hire dates</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_b:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Query Styles</div>
            <div class="metric-value">20+</div>
            <div class="metric-note">count, average, join, sort, and filter patterns</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_c:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Display Mode</div>
            <div class="metric-value">Wide</div>
            <div class="metric-note">built for a cleaner review and demo experience</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

st.markdown('<div class="panel panel-strong">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Try a question</div>', unsafe_allow_html=True)

example_cols = st.columns(3)
examples = [
    "How many employees are in IT?",
    "Show employees with their manager",
    "Show employees hired after 2023",
    "Find employees earning less than 50,000",
    "Show second highest paid employees",
    "Show IT or HR employees with salary above 50000",
]

for index, example in enumerate(examples):
    with example_cols[index % 3]:
        if st.button(example, key=f"example_{index}", use_container_width=True):
            _set_question(example)

st.text_area(
    "Ask your question",
    key="question",
    height=110,
    placeholder="Example: Show IT employees earning more than 60000",
    label_visibility="collapsed",
)

run_col, info_col = st.columns([1, 3])
with run_col:
    run_clicked = st.button("Generate SQL", use_container_width=True)
with info_col:
    st.caption("Tip: use phrases like 'between', 'after 2023', 'with their manager', or 'top 2'.")

st.markdown("</div>", unsafe_allow_html=True)

if run_clicked:
    question = st.session_state.question

    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        sql = generate_sql(question)

        result_area = st.container()
        with result_area:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Generated SQL</div>', unsafe_allow_html=True)
            st.code(sql, language="sql")
            st.markdown("</div>", unsafe_allow_html=True)

        try:
            result = run_query(sql)
        except Exception as exc:
            st.error(f"Could not run the query: {exc}")
        else:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

            if result.empty:
                st.info("No matching records found.")
            elif len(result.columns) == 1 and result.shape[0] == 1 and result.columns[0].lower() in {"count", "average_salary", "total_salary", "max_salary", "min_salary"}:
                metric_value = result.iloc[0, 0]
                st.metric(label=result.columns[0].replace("_", " ").title(), value=metric_value)
            else:
                st.dataframe(result, use_container_width=True, hide_index=True)

            st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <div class="sidebar-card">
        <h4>Supported patterns</h4>
        <ul>
            <li>Counts and aggregates</li>
            <li>Department and name filters</li>
            <li>Salary comparisons and ranges</li>
            <li>JOINs with department manager/location</li>
            <li>Hire-date queries</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)
