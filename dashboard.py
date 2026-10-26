import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart-SIEM Enterprise Dashboard",
    page_icon="🛡️",
    layout="wide"
)

API_URL = "https://smart-siem.onrender.com/api/v1/logs"

st.title("🛡️ Smart-SIEM: Enterprise Threat & Noise Reduction Dashboard")
st.markdown("Monitoring 1,000+ simulated cloud endpoints in real-time.")

# Refresh button to fetch latest data
if st.button("🔄 Refresh Logs Data", type="primary"):
    st.rerun()
try:
    # Fetch data from FastAPI backend
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        total_logs = data.get("total_logs_received", 0)
        logs_list = data.get("logs", [])
        
        if total_logs > 0:
            df = pd.DataFrame(logs_list)

            # --- METRICS DISPLAY ---
            noise_count = int(df["is_noise"].sum())
            threat_count = total_logs - noise_count
            efficiency = round((noise_count / total_logs) * 100, 1)

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Logs Processed", total_logs)
            m2.metric("Noise Filtered Out", noise_count, delta=f"-{efficiency}% Noise Reduction")
            m3.metric("Real Threats Flagged", threat_count, delta_color="inverse")
            m4.metric("System Efficiency", f"{efficiency}%")

            st.markdown("---")

            # --- VISUAL GRAPHS & CHARTS ---
            c1, c2 = st.columns(2)

            with c1:
                st.markdown("### 🍩 Traffic Distribution")
                fig_pie = px.pie(
                    names=["Filtered Noise", "Real Threats"],
                    values=[noise_count, threat_count],
                    color_discrete_sequence=["#2ea043", "#da3633"],
                    hole=0.4
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with c2:
                st.markdown("### 📊 Top Threat Actions Detected")
                threats_only = df[df["is_noise"] == False]
                if not threats_only.empty:
                    action_counts = threats_only["action"].value_counts().reset_index()
                    action_counts.columns = ["Action", "Count"]
                    fig_bar = px.bar(
                        action_counts, 
                        x="Action", 
                        y="Count", 
                        color="Count",
                        color_continuous_scale="Reds"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No threats detected yet!")

            st.markdown("---")

            # --- LIVE SECURITY TRIAGE TABLE ---
            st.markdown("### 📊 Live Security Triage Table")
            
            filter_option = st.radio("Filter View:", ["All Logs", "Only Real Threats", "Only Filtered Noise"], horizontal=True)
            
            filtered_df = df.copy()
            if filter_option == "Only Real Threats":
                filtered_df = filtered_df[filtered_df["is_noise"] == False]
            elif filter_option == "Only Filtered Noise":
                filtered_df = filtered_df[filtered_df["is_noise"] == True]

            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("⚠️ No logs received yet. Please run your client simulator to send logs!")
    else:
        st.error("❌ Could not connect to the FastAPI backend server.")
except Exception as e:
    st.error(f"Connection Error: {e}")