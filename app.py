import streamlit as st
import pandas as pd
from datetime import date, datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Resignation Approval System",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------------
# Custom CSS (Matching the Exact Image Colors & Styling)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8F6F0;
    }
    
    /* Main Layout Containers */
    .stApp {
        background-color: #F8F6F0;
    }
    
    .approval-card {
        background-color: #FAF8F5;
        border: 1.5px solid #D6C2A7;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    /* Headers & Titles */
    .req-subtitle {
        color: #8C5A2B;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .req-title {
        color: #8C5A2B;
        font-weight: 800;
        font-size: 26px;
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    
    /* Employee Card */
    .emp-card-box {
        background: #FAF8F5;
        border: 1px solid #D6C2A7;
        border-radius: 10px;
        padding: 12px 16px;
        display: flex;
        gap: 15px;
        align-items: center;
    }
    .emp-label {
        font-size: 10px;
        text-transform: uppercase;
        color: #8C5A2B;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    .emp-name {
        font-size: 18px;
        font-weight: 800;
        color: #111;
        margin: 2px 0;
    }
    .emp-title {
        font-size: 13px;
        color: #444;
    }
    .emp-resign-date {
        font-size: 12px;
        color: #666;
        margin-top: 4px;
    }

    /* Journey Box */
    .journey-item {
        background-color: #FAF8F5;
        border: 1px solid #D6C2A7;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        min-height: 90px;
    }
    .journey-icon {
        background-color: #8C5A2B;
        color: white;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        margin-bottom: 4px;
    }
    .journey-title {
        font-size: 11px;
        font-weight: 700;
        color: #111;
    }
    .journey-val {
        font-size: 12px;
        color: #333;
    }

    /* Key Metrics / Pills */
    .metric-header {
        background-color: #8C5A2B;
        color: white;
        border-radius: 18px;
        padding: 6px 10px;
        text-align: center;
        font-weight: 700;
        font-size: 12px;
        margin-bottom: 6px;
    }
    .metric-body {
        background-color: #FAF8F5;
        border: 1px solid #D6C2A7;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        font-weight: 800;
        font-size: 14px;
        color: #111;
    }

    /* Table Styling */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        border: 1px solid #D6C2A7;
    }
    .custom-table th {
        background-color: #8C5A2B;
        color: white;
        padding: 8px 12px;
        text-align: left;
        font-size: 13px;
        font-weight: 700;
    }
    .custom-table td {
        padding: 6px 12px;
        border-bottom: 1px solid #EADBCE;
        font-size: 13px;
        color: #222;
    }
    .custom-table tr:nth-child(even) {
        background-color: #FAF8F5;
    }
    .custom-table tr:nth-child(odd) {
        background-color: #FFFFFF;
    }

    /* Action Box */
    .action-box {
        background-color: #FAF8F5;
        border: 1px solid #D6C2A7;
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
    }
    .action-title {
        color: #8C5A2B;
        font-weight: 800;
        font-size: 15px;
        margin-bottom: 2px;
    }
    .action-subtitle {
        color: #8C5A2B;
        font-weight: 700;
        font-size: 13px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------
if 'resignations_db' not in st.session_state:
    st.session_state.resignations_db = [
        {
            "employee_name": "Abu Bakr Muhammad Mahmoud",
            "job_title": "Sales Casual",
            "branch": "Park-St Branch",
            "grading": "G1 - L1",
            "hiring_date": "2026-10-03",
            "resignation_date": "2026-10-20",
            "last_working_day": "2026-10-20",
            "net_pay": 7000,
            "reason": "Education",
            "direct_manager": "Sherif S. El-Sayed",
            "notice_period": "One Month",
            "handover_status": "Team Leader",
            "absence_days": 0,
            "loan_balance": 0,
            "photo": None,
            "exp_days": 17
        }
    ]

# Active selected employee index
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = 0

# Helper to normalize input to English
def to_english_str(text):
    if not text:
        return ""
    arabic_num = "٠١٢٣٤٥٦٧٨٩"
    english_num = "0123456789"
    trans = str.maketrans(arabic_num, english_num)
    return str(text).translate(trans)

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.title("📌 Main Menu")
page = st.sidebar.radio("Navigate to:", ["📝 Register New Resignation", "📄 Resignation Approval View", "📊 Branches & Resignations Dashboard"])

# ---------------------------------------------------------
# PAGE 1: REGISTER NEW RESIGNATION
# ---------------------------------------------------------
if page == "📝 Register New Resignation":
    st.title("📝 Register New Resignation")
    st.write("Fill out the employee information below. All data will be automatically converted and styled.")

    with st.form("resignation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            emp_name = to_english_str(st.text_input("Employee Name", "Abu Bakr Muhammad Mahmoud"))
            job_title = to_english_str(st.text_input("Job Title / Role", "Sales Casual"))
            branch = to_english_str(st.text_input("Branch Name", "Park-St Branch"))
            grading = to_english_str(st.text_input("Grading System", "G1 - L1"))
            direct_manager = to_english_str(st.text_input("Direct Manager Name", "Sherif S. El-Sayed"))
            reason = to_english_str(st.text_input("Reason for Leaving", "Education"))
            
        with col2:
            hiring_date = st.date_input("Hiring / Joined Date", date(2026, 10, 3))
            resignation_date = st.date_input("Resignation Date", date(2026, 10, 20))
            last_working_day = st.date_input("Last Working Day", date(2026, 10, 20))
            net_pay = st.number_input("Total Net Pay (EGP)", value=7000, step=500)
            notice_period = to_english_str(st.text_input("Notice Period Status", "One Month"))
            handover_status = to_english_str(st.text_input("Handover Status", "Team Leader"))
            
        col3, col4 = st.columns(2)
        with col3:
            absence_days = st.number_input("Absence Days", value=0)
            loan_balance = st.number_input("Loan Balance (EGP)", value=0)
        with col4:
            photo_file = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("💾 Save Resignation Record", type="primary")

        if submitted:
            exp_days = (resignation_date - hiring_date).days
            
            photo_bytes = photo_file.getvalue() if photo_file else None

            new_record = {
                "employee_name": emp_name,
                "job_title": job_title,
                "branch": branch,
                "grading": grading,
                "hiring_date": hiring_date.strftime("%Y-%m-%d"),
                "resignation_date": resignation_date.strftime("%Y-%m-%d"),
                "last_working_day": last_working_day.strftime("%Y-%m-%d"),
                "net_pay": net_pay,
                "reason": reason,
                "direct_manager": direct_manager,
                "notice_period": notice_period,
                "handover_status": handover_status,
                "absence_days": absence_days,
                "loan_balance": loan_balance,
                "photo": photo_bytes,
                "exp_days": exp_days
            }
            
            # Insert at top (Newest First)
            st.session_state.resignations_db.insert(0, new_record)
            st.session_state.selected_index = 0
            st.success("✅ Resignation recorded successfully! You can view the template in 'Resignation Approval View'.")

# ---------------------------------------------------------
# PAGE 2: RESIGNATION APPROVAL VIEW
# ---------------------------------------------------------
elif page == "📄 Resignation Approval View":
    if not st.session_state.resignations_db:
        st.warning("No resignation records available. Please add one first.")
    else:
        # Selector for employee records
        emp_names = [f"{r['employee_name']} ({r['branch']})" for r in st.session_state.resignations_db]
        selected_idx = st.selectbox("Select Employee Record to Display:", range(len(emp_names)), format_func=lambda x: emp_names[x])
        data = st.session_state.resignations_db[selected_idx]

        # Convert date strings back for formatting
        h_date = datetime.strptime(data['hiring_date'], "%Y-%m-%d").strftime("%d/%m/%Y")
        r_date = datetime.strptime(data['resignation_date'], "%Y-%m-%d").strftime("%d/%m/%Y")
        l_date = datetime.strptime(data['last_working_day'], "%Y-%m-%d").strftime("%d/%m/%Y")
        r_date_header = datetime.strptime(data['resignation_date'], "%Y-%m-%d").strftime("%d %b %Y")

        st.markdown('<div class="approval-card">', unsafe_allow_html=True)
        
        # Header Section
        head_col1, head_col2 = st.columns([1.8, 1.2])
        with head_col1:
            mgr_first = data['direct_manager'].split()[0] if data['direct_manager'] else 'Manager'
            st.markdown(f'<div class="req-subtitle">Dear Mr. {mgr_first},</div>', unsafe_allow_html=True)
            st.markdown('<div class="req-title">RESIGNATION<br>APPROVAL REQUEST</div>', unsafe_allow_html=True)

        with head_col2:
            p_col1, p_col2 = st.columns([1, 2])
            with p_col1:
                if data['photo']:
                    st.image(data['photo'], width=85)
                else:
                    st.markdown('<div style="width:80px;height:80px;background:#e2d2c0;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:30px;">👤</div>', unsafe_allow_html=True)
            with p_col2:
                st.markdown(f"""
                <div class="emp-label">Employee Profile</div>
                <div class="emp-name">{data['employee_name']}</div>
                <div class="emp-title">{data['job_title']}</div>
                <div class="emp-resign-date">Resigning {r_date_header}</div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Resignation Journey Title
        st.markdown('<div style="color:#000; font-weight:800; font-size:18px; margin-bottom:8px;">Resignation Journey</div>', unsafe_allow_html=True)
        
        # 5 Journey Items
        j1, j2, j3, j4, j5 = st.columns(5)
        with j1:
            st.markdown(f'<div class="journey-item"><div class="journey-icon">👤</div><div class="journey-title">Joined</div><div class="journey-val">{h_date}</div></div>', unsafe_allow_html=True)
        with j2:
            st.markdown(f'<div class="journey-item"><div class="journey-icon">🏆</div><div class="journey-title">Total Experience</div><div class="journey-val">{data["exp_days"]} Days</div></div>', unsafe_allow_html=True)
        with j3:
            st.markdown(f'<div class="journey-item"><div class="journey-icon">📄</div><div class="journey-title">Resignation Letter Submitted</div><div class="journey-val">{r_date}</div></div>', unsafe_allow_html=True)
        with j4:
            st.markdown(f'<div class="journey-item"><div class="journey-icon">🕒</div><div class="journey-title">Notice Period Status</div><div class="journey-val">{data["notice_period"]}</div></div>', unsafe_allow_html=True)
        with j5:
            st.markdown(f'<div class="journey-item"><div class="journey-icon">✅</div><div class="journey-title">Resignation Process Finalized</div><div class="journey-val">Approved<br>{r_date}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 4 Metric Pills
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-header">Total Net Pay (EGP)</div><div class="metric-body">{data["net_pay"]}</div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-header">Last Working Day</div><div class="metric-body">{l_date}</div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-header">Reason for Leaving</div><div class="metric-body">{data["reason"]}</div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-header">Direct Manager</div><div class="metric-body">{data["direct_manager"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Data Table
        table_html = f"""
        <table class="custom-table">
            <thead>
                <tr>
                    <th style="width: 40%;">Field</th>
                    <th style="width: 60%;">Value</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Employee Name</td><td><b>{data['employee_name']}</b></td></tr>
                <tr><td>Branch</td><td>{data['branch']}</td></tr>
                <tr><td>Job Title</td><td>{data['job_title']}</td></tr>
                <tr><td>Hiring Date</td><td>{h_date}</td></tr>
                <tr><td>Resignation Date</td><td>{r_date}</td></tr>
                <tr><td>Last Working Day</td><td>{l_date}</td></tr>
                <tr><td>Grading System</td><td>{data['grading']}</td></tr>
                <tr><td>Total Net to pay EGP</td><td><b>{data['net_pay']}</b></td></tr>
                <tr><td>Reason for Leaving</td><td>{data['reason']}</td></tr>
                <tr><td>Notice Period Status</td><td>{data['notice_period']}</td></tr>
                <tr><td>Handover Status</td><td>{data['handover_status']}</td></tr>
                <tr><td>Total Experience</td><td>{data['exp_days']} Day</td></tr>
                <tr><td>Direct Manager</td><td>{data['direct_manager']}</td></tr>
                <tr><td>Absence during the year</td><td>{data['absence_days']} Day</td></tr>
                <tr><td>Loan balance</td><td>{data['loan_balance']} EGP</td></tr>
            </tbody>
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)

        # Manager Action Items
        st.markdown(f"""
        <div class="action-box">
            <div class="action-title">MANAGER ACTION ITEMS</div>
            <div class="action-subtitle">Resignation Next Steps</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 13px;">
                <div>🧮 Calculate final dues and payout. Ensure 'Total Net to pay {data['net_pay']} EGP' is correct.</div>
                <div>🤝 Facilitate handover process with {data['handover_status']} and new point of contact.</div>
                <div>🕒 Review notice period waiver request ({data['notice_period']}).</div>
                <div>📦 Schedule property return (laptop, badge, keys).</div>
                <div>📑 Issue final acceptance letter and experience certificate.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Email Options
        with st.expander("📧 Email this Template"):
            recv_email = st.text_input("Recipient Email Address")
            sender_email = st.text_input("Sender Email Address")
            sender_pwd = st.text_input("Sender App Password", type="password")
            if st.button("Send Resignation Email"):
                if recv_email and sender_email and sender_pwd:
                    try:
                        msg = MIMEMultipart('alternative')
                        msg['Subject'] = f"Resignation Approval Request - {data['employee_name']}"
                        msg['From'] = sender_email
                        msg['To'] = recv_email
                        
                        email_html = f"""
                        <html>
                        <body style="font-family: Arial; background:#F8F6F0; padding:20px;">
                            <div style="background:#FAF8F5; border:1px solid #D6C2A7; padding:20px; border-radius:10px;">
                                <h2 style="color:#8C5A2B;">RESIGNATION APPROVAL REQUEST</h2>
                                <p><b>Employee:</b> {data['employee_name']}</p>
                                <p><b>Branch:</b> {data['branch']}</p>
                                <p><b>Job Title:</b> {data['job_title']}</p>
                                <p><b>Resignation Date:</b> {r_date}</p>
                                <p><b>Last Working Day:</b> {l_date}</p>
                                <p><b>Net Pay:</b> {data['net_pay']} EGP</p>
                                <p><b>Manager:</b> {data['direct_manager']}</p>
                            </div>
                        </body>
                        </html>
                        """
                        msg.attach(MIMEText(email_html, 'html'))
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(sender_email, sender_pwd)
                        server.sendmail(sender_email, recv_email, msg.as_string())
                        server.quit()
                        st.success("Email sent successfully!")
                    except Exception as e:
                        st.error(f"Failed to send email: {e}")
                else:
                    st.error("Please fill in all email fields.")

# ---------------------------------------------------------
# PAGE 3: DASHBOARD & BRANCH ANALYTICS
# ---------------------------------------------------------
elif page == "📊 Branches & Resignations Dashboard":
    st.title("📊 Branches & Resignations Analytics")

    if not st.session_state.resignations_db:
        st.info("No resignations registered yet.")
    else:
        df = pd.DataFrame(st.session_state.resignations_db)

        # Overview Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Resignations", len(df))
        m2.metric("Total Branches Affected", df['branch'].nunique())
        m3.metric("Total Payout Dues (EGP)", f"{df['net_pay'].sum():,}")
        m4.metric("Avg Experience (Days)", f"{int(df['exp_days'].mean())} Days")

        st.markdown("---")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🏢 Resignations Count by Branch")
            branch_counts = df['branch'].value_counts().reset_index()
            branch_counts.columns = ['Branch', 'Resignation Count']
            st.dataframe(branch_counts, use_container_width=True)

        with col2:
            st.subheader("💡 Reasons Breakdown")
            reason_counts = df['reason'].value_counts().reset_index()
            reason_counts.columns = ['Reason', 'Count']
            st.dataframe(reason_counts, use_container_width=True)

        st.markdown("---")
        st.subheader("🔍 Search & Log Records (Newest to Oldest)")

        search_query = st.text_input("Search by Employee Name, Branch, or Manager:").strip()

        df_display = df.copy()
        if search_query:
            df_display = df_display[
                df_display['employee_name'].str.contains(search_query, case=False, na=False) |
                df_display['branch'].str.contains(search_query, case=False, na=False) |
                df_display['direct_manager'].str.contains(search_query, case=False, na=False)
            ]

        # Selected columns for tabular presentation
        show_cols = ['employee_name', 'branch', 'job_title', 'resignation_date', 'last_working_day', 'net_pay', 'reason', 'direct_manager']
        st.dataframe(df_display[show_cols], use_container_width=True)

        # CSV Download
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Resignations Log to CSV", data=csv, file_name="resignations_master_log.csv", mime="text/csv")
