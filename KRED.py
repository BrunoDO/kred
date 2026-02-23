import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import phonenumbers
from phonenumbers import timezone
import google.generativeai as genai
import stripe

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="KRED | Financial Command Center",
    page_icon="💳",
    layout="wide"
)

# 2. STRIPE & AI CONFIGURATION (Use Streamlit Secrets for Production)
# stripe.api_key = st.secrets["STRIPE_KEY"]
# genai.configure(api_key=st.secrets["GEMINI_KEY"])

# 3. SUCCESS REDIRECT HANDLER
query_params = st.query_params
if query_params.get("payment") == "success":
    st.balloons()
    st.markdown("""
        <div style="text-align: center; padding: 50px; background-color: #F8F9FA; border-radius: 20px; border: 1px solid #00C04B; margin-top: 50px;">
            <h1 style="color: #00C04B; font-size: 60px;">✔</h1>
            <h2 style="color: #000; font-weight: 900; letter-spacing: -2px; font-size: 40px;">PAYMENT VERIFIED</h2>
            <p style="color: #636E72; font-size: 18px;">The transaction has been processed securely via <b>KRED</b>.</p>
            <hr style="border: 0.5px solid #EDF0F2; margin: 30px 0;">
            <a href="/" target="_self"><button style="background-color: #000; color: #fff; padding: 10px 30px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600;">Return to Dashboard</button></a>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# 4. ALPINE LIGHT UI (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    .stApp { background-color: #FFFFFF; color: #1A1C1E; font-family: 'Inter', sans-serif; }
    .kred-header { color: #000000; font-weight: 900; letter-spacing: -4px; font-size: 82px; line-height: 1; margin: 0; }
    .tagline { color: #636E72; letter-spacing: 1.5px; font-size: 11px; font-weight: 500; text-transform: uppercase; margin-top: 5px; }
    div[data-testid="stMetric"] { background-color: #F8F9FA; border: 1px solid #EDF0F2; padding: 20px; border-radius: 16px; }
    .stButton>button { border-radius: 8px; border: 1px solid #000; background-color: #000; color: #fff; font-weight: 600; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# 5. BRANDING HEADER
col_logo, col_title = st.columns([1, 10])
with col_logo:
    try: st.image("logo.png", width=85)
    except: st.info("KRED")

with col_title:
    st.markdown('<div style="height: 85px; display: flex; flex-direction: column; justify-content: center;"><h1 class="kred-header">KRED</h1><p class="tagline">Data Sanitization • Revenue Recovery • AI Intelligence</p></div>', unsafe_allow_html=True)

st.divider()

# 6. SIDEBAR & DATA LOADING
st.sidebar.title("KRED Control")
uploaded_file = st.sidebar.file_uploader("Upload Ledger", type=["csv", "xlsx"])
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Enter key to enable KRED AI Intelligence")

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df.columns = [c.upper().strip() for c in df.columns]
    
    # Financial Logic
    df['OUTSTANDING'] = df.get('AMOUNT', 0) - df.get('PAID', 0)
    df['PRIORITY'] = df['OUTSTANDING'].apply(lambda x: "🔴 HIGH" if x > 500 else ("🟡 MED" if x > 0 else "🟢 PAID"))

    # AI Intelligence Section
    if api_key:
        genai.configure(api_key=api_key)
        st.sidebar.divider()
        user_query = st.sidebar.text_input("Ask KRED AI Analyst...")
        if user_query:
            model = genai.GenerativeModel('gemini-1.5-flash')
            context = f"Data Summary: {df.describe().to_string()}. Debtor list: {df[['NAME', 'OUTSTANDING']].to_string()}"
            with st.sidebar:
                with st.spinner("Analyzing..."):
                    response = model.generate_content(f"{context}\n\nUser Question: {user_query}")
                    st.info(f"**AI Insight:**\n\n{response.text}")

    # MAIN TABS
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "✏️ Master Ledger", "📧 Recovery & Payments"])

    with tab1:
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Revenue", f"${df.get('AMOUNT', 0).sum():,.2f}")
        m2.metric("Collected", f"${df.get('PAID', 0).sum():,.2f}")
        m3.metric("Pending", f"${df['OUTSTANDING'].sum():,.2f}")
        
        fig = px.pie(df, names='PRIORITY', color='PRIORITY', color_discrete_map={"🔴 HIGH":"#000", "🟡 MED":"#636E72", "🟢 PAID":"#EDF0F2"})
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        edited_df = st.data_editor(df, use_container_width=True, hide_index=True)

    with tab3:
        debtors = df[df['OUTSTANDING'] > 0]
        if not debtors.empty:
            selected_user = st.selectbox("Select Debtor", debtors['NAME'].tolist())
            user_data = debtors[debtors['NAME'] == selected_user].iloc[0]
            
            # Payment Link Generation
            if st.button("Generate Stripe Payment Link"):
                # Placeholder for Stripe logic - in real usage, call create_checkout_session here
                st.success(f"Link Generated for {selected_user} for ${user_data['OUTSTANDING']}")
                st.info("Check Stripe Dashboard to finalize redirect URLs.")
            
            # Email Outreach
            email_body = f"Hi {selected_user}, your balance of ${user_data['OUTSTANDING']} is due. Pay here via KRED Secure Link."
            st.text_area("Draft Message", email_body)
            st.markdown(f'<a href="mailto:?body={email_body}"><button style="width:100%; background:black; color:white; border:none; padding:10px; border-radius:8px;">📧 SEND EMAIL</button></a>', unsafe_allow_html=True)
        else:
            st.success("All accounts cleared.")

else:
    # Onboarding Screen
    st.markdown("""
        <div style="background-color: #F8F9FA; padding: 40px; border-radius: 20px; text-align: center; border: 1px solid #EDF0F2;">
            <h2 style="font-weight: 700;">Welcome to KRED Command</h2>
            <p style="color: #636E72;">Upload your financial ledger to activate AI-driven revenue recovery.</p>
        </div>
    """, unsafe_allow_html=True)