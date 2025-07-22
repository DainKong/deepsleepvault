import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Initialize or load data
if 'sleep_data' not in st.session_state:
    st.session_state.sleep_data = pd.DataFrame(columns=['Date', 'Hours Slept', 'Energy Score', 'Notes'])

st.title("Deep Sleep Vault Tracker (Athlete Edition)")
st.subheader("Your personal sleep coach with streaks, badges, and insights")

# Sleep Log Form
with st.form("sleep_log_form"):
    date = st.date_input("Date", datetime.today())
    hours = st.number_input("Hours Slept", min_value=0.0, max_value=24.0, step=0.5)
    energy = st.slider("Energy Score (1 = Exhausted, 10 = Peak Energy)", 1, 10, 7)
    notes = st.text_area("Notes (Optional)", placeholder="e.g., Felt sore, late training...")
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_entry = {'Date': date.strftime('%Y-%m-%d'), 'Hours Slept': hours, 'Energy Score': energy, 'Notes': notes}
        st.session_state.sleep_data = pd.concat([st.session_state.sleep_data, pd.DataFrame([new_entry])], ignore_index=True)
        st.success("Entry added successfully! Keep going — your rest is your edge.")

# Display Data Table
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
    fig, ax = plt.subplots()
    ax.plot(recent_data['Date'], recent_data['Hours Slept'], marker='o', label="Hours Slept")
    ax.axhline(y=8, color='green', linestyle='--', label="Target (8 hrs)")
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

    st.subheader("Energy Score Trend")
    fig2, ax2 = plt.subplots()
    ax2.bar(recent_data['Date'], recent_data['Energy Score'], color='skyblue')
    ax2.set_ylim(0, 10)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# Export Data
st.download_button(
    label="Download Sleep Log (CSV)",
    data=st.session_state.sleep_data.to_csv(index=False),
    file_name="sleep_log.csv",
    mime="text/csv"
)
