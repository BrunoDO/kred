import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="KRED | Financial Command Center",
    page_icon="💳",
    layout="wide"
)

# 2. ALPINE LIGHT UI STYLING
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    .stApp { background-color: #FFFFFF; color: #1A1C1E; font-family: 'Inter', sans-serif; }
    .kred-header { color: #000000; font-weight: 900; letter-spacing: -4px; font-size: 82px; line-height: 1; margin: 0; }
    .tagline { color: #636E72; letter-spacing: 1.5px; font-size: 11px; font-weight: 500; text-transform: uppercase; margin-top: 5px; }
    div[data-testid="stMetric"] { background-color: #F8F9FA; border: 1px solid #EDF0F2; padding: 20px; border-radius: 16px; }
    .stButton>button { border-radius: 8px; border: 1px solid #000; background-color: #000; color: #fff; font-weight: 600; width: 100%; height: 45px; }
    [data-testid="stSidebar"] { background-color: #F8F9FA; border-right: 1px solid #EDF0F2; }
    </style>
""", unsafe_allow_html=True)

# 3. HEADER
st.markdown('<h1 class="kred-header">KRED</h1><p class="tagline">Data Sanitization • Revenue Recovery • Elite Operations</p>', unsafe_allow_html=True)
st.divider()

# 4. SIDEBAR & DATA LOADING
st.sidebar.title("Navigation")
uploaded_file = st.sidebar.file_uploader("Upload Ledger (CSV/XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    # Load Data
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Standardize Column Names
    df.columns = [c.upper().strip() for c in df.columns]
    
    # Core KRED Logic: Calculate Balances
    if 'AMOUNT' in df.columns and 'PAID' in df.columns:
        df['OUTSTANDING'] = df['AMOUNT'] - df['PAID']
        df['STATUS'] = df['OUTSTANDING'].apply(lambda x: "🔴 UNPAID" if x > 0 else "🟢 SETTLED")
    else:
        st.error("Data Error: Please ensure your file has 'AMOUNT' and 'PAID' columns.")
        st.stop()

    # MAIN TABS
    tab1, tab2, tab3 = st.tabs(["📊 Analytics", "📋 Master Ledger", "📩 Outreach"])

    with tab1:
        # Top Level Metrics
        m1, m2, m3 = st.columns(3)
        total_booked = df['AMOUNT'].sum()
        total_paid = df['PAID'].sum()
        total_pending = df['OUTSTANDING'].sum()
        
        m1.metric("Total Revenue", f"${total_booked:,.2f}")
        m2.metric("Collected", f"${total_paid:,.2f}")
        m3.metric("Pending", f"${total_pending:,.2f}")
        
        # Priority Chart
        fig = px.bar(df, x="NAME", y="OUTSTANDING", color="STATUS",
                     title="Revenue Recovery Pipeline",
                     color_discrete_map={"🔴 UNPAID":"#000000", "🟢 SETTLED":"#EDF0F2"},
                     template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Data Sanitization Layer")
        # Editable dataframe for manual corrections
        edited_df = st.data_editor(df, use_container_width=True, hide_index=True)
        
        # Download Cleaned Data
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button("Export Cleaned Ledger", csv, "KRED_Sanitized_Data.csv", "text/csv")

    with tab3:
        st.subheader("Direct Communication")
        unpaid = df[df['OUTSTANDING'] > 0]
        
        if not unpaid.empty:
            selected_client = st.selectbox("Select Client", unpaid['NAME'].unique())
            client_debt = unpaid[unpaid['NAME'] == selected_client]['OUTSTANDING'].sum()
            
            email_template = f"Subject: Account Reconciliation - {selected_client}\n\nOur records indicate an outstanding balance of ${client_debt:,.2f}. Please confirm receipt of this notice."
            st.text_area("Draft Message", email_template, height=150)
            
            st.markdown(f'<a href="mailto:?subject=Payment Reminder&body={email_template}"><button>Open Mail Client</button></a>', unsafe_allow_html=True)
        else:
            st.success("Clean Slate: No outstanding balances detected.")

else:
    # Landing State
    st.markdown("""
        <div style="background-color: #F8F9FA; padding: 60px; border-radius: 24px; text-align: center; border: 1px solid #EDF0F2; margin-top: 30px;">
            <h2 style="font-weight: 800; font-size: 32px; letter-spacing: -1px;">Ready for Reconciliation</h2>
            <p style="color: #636E72; font-size: 18px; margin-bottom: 30px;">Drop your itinerary or ledger here to activate the KRED engine.</p>
            <div style="display: inline-block; text-align: left; background: white; padding: 20px; border-radius: 12px; border: 1px solid #EDF0F2; font-family: monospace;">
                Required: NAME | AMOUNT | PAID
            </div>
        </div>
    """, unsafe_allow_html=True)