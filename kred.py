import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse

# 1. PAGE CONFIG
st.set_page_config(page_title="KRED | Financial Command Center", page_icon="💳", layout="wide")

# 2. STYLING (Your Alpine Light Style)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1A1C1E; font-family: 'Inter', sans-serif; }
    .kred-header { color: #000; font-weight: 900; letter-spacing: -3px; font-size: 72px; margin: 0; }
    div[data-testid="stMetric"] { background-color: #F8F9FA; border: 1px solid #EDF0F2; padding: 20px; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# 3. SESSION STATE (The Brain)
# This keeps your data alive even when the app refreshes
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['NAME', 'AMOUNT', 'PAID', 'OUTSTANDING', 'STATUS'])

# 4. HEADER
st.markdown('<h1 class="kred-header">KRED</h1>', unsafe_allow_html=True)
st.divider()

# 5. SIDEBAR / UPLOAD
st.sidebar.title("KRED Control")
uploaded_file = st.sidebar.file_uploader("Upload Ledger", type=["csv", "xlsx"])

if uploaded_file:
    # Read data only if it's not already in session state or user wants to reset
    if st.sidebar.button("Initialize/Reset Data"):
        new_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        new_df.columns = [c.upper().strip() for c in new_df.columns]
        st.session_state.df = new_df

# 6. CORE LOGIC (Auto-Recalculate)
if not st.session_state.df.empty:
    # Reference the session state data
    current_df = st.session_state.df
    
    # Auto-calculate math
    if 'AMOUNT' in current_df.columns and 'PAID' in current_df.columns:
        current_df['OUTSTANDING'] = current_df['AMOUNT'] - current_df['PAID']
        current_df['STATUS'] = current_df['OUTSTANDING'].apply(lambda x: "🔴 UNPAID" if x > 0 else "🟢 SETTLED")
    
    tab1, tab2, tab3 = st.tabs(["📊 Analytics", "📋 Master Ledger", "📩 Outreach"])

    with tab1:
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Revenue", f"${current_df['AMOUNT'].sum():,.2f}")
        m2.metric("Collected", f"${current_df['PAID'].sum():,.2f}")
        m3.metric("Pending", f"${current_df['OUTSTANDING'].sum():,.2f}")
        
        fig = px.bar(current_df, x="NAME", y="OUTSTANDING", color="STATUS", 
                     title="Revenue Recovery Pipeline",
                     color_discrete_map={"🔴 UNPAID":"#000000", "🟢 SETTLED":"#EDF0F2"}, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Data Sanitization Layer")
        # num_rows="dynamic" is what allows you to add/delete customers
        edited_df = st.data_editor(current_df, num_rows="dynamic", use_container_width=True, hide_index=True)
        
        # This button "saves" the edits back to the session state
        if st.button("💾 Save & Actualize Changes"):
            st.session_state.df = edited_df
            st.rerun()

        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button("Export Cleaned Ledger", csv, "KRED_Sanitized_Data.csv", "text/csv")

    with tab3:
        st.subheader("Direct Communication")
        unpaid = current_df[current_df['OUTSTANDING'] > 0]
        if not unpaid.empty:
            selected_client = st.selectbox("Select Client", unpaid['NAME'].unique())
            client_debt = unpaid[unpaid['NAME'] == selected_client]['OUTSTANDING'].sum()
            
            email_body = f"Subject: Account Reconciliation - {selected_client}\n\nOur records indicate an outstanding balance of ${client_debt:,.2f}. Please confirm receipt of this notice."
            st.text_area("Draft Message", email_body, height=150)
            
            # FIXED MAILTO ENCODING
            subject = "Payment Reminder"
            encoded_subject = urllib.parse.quote(subject)
            encoded_body = urllib.parse.quote(email_body)
            mail_link = f"mailto:?subject={encoded_subject}&body={encoded_body}"
            
            st.markdown(f'<a href="{mail_link}" target="_blank"><button style="background:#000;color:#fff;padding:10px;border-radius:5px;cursor:pointer;">Open Mail Client</button></a>', unsafe_allow_html=True)
        else:
            st.success("Clean Slate: No outstanding balances detected.")
else:
    # Your Landing State
    st.markdown("""
        <div style="background-color: #F8F9FA; padding: 60px; border-radius: 24px; text-align: center; border: 1px solid #EDF0F2; margin-top: 30px;">
            <h2 style="font-weight: 800; font-size: 32px; letter-spacing: -1px;">Ready for Reconciliation</h2>
            <p style="color: #636E72; font-size: 18px; margin-bottom: 30px;">Drop your itinerary or ledger here to activate the KRED engine.</p>
            <div style="display: inline-block; text-align: left; background: white; padding: 20px; border-radius: 12px; border: 1px solid #EDF0F2; font-family: monospace;">
                Required: NAME | AMOUNT | PAID
            </div>
        </div>
    """, unsafe_allow_html=True)