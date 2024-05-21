import streamlit as st

from backend.util import get_months_between, format_money

CURRENCY = "₹"

st.header("Just Do A SIP")
st.write(
    "Instead of spending so much time researching companies, "
    "listening to one stock-tip after the other, "
    "what if ... you simply did a SIP instead?"
)


def show_raw_sip(st=st):
    col1, col2, col3 = st.columns(3)

    start_date = col1.date_input(label="Start date")
    end_date = col2.date_input(label="End date")
    monthly = col3.number_input(
        label=f"Monthly investment amount (in {CURRENCY})",
        min_value=0.0,
    )

    months = get_months_between(start_date, end_date)
    st.write(
        f"I want to do a SIP of {CURRENCY}{format_money(monthly)} for a duration of {len(months)} months."
    )


(raw_sip,) = st.tabs(["Simple SIP Calculator"])
show_raw_sip(raw_sip)
