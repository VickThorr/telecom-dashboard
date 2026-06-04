import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Ticket Triage Dashboard", page_icon="🤖", layout="wide")
st.title("🤖 Telecom Support AI Triage Center")
st.markdown("Real-time ticket classification and human escalation metrics.")

# Update this URL to your raw github link or your published Google Sheets CSV link!
DATA_URL = "https://raw.githubusercontent.com/vickthorr/triage-dashboard/main/triagetickettesting(1).csv"

try:
    df = pd.read_csv(DATA_URL)
    df.columns = [c.replace('output.', '').replace('data.', '').strip() for c in df.columns]
    
    total_tickets = len(df)
    
    # Check for escalation tags dynamically
    is_escalated = 0
    if 'escalated' in df.columns:
        is_escalated = len(df[df['escalated'].astype(str).str.upper() == 'TRUE'])
    elif 'routed_queue' in df.columns:
        is_escalated = len(df[df['routed_queue'].astype(str).str.upper() == 'ESCALATED'])

    avg_confidence = df['confidence'].mean() if 'confidence' in df.columns else 0.95

    # Layout Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets Processed", f"{total_tickets}")
    col2.metric("🚨 Sent to Human Escalation", f"{is_escalated}")
    col3.metric("🧠 Avg AI Confidence Score", f"{avg_confidence:.2%}" if avg_confidence <= 1 else f"{avg_confidence}%")

    st.markdown("---")

    left_chart_col, right_chart_col = st.columns(2)

    with left_chart_col:
        st.subheader("Tickets by Category")
        cat_col = [c for c in df.columns if 'cat' in c]
        if cat_col:
            cat_counts = df[cat_col[0]].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            fig_cat = px.bar(cat_counts, x='Category', y='Count', color='Category', template="plotly_dark")
            st.plotly_chart(fig_cat, use_container_width=True)

    with right_chart_col:
        st.subheader("Tickets by Priority Distribution")
        prio_col = [c for c in df.columns if 'prio' in c]
        if prio_col:
            priority_counts = df[prio_col[0]].value_counts().reset_index()
            priority_counts.columns = ['Priority', 'Count']
            fig_prio = px.pie(priority_counts, values='Count', names='Priority', hole=0.4, template="plotly_dark")
            st.plotly_chart(fig_prio, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Live Triage Queue")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.warning("🔄 Setting up cloud data stream dependencies... Please verify files are fully committed to GitHub.")
    st.error(f"Details: {e}")
