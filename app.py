import streamlit as st
import pandas as pd
from datetime import date, datetime
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Page Configuration
st.set_page_config(
    page_title="Resignation Approval System",
    page_icon="📄",
    layout="wide"
)

# Custom CSS matching the Image Layout
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-card {
        background-color: #FAF8F5;
        border: 1px solid #E7D5C1;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .header-title {
        color: #8C5A2B;
        font-weight: 800;
        font-size: 26px;
        line-height: 1.2;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #8C5A2B;
        font-size: 18px;
        font-weight: 600;
    }
    .profile-card {
        background: #FAF8F5;
        border: 1px solid #D1B89D;
        border-radius: 12px;
        padding: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .profile-img {
        width: 80px;
        height: 80px;
        border-radius: 10px;
        object-fit: cover;
    }
    .journey-box {
        background-color: #FAF8F5;
        border: 1px solid #E7D5C1;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
    }
    .journey-icon {
        background-color: #8C5A2B;
        color: white;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 5px;
        font-size: 14px;
    }
    .metric-pill {
        background-color: #8C5A2B;
        color: white;
        border-radius: 20px;
        padding: 8px 12px;
        text-align: center;
        font-weight: bold;
        font-size: 13px;
        margin-bottom: 5px;
    }
    .metric-val {
        background-color: #FAF8F5;
        border: 1px solid #E7D5C1;
        border-radius: 10px;
        padding: 8px;
        text-align: center;
        font-weight: 800;
        color: #333;
    }
    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }
    .data-table th {
        background-color: #8C5A2B;
        color: white;
        padding: 10px;
        text-align: left;
    }
    .data-table td {
        padding: 8px 12px;
        border-bottom: 1px solid #E7D5C1;
        font-size: 14px;
    }
    .data-table tr:nth-child(even) {
        background-color: #FAF8F5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State Database
if 'resignations' not in st.session_state:
    st.session_state.resignations = []

# Helper Function: Translate / Format to English
def to_english_str(text):
    if not text:
        return ""
    # Arabic to English numbers conversion
    arabic_num = "٠١٢٣٤٥٦٧٨٩"
    english_num = "0123456789"
    trans = str.maketrans(arabic_num, english_num)
    return str(text).translate(trans)

# Sidebar - Controls & Inputs
st.sidebar.header("⚙️ Enter Resignation Data")

# 1. Profile Upload & Personal Info
st.sidebar.subheader("👤 Employee Profile")
uploaded_photo = st.sidebar.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])
employee_name = to_english_str(st.sidebar.text_input("Employee Name", "Abu Bakr Muhammad Mahmoud"))
job_title = to_english_str(st.sidebar.text_input("Job Title / Position", "Sales Casual"))
branch = to_english_str(st.sidebar.text_input("Branch", "Park-St Branch"))
grading = to_english_str(st.sidebar.text_input("Grading System", "G1 - L1"))

# 2. Key Dates & Experience
st.sidebar.subheader("📅 Dates & Timeline")
hiring_date = st.sidebar.date_input("Hiring / Joined Date", date(2026, 10, 3))
resignation_date = st.sidebar.date_input("Resignation Letter Submitted", date(2026, 10, 20))
last_working_day = st.sidebar.date_input("Last Working Day", date(2026, 10, 20))

# 3. Manager & Compensation Details
st.sidebar.subheader("💼 Manager & Dues")
direct_manager = to_english_str(st.sidebar.text_input("Direct Manager", "Sherif S. El-Sayed"))
reason = to_english_str(st.sidebar.text_input("Reason for Leaving", "Education"))
net_pay = st.sidebar.number_input("Total Net Pay (EGP)", value=7000, step=500)
notice_period = to_english_str(st.sidebar.text_input("Notice Period Status", "One Month"))
handover_status = to_english_str(st.sidebar.text_input("Handover Status", "Team Leader"))
absence_days = st.sidebar.number_input("Absence during the year (Days)", value=0)
loan_balance = st.sidebar.number_input("Loan Balance (EGP)", value=0)

# Calculate total experience in days
exp_days = (resignation_date - hiring_date).days

# Save Button to Store Record in Database
if st.sidebar.button("💾 Save Resignation Record", type="primary"):
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Employee Name": employee_name,
        "Job Title": job_title,
        "Branch": branch,
        "Hiring Date": hiring_date.strftime("%d/%m/%Y"),
        "Resignation Date": resignation_date.strftime("%d/%m/%Y"),
        "Last Working Day": last_working_day.strftime("%d/%m/%Y"),
        "Total Net Pay (EGP)": net_pay,
        "Reason": reason,
        "Direct Manager": direct_manager,
        "Notice Period": notice_period
    }
    st.session_state.resignations.insert(0, record) # Insert at beginning (Newest to Oldest)
    st.sidebar.success("Saved successfully!")

# Tab Layout
tab1, tab2, tab3 = st.tabs(["📄 Approval View", "📊 Resignations Database", "📧 Send via Email"])

