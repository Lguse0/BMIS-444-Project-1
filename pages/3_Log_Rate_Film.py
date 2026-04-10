import streamlit as st
from db import get_film_options, get_rating, upsert_rating

st.set_page_config(page_title="Log / Rate Film", page_icon="⭐")

USER_ID = 1

st.title("⭐ Log / Rate a Film")

film_options = get_film_options()

# 🔒 SAFE GUARD (prevents random crashes)
if not film_options:
    st.error("No films found. Please add films first.")
    st.stop()

film_name = st.selectbox("Choose a Film", list(film_options.keys()))
film_id = film_options.get(film_name)

if film_id is None:
    st.error("Invalid selection.")
    st.stop()

existing = get_rating(USER_ID, film_id)

existing_id = None
rating_default = 0.0
review_default = ""
watched_default = None

if existing:
    existing_id, rating_default, review_default, watched_default = existing

st.markdown("---")

with st.form("rate_form"):
    rating = st.number_input(
        "Rating (0.0 - 5.0)",
        min_value=0.0,
        max_value=5.0,
        step=0.1,
        value=float(rating_default)
    )

    review = st.text_area("Review", value=review_default)
    watched_date = st.date_input("Watched Date")

    submitted = st.form_submit_button("Save Rating")

    if submitted:
        upsert_rating(USER_ID, film_id, rating, review, watched_date, existing_id)
        st.success("Saved successfully!")
