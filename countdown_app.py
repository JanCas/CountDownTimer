import streamlit as st
from datetime import date, datetime
import json
import os

SAVE_FILE = "saved_dates.json"

st.set_page_config(page_title="Countdown Timer", page_icon="⏳", layout="centered")


def load_saved_dates():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_dates(dates: dict):
    with open(SAVE_FILE, "w") as f:
        json.dump(dates, f, indent=2)


saved_dates = load_saved_dates()

st.title("⏳ Countdown Timer")
st.markdown("---")

# --- Saved dates selector ---
if saved_dates:
    last_saved_key = list(saved_dates.keys())[-1]
    options = ["— enter manually —"] + list(saved_dates.keys())
    default_index = options.index(last_saved_key)
    selected_id = st.selectbox("Load a saved date:", options, index=default_index)
else:
    selected_id = None

# Determine default date from selection
if selected_id and selected_id != "— enter manually —":
    default_date = date.fromisoformat(saved_dates[selected_id])
else:
    default_date = date.today()

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    target_date = st.date_input(
        "Pick a date to count down to:",
        value=default_date,
    )

with col2:
    unit = st.selectbox(
        "Show countdown in:",
        options=["Days", "Hours", "Minutes"],
        index=1,
    )

# --- Save a date ---
with st.expander("💾 Save this date"):
    save_col1, save_col2 = st.columns([2, 1])
    with save_col1:
        new_id = st.text_input("ID / label for this date:", placeholder="e.g. graduation, vacation")
    with save_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save", use_container_width=True):
            if new_id.strip():
                saved_dates[new_id.strip()] = target_date.isoformat()
                save_dates(saved_dates)
                st.success(f"Saved **{new_id.strip()}** → {target_date.strftime('%B %d, %Y')}")
                st.rerun()
            else:
                st.warning("Please enter an ID before saving.")

# --- Delete a saved date ---
if saved_dates:
    with st.expander("🗑️ Delete a saved date"):
        del_col1, del_col2 = st.columns([2, 1])
        with del_col1:
            to_delete = st.selectbox("Choose a saved date to delete:", list(saved_dates.keys()), key="delete_select")
        with del_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Delete", use_container_width=True):
                del saved_dates[to_delete]
                save_dates(saved_dates)
                st.success(f"Deleted **{to_delete}**.")
                st.rerun()

st.markdown("---")

# --- Countdown display ---
now = datetime.now()
target_dt = datetime(target_date.year, target_date.month, target_date.day)
delta = target_dt - now
total_seconds = delta.total_seconds()

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
    else:
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