with tab1:
    # Top Header
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"#### Dear Mr. {direct_manager.split()[0] if direct_manager else 'Manager'},")
        st.markdown('<div class="header-title">RESIGNATION<br>APPROVAL REQUEST</div>', unsafe_allow_html=True)
    
    with c2:
        # Display Photo or Default
        if uploaded_photo:
            st.image(uploaded_photo, width=110)
        else:
            st.markdown("👤 *No Profile Picture Uploaded*")
            
        st.markdown(f"**EMPLOYEE PROFILE**\n\n### {employee_name}\n*{job_title}*\n\nResigning {resignation_date.strftime('%d %b %Y')}")

    st.markdown("---")
    
    # Resignation Journey
    st.subheader("Resignation Journey")
    j1, j2, j3, j4, j5 = st.columns(5)
    
    with j1:
        st.markdown(f'<div class="journey-box"><div class="journey-icon">👤</div><br><b>Joined</b><br>{hiring_date.strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)
    with j2:
        st.markdown(f'<div class="journey-box"><div class="journey-icon">🏆</div><br><b>Total Experience</b><br>{exp_days} Days</div>', unsafe_allow_html=True)
    with j3:
        st.markdown(f'<div class="journey-box"><div class="journey-icon">📄</div><br><b>Resignation Submitted</b><br>{resignation_date.strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)
    with j4:
        st.markdown(f'<div class="journey-box"><div class="journey-icon">🕒</div><br><b>Notice Period</b><br>{notice_period}</div>', unsafe_allow_html=True)
    with j5:
        st.markdown(f'<div class="journey-box"><div class="journey-icon">✅</div><br><b>Process Finalized</b><br>Approved<br>{resignation_date.strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Key Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="metric-pill">Total Net Pay (EGP)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-val">{net_pay}</div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-pill">Last Working Day</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-val">{last_working_day.strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-pill">Reason for Leaving</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-val">{reason}</div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="metric-pill">Direct Manager</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-val">{direct_manager}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Details Table
    details_df = pd.DataFrame([
        ("Employee Name", employee_name),
        ("Branch", branch),
        ("Job Title", job_title),
        ("Hiring Date", hiring_date.strftime("%d/%m/%Y")),
        ("Resignation Date", resignation_date.strftime("%d/%m/%Y")),
        ("Last Working Day", last_working_day.strftime("%d/%m/%Y")),
        ("Grading System", grading),
        ("Total Net to pay EGP", str(net_pay)),
        ("Reason for Leaving", reason),
        ("Notice Period Status", notice_period),
        ("Handover Status", handover_status),
        ("Total Experience", f"{exp_days} Day"),
        ("Direct Manager", direct_manager),
        ("Absence during the year", f"{absence_days} Day"),
        ("Loan balance", f"{loan_balance} EGP")
    ], columns=["Field", "Value"])

    st.table(details_df)

with tab2:
    st.subheader("📋 Resignation Log (Newest to Oldest)")
    
    # Search Filter
    search_query = st.text_input("🔍 Search Employee Name:", "").strip()
    
    if st.session_state.resignations:
        df_log = pd.DataFrame(st.session_state.resignations)
        
        # Apply Search Filter
        if search_query:
            df_log = df_log[df_log['Employee Name'].str.contains(search_query, case=False, na=False)]
            
        st.dataframe(df_log, use_container_width=True)
        
        # CSV Export
        csv_data = df_log.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV Log", data=csv_data, file_name="resignations_log.csv", mime="text/csv")
    else:
        st.info("No saved resignation records yet. Click 'Save Resignation Record' in the sidebar to add records.")

with tab3:
    st.subheader("📧 Send Resignation Summary via Email")
    
    smtp_server = st.text_input("SMTP Server", "smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", value=587)
    sender_email = st.text_input("Sender Email")
    sender_password = st.text_input("Sender App Password", type="password")
    receiver_email = st.text_input("Recipient Email")
    
    if st.button("🚀 Send Email"):
        if not sender_email or not sender_password or not receiver_email:
            st.error("Please fill in all email configuration credentials.")
        else:
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = f"Resignation Request - {employee_name}"
                msg['From'] = sender_email
                msg['To'] = receiver_email

                # HTML Template matching the layout
                html_body = f"""
                <html>
                <body style="font-family: Arial, sans-serif; background-color: #FAF8F5; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: white; border: 1px solid #E7D5C1; padding: 20px; border-radius: 10px;">
                        <h2 style="color: #8C5A2B;">RESIGNATION APPROVAL REQUEST</h2>
                        <p><b>Employee Name:</b> {employee_name}</p>
                        <p><b>Job Title:</b> {job_title}</p>
                        <p><b>Branch:</b> {branch}</p>
                        <p><b>Resignation Date:</b> {resignation_date.strftime("%d/%m/%Y")}</p>
                        <p><b>Last Working Day:</b> {last_working_day.strftime("%d/%m/%Y")}</p>
                        <p><b>Total Net Pay:</b> {net_pay} EGP</p>
                        <p><b>Reason:</b> {reason}</p>
                        <p><b>Direct Manager:</b> {direct_manager}</p>
                    </div>
                </body>
                </html>
                """
                msg.attach(MIMEText(html_body, 'html'))

                server = smtplib.SMTP(smtp_server, int(smtp_port))
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                server.quit()
                
                st.success("Email sent successfully!")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
