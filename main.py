import pandas as pd
import plotly.express as px
import streamlit as st

from backend.util import get_months_between, format_money
from backend.main import get_baseline, get_sip

CURRENCY = "₹"

st.set_page_config(layout="wide")
st.header("Just Do A SIP")
st.write(
    "Instead of spending so much time researching companies, "
    "listening to one stock-tip after the other, "
    "what if ... you simply did a SIP instead?"
)


def get_delta(original: float, current: float) -> str:
    change = (current - original) / original * 100
    return f"{round(change, 2)}% (from baseline)"


def show_graph_and_metric(
    months: list[str], baseline: list[float], worths: list[float]
) -> None:
    df = pd.DataFrame(
        {
            "months": months,
            "baseline": baseline,
            "worth": worths,
        }
    )

    st_graph, st_metric = st.columns([0.8, 0.2])
    st_graph.plotly_chart(
        px.line(df, x="months", y=["baseline", "worth"]),
        use_container_width=True,
    )
    st_metric.metric(
        label="Net Worth",
        value=format_money(worths[-1]),
        delta=get_delta(baseline[-1], worths[-1]),
    )


def show_raw_sip(st=st):
    col1, col2, col3 = st.columns(3)

    start_date = col1.date_input(label="Start date")
    end_date = col2.date_input(label="End date")
    monthly_investment = col3.number_input(
        label=f"Monthly investment amount (in {CURRENCY})",
        min_value=0.0,
    )

    months = get_months_between(start_date, end_date)
    st.write(
        f"*I want to do a SIP of {CURRENCY}{format_money(monthly_investment)} "
        f"for a duration of {len(months)} months.*"
    )

    baseline = get_baseline(months, monthly_investment)
    sip = get_sip("^NSEI", months, monthly_investment)
    show_graph_and_metric(months, baseline, sip)


(raw_sip,) = st.tabs(["Simple SIP Calculator"])
show_raw_sip(raw_sip)
