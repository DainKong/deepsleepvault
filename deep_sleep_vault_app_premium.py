
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import random

# --------------------------
# PREMIUM DESIGN STYLING
# --------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500&display=swap');
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        background-color: #0A1A2F;
        color: white;
    }
    .css-18e3th9 {background-color: #0A1A2F;}
    .css-1d391kg {color: #FFD700;}
    </style>
    """,
    unsafe_allow_html=True
)

# Welcome Banner
st.markdown(
    """
    <div style="background-color:#FFD700;padding:20px;border-radius:10px;text-align:center;">
        <h1 style="color:#0A1A2F;">Deep Sleep Vault: Athlete Edition</h1>
        <p style="color:#0A1A2F;">Your personal sleep coach to boost recovery, energy, and performance.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------
# DATA INITIALIZATION
# --------------------------
if 'sleep_data' not in st.session_state:
    st.session_state.sleep_data = pd.DataFrame(columns=['Date', 'Hours Slept', 'Energy Score', 'Notes'])

# --------------------------
# SLEEP LOG FORM
# --------------------------
st.subheader("Log Your Sleep")
with st.form("sleep_log_form"):
    date = st.date_input("Date", datetime.today())
    hours = st.number_input("Hours Slept", min_value=0.0, max_value=24.0, step=0.5)
    energy = st.slider("Energy Score (1 = Exhausted, 10 = Peak Energy)", 1, 10, 7)
    notes = st.text_area("Notes (Optional)", placeholder="e.g., Felt sore, late training...")
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_entry = {'Date': date.strftime('%Y-%m-%d'), 'Hours Slept': hours, 'Energy Score': energy, 'Notes': notes}
        st.session_state.sleep_data = pd.concat([st.session_state.sleep_data, pd.DataFrame([new_entry])], ignore_index=True)
        st.success("Entry added successfully!")

        # Display motivational quote
        quotes = [
            "Psalm 127:2 — God grants sleep to those He loves.",
            "Matthew 11:28 — Come to me, all who are weary, and I will give you rest.",
            "Strong bodies are built in silence — during deep rest.",
            "Recovery is where strength is born. Sleep well tonight!"
        ]
        st.info(random.choice(quotes))

# --------------------------
# DATA DISPLAY AND VISUALS
# --------------------------
if not st.session_state.sleep_data.empty:
    st.subheader("Your Sleep Log")
    st.dataframe(st.session_state.sleep_data.tail(7))

    # Calculate streak
    streak = 0
    sorted_data = st.session_state.sleep_data.sort_values('Date', ascending=False)
    for _, row in sorted_data.iterrows():
        if row['Hours Slept'] >= 8:
            streak += 1
        else:
            break
    if streak > 0:
        st.info(f"🔥 You’re on a {streak}-day streak of 8+ hours! Keep it up!")
        if streak >= 30:
            st.success("🏆 Diamond Badge: 30+ days of greatness!")
        elif streak >= 14:
            st.success("🥇 Gold Badge: 14+ days!")
        elif streak >= 7:
            st.success("🥈 Silver Badge: 7+ days!")
        elif streak >= 3:
            st.success("🥉 Bronze Badge: 3 days in a row!")

    # Weekly Insights
    st.subheader("Weekly Insights")
    recent_data = st.session_state.sleep_data.tail(7)
    avg_hours = recent_data['Hours Slept'].mean()
    max_energy = recent_data['Energy Score'].max()
    st.write(f"**Average Hours Slept:** {avg_hours:.1f} hrs")
    st.write(f"**Highest Energy Score:** {max_energy}/10")

    if avg_hours >= 8:
        st.success("Amazing! Psalm 127:2 — God grants sleep to those He loves. Keep resting strong!")
    else:
        st.warning("You’re averaging below 8 hours. Focus on winding down earlier tonight.")

    # Charts
    st.subheader("Sleep Trend")
    fig, ax = plt.subplots(facecolor='#0A1A2F')
    ax.plot(recent_data['Date'], recent_data['Hours Slept'], marker='o', color='#FFD700', label="Hours Slept")
    ax.axhline(y=8, color='green', linestyle='--', label="Target (8 hrs)")
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    ax.set_title("Sleep Hours vs Target", color='white')
    ax.set_xlabel("Date", color='white')
    ax.set_ylabel("Hours", color='white')
    ax.legend()
    st.pyplot(fig)

    st.subheader("Energy Score Trend")
    fig2, ax2 = plt.subplots(facecolor='#0A1A2F')
    ax2.bar(recent_data['Date'], recent_data['Energy Score'], color='skyblue')
    ax2.set_ylim(0, 10)
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    ax2.set_title("Energy Score (1-10)", color='white')
    ax2.set_xlabel("Date", color='white')
    ax2.set_ylabel("Score", color='white')
    st.pyplot(fig2)

# --------------------------
# EXPORT DATA
# --------------------------
st.download_button(
    label="Download Sleep Log (CSV)",
    data=st.session_state.sleep_data.to_csv(index=False),
    file_name="sleep_log.csv",
    mime="text/csv"
)
