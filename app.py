import streamlit as st

st.set_page_config(
    page_title="Oil Metrics Calculator",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background-color: #0f1117;
}

section[data-testid="stSidebar"] {
    background-color: #161920;
    border-right: 1px solid #2a2d35;
}

/* Metric cards */
div[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 500 !important;
    color: #e8eaf0 !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7280 !important;
}
div[data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
}

/* Section headings */
h1 { color: #e8eaf0 !important; }
h2, h3 { color: #c9cdd8 !important; }
p, li { color: #9ca3af !important; }

/* Divider */
hr { border-color: #2a2d35 !important; }

/* Expander */
details { background-color: #161920 !important; border: 1px solid #2a2d35 !important; border-radius: 8px !important; }
summary { color: #9ca3af !important; }
</style>
""", unsafe_allow_html=True)


# ── Core logic ────────────────────────────────────────────────────────────────
def calculate_oil_metrics(w_crude):
    L = ((w_crude - 0.9) * 20) / 18.1

    if L >= 15.0:
        d = 1.0
    elif L >= 6.0:
        d = 0.5
    elif L >= 1.0:
        d = 0.25
    else:
        d = 0.0

    pre = L - d
    whole = int(pre)
    p = pre - whole

    if p > 0.99:
        cl = whole + 1.0
    elif p >= 0.75:
        cl = whole + 0.75
    elif p >= 0.5:
        cl = whole + 0.5
    elif p >= 0.25:
        cl = whole + 0.25
    else:
        cl = float(whole)

    wcl = ((cl * 18.1) + 0.9) / 20
    return L, d, pre, cl, wcl


def bracket_info(d):
    if d == 1.0:
        return "🟢 Volume bracket: ≥ 15.0 L — deduction **1.0**"
    elif d == 0.5:
        return "🟡 Volume bracket: 6.0 – 14.9 L — deduction **0.5**"
    elif d == 0.25:
        return "🟠 Volume bracket: 1.0 – 5.9 L — deduction **0.25**"
    else:
        return "🔴 Out of range — no deduction applied"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    st.markdown("Adjust the crude oil weight to see all metrics update instantly.")
    st.markdown("---")

    w_crude_input = st.number_input(
        label="Weight of Crude Oil (W)",
        min_value=0.90,
        max_value=25.00,
        value=15.50,
        step=0.10,
        format="%.2f",
        help="Raw crude oil weight measurement."
    )

    st.markdown("---")
    st.caption("💡 Tip: You can also type a value directly into the field above.")

    # Mini pipeline in sidebar
    L_s, d_s, pre_s, cl_s, wcl_s = calculate_oil_metrics(w_crude_input)
    st.markdown("**Pipeline preview**")
    st.markdown(f"""
| Step | Value |
|------|-------|
| W (input) | `{w_crude_input:.2f}` |
| L (volume) | `{L_s:.4f}` |
| d (deduct) | `{d_s:.2f}` |
| CL (clean) | `{cl_s:.2f}` |
| WCL (weight) | `{wcl_s:.4f}` |
""")


# ── Main header ───────────────────────────────────────────────────────────────
st.markdown("# 💧 Oil Metrics Calculator")
st.markdown("Crude weight → clean oil analysis, updated in real time.")
st.markdown("---")

L_val, d_val, pre_val, cl_val, wcl_val = calculate_oil_metrics(w_crude_input)

# Bracket badge
st.info(bracket_info(d_val))

# ── Metric cards ──────────────────────────────────────────────────────────────
st.markdown("### 📊 Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🛢️ Crude Volume (L)",
        value=f"{L_val:.4f}",
        help="Raw calculated volume from crude weight."
    )

with col2:
    st.metric(
        label="📉 Deduction (d)",
        value=f"{d_val:.2f}",
        help="Deduction applied based on volume bracket."
    )

with col3:
    st.metric(
        label="✨ Clean Volume (CL)",
        value=f"{cl_val:.2f}",
        delta=f"−{d_val:.2f} from L",
        help="Volume after deduction and quarter-point rounding."
    )

with col4:
    st.metric(
        label="⚖️ Clean Weight (WCL)",
        value=f"{wcl_val:.4f}",
        help="Weight of the clean oil derived from CL."
    )

st.markdown("---")

# ── Formula breakdown ─────────────────────────────────────────────────────────
st.markdown("### 🔬 Formula Breakdown")

c1, c2 = st.columns(2)

with c1:
    st.markdown(f"""
**Step 1 — Crude Volume**
```
L = ((W − 0.9) × 20) ÷ 18.1
  = (({w_crude_input:.2f} − 0.9) × 20) ÷ 18.1
  = {L_val:.6f}
```

**Step 2 — Deduction**
```
L = {L_val:.4f}  →  d = {d_val:.2f}
{bracket_info(d_val).replace('*', '')}
```
""")

with c2:
    st.markdown(f"""
**Step 3 — Pre-rounded CL**
```
CL_raw = L − d
       = {L_val:.4f} − {d_val:.2f}
       = {pre_val:.6f}
```

**Step 4 — Quarter-point rounding**
```
CL = {cl_val:.2f}
```

**Step 5 — Clean Weight**
```
WCL = (CL × 18.1 + 0.9) ÷ 20
    = ({cl_val:.2f} × 18.1 + 0.9) ÷ 20
    = {wcl_val:.6f}
```
""")

st.markdown("---")

# ── Rounding reference ────────────────────────────────────────────────────────
with st.expander("📐 Quarter-point rounding rules"):
    st.markdown("""
| Decimal part (p) | Rounds to |
|---|---|
| 0.00 – 0.249 | `.00` (floor) |
| 0.25 – 0.499 | `.25` |
| 0.50 – 0.749 | `.50` |
| 0.75 – 0.989 | `.75` |
| ≥ 0.99 | `+1.00` |
""")

with st.expander("🏷️ Deduction bracket reference"):
    st.markdown("""
| Volume range (L) | Deduction (d) |
|---|---|
| ≥ 15.0 | 1.00 |
| 6.0 – 14.9 | 0.50 |
| 1.0 – 5.9 | 0.25 |
| < 1.0 | 0.00 |
""")