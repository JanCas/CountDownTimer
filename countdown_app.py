import streamlit as st
from datetime import date, datetime

st.set_page_config(page_title="Countdown Timer", page_icon="⏳", layout="centered")

st.title("⏳ Countdown Timer")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    target_date = st.date_input(
        "Pick a date to count down to:",
        value=date.today(),
    )

with col2:
    unit = st.selectbox(
        "Show countdown in:",
        options=["Days", "Hours", "Minutes"],
    )

now = datetime.now()
target_dt = datetime(target_date.year, target_date.month, target_date.day)
delta = target_dt - now
total_seconds = delta.total_seconds()

st.markdown("---")

if total_seconds < 0:
    st.markdown(
        """
        <div style='text-align: center;'>
            <p style='font-size: 2rem; color: gray;'>That date has already passed.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif total_seconds < 60:
    st.markdown(
        """
        <div style='text-align: center;'>
            <p style='font-size: 5rem; font-weight: 900; color: #e63946;'>🎉 Today's the day!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    if unit == "Days":
        value = int(total_seconds // 86400)
        label = "day" if value == 1 else "days"
    elif unit == "Hours":
        value = int(total_seconds // 3600)
        label = "hour" if value == 1 else "hours"
    else:  # Minutes
        value = int(total_seconds // 60)
        label = "minute" if value == 1 else "minutes"

    formatted_value = f"{value:,}"

    st.markdown(
        f"""
        <div style='text-align: center;'>
            <p style='font-size: 1.4rem; color: #888;'>Until <strong>{target_date.strftime("%B %d, %Y")}</strong></p>
            <p style='font-size: 8rem; font-weight: 900; line-height: 1; color: #1a73e8;'>{formatted_value}</p>
            <p style='font-size: 2.5rem; font-weight: 600; color: #555;'>{label} to go</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
