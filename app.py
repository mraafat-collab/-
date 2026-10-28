import streamlit as st
import pandas as pd
from datetime import date
import streamlit.components.v1 as components
import base64
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from docx import Document

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Resignation Approval System",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------------
# Custom CSS for Top Navigation Tabs
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8F6F0;
    }
    .stApp {
        background-color: #F8F6F0;
    }

    /* Glowing Rectangular Top Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        padding-bottom: 12px;
        border-bottom: 2px solid #EADBCE;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        background-color: #FFFFFF;
        border-radius: 8px;
        color: #8C5A2B;
        font-weight: 700;
        font-size: 15px;
        border: 1.5px solid #D6C2A7;
        padding: 0px 22px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.03);
        transition: all 0.2s ease-in-out;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #8C5A2B;
        color: #8C5A2B;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #8C5A2B !important;
        color: #FFFFFF !important;
        border-color: #8C5A2B !important;
        box-shadow: 0px 4px 12px rgba(140, 90, 43, 0.4) !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Helper Function
def to_english_str(text):
    if not text:
        return ""
    arabic_num = "٠١٢٣٤٥٦٧٨٩"
    english_num = "0123456789"
    trans = str.maketrans(arabic_num, english_num)
    return str(text).translate(trans)

# Helper for Word (.docx)
def generate_word_doc(data, exp_days):
    doc = Document()
    doc.add_heading(f"RESIGNATION APPROVAL REQUEST - {data['employee_name']}", 0)
    
    doc.add_paragraph(f"Recipient: Dear {data.get('recipient_name', 'Manager')}")
    doc.add_paragraph(f"Employee Name: {data['employee_name']}")
    doc.add_paragraph(f"Job Title: {data['job_title']}")
    doc.add_paragraph(f"Branch: {data['branch']}")
    doc.add_paragraph(f"Hiring Date: {data['hiring_date'].strftime('%d/%m/%Y')}")
    doc.add_paragraph(f"Resignation Date: {data['resignation_date'].strftime('%d/%m/%Y')}")
    doc.add_paragraph(f"Last Working Day: {data['last_working_day'].strftime('%d/%m/%Y')}")
    doc.add_paragraph(f"Total Experience: {exp_days} Days")
    doc.add_paragraph(f"Total Net Pay: {data['net_pay']} EGP")
    doc.add_paragraph(f"Reason for Leaving: {data['reason']}")
    doc.add_paragraph(f"Direct Manager: {data['direct_manager']}")
    doc.add_paragraph(f"Notice Period Status: {data['notice_period']}")
    doc.add_paragraph(f"Handover Status: {data['handover_status']}")
    
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# Helper for Excel (.xlsx)
def generate_excel(data, exp_days):
    df_single = pd.DataFrame([{
        "Recipient Name": data.get('recipient_name', ''),
        "Employee Name": data['employee_name'],
        "Branch": data['branch'],
        "Job Title": data['job_title'],
        "Hiring Date": data['hiring_date'].strftime('%Y-%m-%d'),
        "Resignation Date": data['resignation_date'].strftime('%Y-%m-%d'),
        "Last Working Day": data['last_working_day'].strftime('%Y-%m-%d'),
        "Total Experience (Days)": exp_days,
        "Grading System": data['grading'],
        "Total Net Pay (EGP)": data['net_pay'],
        "Reason": data['reason'],
        "Notice Period Status": data['notice_period'],
        "Handover Status": data['handover_status'],
        "Direct Manager": data['direct_manager'],
        "Absence Days": data['absence_days'],
        "Loan Balance EGP": data['loan_balance']
    }])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_single.to_excel(writer, index=False, sheet_name='Resignation')
    return output.getvalue()

# Database Initialization
if 'resignations_db' not in st.session_state:
    st.session_state.resignations_db = [
        {
            "id": 1,
            "recipient_name": "Mohamed",
            "employee_name": "Abu Bakr Muhammad Mahmoud",
            "job_title": "Sales Casual",
            "branch": "Park-St Branch",
            "grading": "G1 - L1",
            "hiring_date": date(2026, 10, 3),
            "resignation_date": date(2026, 10, 20),
            "last_working_day": date(2026, 10, 20),
            "net_pay": 7000,
            "reason": "Education",
            "direct_manager": "Sherif S. El-Sayed",
            "notice_period": "One Month",
            "handover_status": "Team Leader",
            "absence_days": 0,
            "loan_balance": 0,
            "photo_b64": None
        }
    ]

# ---------------------------------------------------------
# Top Navigation Bar
# ---------------------------------------------------------
tab_main, tab_manage, tab_dashboard = st.tabs([
    "🏠 عرض وطباعة الاستقالة (A4)", 
    "📝 إضافة / تعديل / حذف استقالة", 
    "📊 داشبورد الفروع"
])

# ---------------------------------------------------------
# TAB 1: DISPLAY & EXPORT A4 TEMPLATE
# ---------------------------------------------------------
with tab_main:
    if not st.session_state.resignations_db:
        st.warning("⚠️ لا توجد بيانات استقالات مسجلة حالياً.")
    else:
        emp_options = {r['id']: f"{r['employee_name']} — ({r['branch']})" for r in st.session_state.resignations_db}
        selected_id = st.selectbox("اختر الموظف لعرض طلب الاستقالة الخاصة به:", options=list(emp_options.keys()), format_func=lambda x: emp_options[x])

        data = next(item for item in st.session_state.resignations_db if item["id"] == selected_id)

        exp_days = (data['last_working_day'] - data['hiring_date']).days
        if exp_days < 0:
            exp_days = 0

        h_date = data['hiring_date'].strftime("%d/%m/%Y")
        r_date = data['resignation_date'].strftime("%d/%m/%Y")
        l_date = data['last_working_day'].strftime("%d/%m/%Y")
        r_date_header = data['resignation_date'].strftime("%d %b %Y")
        
        recipient = data.get('recipient_name', '').strip()
        if not recipient:
            recipient = "Mohamed"
        if not recipient.lower().startswith("mr.") and not recipient.lower().startswith("ms."):
            recipient_title = f"Mr. {recipient}"
        else:
            recipient_title = recipient

        # Export Toolbar
        st.markdown("#### 📥 خيارات الحفظ والتصدير [Export & Save Options]:")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            word_bytes = generate_word_doc(data, exp_days)
            st.download_button(
                label="📄 حفظ كملف Word (.docx)",
                data=word_bytes,
                file_name=f"Resignation_{data['employee_name']}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            
        with col_btn2:
            excel_bytes = generate_excel(data, exp_days)
            st.download_button(
                label="📊 حفظ كملف Excel (.xlsx)",
                data=excel_bytes,
                file_name=f"Resignation_{data['employee_name']}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        st.markdown("---")

        if data.get('photo_b64'):
            img_html = f'<img src="data:image/png;base64,{data["photo_b64"]}" style="width:105px; height:140px; border-radius:8px; object-fit:cover; border:1px solid #D6C2A7;" />'
        else:
            img_html = '<div style="width:105px; height:140px; background:#EADBCE; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:42px; border:1px solid #D6C2A7;">👤</div>'

        # Dynamic Render with html2canvas Image Generator & PDF Print Engine
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
                body {{
                    font-family: 'Inter', sans-serif;
                    background-color: #F8F6F0;
                    margin: 0;
                    padding: 10px;
                }}
                .btn-group {{
                    display: flex;
                    gap: 10px;
                    justify-content: flex-end;
                    margin-bottom: 15px;
                }}
                .action-btn {{
                    background-color: #8C5A2B;
                    color: white;
                    border: none;
                    padding: 11px 20px;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 13px;
                    cursor: pointer;
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    box-shadow: 0px 3px 8px rgba(140, 90, 43, 0.3);
                }}
                .action-btn:hover {{ background-color: #704721; }}
                .a4-card {{
                    background-color: #FAF8F5;
                    border: 1.5px solid #D6C2A7;
                    border-radius: 12px;
                    padding: 22px;
                    max-width: 800px;
                    margin: 0 auto;
                    box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
                }}
                .custom-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                    border: 1px solid #D6C2A7;
                }}
                .custom-table th {{
                    background-color: #8C5A2B;
                    color: white;
                    padding: 6px 10px;
                    text-align: left;
                    font-size: 12px;
                    font-weight: 700;
                }}
                .custom-table td {{
                    padding: 5px 10px;
                    border-bottom: 1px solid #EADBCE;
                    font-size: 12px;
                    color: #222;
                }}
                .custom-table tr:nth-child(even) {{ background-color: #FAF8F5; }}
                .metric-badge {{
                    background-color: #8C5A2B;
                    color: white;
                    border-radius: 14px;
                    padding: 5px 8px;
                    text-align: center;
                    font-weight: 700;
                    font-size: 11px;
                    margin-bottom: 4px;
                }}
                .metric-box {{
                    background-color: #FAF8F5;
                    border: 1px solid #D6C2A7;
                    border-radius: 6px;
                    padding: 6px;
                    text-align: center;
                    font-weight: 800;
                    font-size: 13px;
                    color: #111;
                }}
                @media print {{
                    .no-print {{ display: none !important; }}
                    body {{ background: white; padding: 0; }}
                    .a4-card {{ border: none; box-shadow: none; width: 100%; max-width: 100%; padding: 0; }}
                }}
            </style>
        </head>
        <body>
            <div class="btn-group no-print">
                <button onclick="downloadAsImage()" class="action-btn">🖼️ تنزيل كصورة (PNG)</button>
                <button onclick="window.print()" class="action-btn">🖨️ طباعة / حفظ كـ PDF</button>
            </div>

            <div id="capture-card" class="a4-card">
                <table style="width:100%; border:none; margin-bottom:12px;">
                    <tr>
                        <td style="width:55%; vertical-align:top; border:none;">
                            <div style="color:#8C5A2B; font-size:16px; font-weight:700; margin-bottom:4px;">Dear {recipient_title},</div>
                            <div style="color:#8C5A2B; font-weight:800; font-size:24px; line-height:1.1;">RESIGNATION<br>APPROVAL REQUEST</div>
                        </td>
                        <td style="width:45%; vertical-align:top; border:none;">
                            <div style="background:#FAF8F5; border:1px solid #D6C2A7; border-radius:10px; padding:10px; display:flex; gap:12px; align-items:center;">
                                {img_html}
                                <div>
                                    <div style="font-size:10px; text-transform:uppercase; color:#8C5A2B; font-weight:800; letter-spacing:0.5px;">EMPLOYEE PROFILE</div>
                                    <div style="font-size:16px; font-weight:800; color:#111; margin:3px 0;">{data['employee_name']}</div>
                                    <div style="font-size:12px; color:#444;">{data['job_title']}</div>
                                    <div style="font-size:11px; color:#666; margin-top:4px;">Resigning {r_date_header}</div>
                                </div>
                            </div>
                        </td>
                    </tr>
                </table>

                <div style="color:#000; font-weight:800; font-size:14px; margin-top:6px; margin-bottom:6px;">Resignation Journey</div>
                
                <div style="display:flex; gap:6px; text-align:center;">
                    <div style="flex:1; border:1px solid #D6C2A7; border-radius:8px; padding:6px;"><div style="background:#8C5A2B; color:white; border-radius:50%; width:22px; height:22px; margin:auto; font-size:10px; display:flex; align-items:center; justify-content:center;">👤</div><div style="font-size:10px; font-weight:700; margin-top:2px;">Joined</div><div style="font-size:11px;">{h_date}</div></div>
                    <div style="flex:1; border:1px solid #D6C2A7; border-radius:8px; padding:6px;"><div style="background:#8C5A2B; color:white; border-radius:50%; width:22px; height:22px; margin:auto; font-size:10px; display:flex; align-items:center; justify-content:center;">🏆</div><div style="font-size:10px; font-weight:700; margin-top:2px;">Total Experience</div><div style="font-size:11px;">{exp_days} Days</div></div>
                    <div style="flex:1; border:1px solid #D6C2A7; border-radius:8px; padding:6px;"><div style="background:#8C5A2B; color:white; border-radius:50%; width:22px; height:22px; margin:auto; font-size:10px; display:flex; align-items:center; justify-content:center;">📄</div><div style="font-size:10px; font-weight:700; margin-top:2px;">Submitted</div><div style="font-size:11px;">{r_date}</div></div>
                    <div style="flex:1; border:1px solid #D6C2A7; border-radius:8px; padding:6px;"><div style="background:#8C5A2B; color:white; border-radius:50%; width:22px; height:22px; margin:auto; font-size:10px; display:flex; align-items:center; justify-content:center;">🕒</div><div style="font-size:10px; font-weight:700; margin-top:2px;">Notice Period</div><div style="font-size:11px;">{data["notice_period"]}</div></div>
                    <div style="flex:1; border:1px solid #D6C2A7; border-radius:8px; padding:6px;"><div style="background:#8C5A2B; color:white; border-radius:50%; width:22px; height:22px; margin:auto; font-size:10px; display:flex; align-items:center; justify-content:center;">✅</div><div style="font-size:10px; font-weight:700; margin-top:2px;">Finalized</div><div style="font-size:11px;">Approved {r_date}</div></div>
                </div>

                <div style="display:flex; gap:8px; margin-top:10px;">
                    <div style="flex:1;"><div class="metric-badge">Total Net Pay (EGP)</div><div class="metric-box">{data["net_pay"]}</div></div>
                    <div style="flex:1;"><div class="metric-badge">Last Working Day</div><div class="metric-box">{l_date}</div></div>
                    <div style="flex:1;"><div class="metric-badge">Reason for Leaving</div><div class="metric-box">{data["reason"]}</div></div>
                    <div style="flex:1;"><div class="metric-badge">Direct Manager</div><div class="metric-box">{data["direct_manager"]}</div></div>
                </div>

                <table class="custom-table">
                    <thead>
                        <tr><th style="width:40%;">Field</th><th style="width:60%;">Value</th></tr>
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
                        <tr><td>Total Experience</td><td>{exp_days} Day</td></tr>
                        <tr><td>Direct Manager</td><td>{data['direct_manager']}</td></tr>
                        <tr><td>Absence during the year</td><td>{data['absence_days']} Day</td></tr>
                        <tr><td>Loan balance</td><td>{data['loan_balance']} EGP</td></tr>
                    </tbody>
                </table>

                <div style="background:#FAF8F5; border:1px solid #D6C2A7; border-radius:8px; padding:10px; margin-top:10px;">
                    <div style="color:#8C5A2B; font-weight:800; font-size:13px;">MANAGER ACTION ITEMS</div>
                    <div style="color:#8C5A2B; font-weight:700; font-size:11px; margin-bottom:6px;">Resignation Next Steps</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:11px;">
                        <div>🧮 Calculate final dues payout ({data['net_pay']} EGP).</div>
                        <div>🤝 Facilitate handover process with {data['handover_status']}.</div>
                        <div>🕒 Review notice period waiver request ({data['notice_period']}).</div>
                        <div>📦 Schedule property return (laptop, badge, keys).</div>
                    </div>
                </div>
            </div>

            <script>
                function downloadAsImage() {{
                    const element = document.getElementById("capture-card");
                    html2canvas(element, {{ scale: 2 }}).then(canvas => {{
                        const link = document.createElement("a");
                        link.download = "Resignation_{data['employee_name']}.png";
                        link.href = canvas.toDataURL("image/png");
                        link.click();
                    }});
                }}
            </script>
        </body>
        </html>
        """
        components.html(html_content, height=940, scrolling=True)

        # EMAIL TEMPLATE SECTION
        with st.expander("📧 إرسال / نسخ قالب الإيميل (Email Options)"):
            c_e1, c_e2 = st.columns(2)
            with c_e1:
                sender = st.text_input("بريد المرسل (Sender Email)")
                pwd = st.text_input("كلمة مرور التطبيق (App Password)", type="password")
            with c_e2:
                receiver = st.text_input("بريد المستلم (Receiver Email)")
                smtp_host = st.text_input("سيرفر SMTP", value="smtp.gmail.com")

            if st.button("🚀 إرسال التقرير مباشرة بالإيميل"):
                if sender and pwd and receiver:
                    try:
                        msg = MIMEMultipart('alternative')
                        msg['Subject'] = f"Resignation Approval Request - {data['employee_name']}"
                        msg['From'] = sender
                        msg['To'] = receiver
                        
                        email_html = f"""
                        <html>
                        <body style="font-family: Arial, sans-serif; background-color: #F8F6F0; padding: 20px;">
                            <div style="background-color: #FAF8F5; border: 1px solid #D6C2A7; padding: 20px; border-radius: 10px; max-width: 600px; margin: auto;">
                                <h3 style="color: #8C5A2B;">Dear {recipient_title},</h3>
                                <h2 style="color: #8C5A2B;">RESIGNATION APPROVAL REQUEST</h2>
                                <hr style="border: 1px solid #EADBCE;">
                                <p><b>Employee Name:</b> {data['employee_name']}</p>
                                <p><b>Branch:</b> {data['branch']}</p>
                                <p><b>Job Title:</b> {data['job_title']}</p>
                                <p><b>Hiring Date:</b> {h_date}</p>
                                <p><b>Last Working Day:</b> {l_date}</p>
                                <p><b>Total Experience:</b> {exp_days} Days</p>
                                <p><b>Total Net Pay:</b> {data['net_pay']} EGP</p>
                                <p><b>Reason for Leaving:</b> {data['reason']}</p>
                                <p><b>Direct Manager:</b> {data['direct_manager']}</p>
                            </div>
                        </body>
                        </html>
                        """
                        msg.attach(MIMEText(email_html, 'html'))
                        server = smtplib.SMTP(smtp_host, 587)
                        server.starttls()
                        server.login(sender, pwd)
                        server.sendmail(sender, receiver, msg.as_string())
                        server.quit()
                        st.success("✅ تم إرسال الإيميل بنجاح!")
                    except Exception as e:
                        st.error(f"❌ فشل إرسال الإيميل: {e}")
                else:
                    st.error("يرجى ملء جميع بيانات الإيميل.")

# ---------------------------------------------------------
# TAB 2: EDIT & MANAGE RESIGNATIONS
# ---------------------------------------------------------
with tab_manage:
    st.subheader("⚙️ إدارة تسجيلات الاستقالات")

    action_type = st.radio("اختر نوع الإجراء المطلوب:", ["إضافة استقالة جديدة ➕", "تعديل بيانات استقالة ✏️", "حذف استقالة 🗑️"], horizontal=True)

    if action_type == "حذف استقالة 🗑️":
        if not st.session_state.resignations_db:
            st.warning("لا توجد استقالات مسجلة لحذفها.")
        else:
            del_options = {r['id']: f"{r['employee_name']} — ({r['branch']})" for r in st.session_state.resignations_db}
            del_id = st.selectbox("اختر الاستقالة المراد حذفها نهائياً:", options=list(del_options.keys()), format_func=lambda x: del_options[x])
            
            if st.button("❌ تأكيد الحذف النهائي", type="primary"):
                st.session_state.resignations_db = [r for r in st.session_state.resignations_db if r['id'] != del_id]
                st.success("✅ تم حذف الاستقالة بنجاح!")
                st.rerun()

    else:
        if action_type == "تعديل بيانات استقالة ✏️" and st.session_state.resignations_db:
            edit_options = {r['id']: f"{r['employee_name']} — ({r['branch']})" for r in st.session_state.resignations_db}
            edit_id = st.selectbox("اختر الموظف المراد تعديل بياناته:", options=list(edit_options.keys()), format_func=lambda x: edit_options[x])
            target_data = next(item for item in st.session_state.resignations_db if item["id"] == edit_id)
        else:
            target_data = {
                "id": None,
                "recipient_name": "",
                "employee_name": "",
                "job_title": "",
                "branch": "",
                "grading": "",
                "hiring_date": date.today(),
                "resignation_date": date.today(),
                "last_working_day": date.today(),
                "net_pay": 0,
                "reason": "",
                "direct_manager": "",
                "notice_period": "",
                "handover_status": "",
                "absence_days": 0,
                "loan_balance": 0,
                "photo_b64": None
            }

        with st.form("resignation_form"):
            st.markdown("##### 📩 بيانات الموجه إليه الطلب والمدير المباشر")
            col_rec1, col_rec2 = st.columns(2)
            with col_rec1:
                recipient_input = to_english_str(st.text_input("اسم المرسل إليه / الموجه له الطلب (Recipient Name)", value=target_data.get('recipient_name', '')))
            with col_rec2:
                direct_manager = to_english_str(st.text_input("المدير المباشر (Direct Manager)", value=target_data['direct_manager']))

            st.markdown("---")
            st.markdown("##### 👤 بيانات الموظف والوظيفة")
            col1, col2 = st.columns(2)
            
            with col1:
                emp_name = to_english_str(st.text_input("اسم الموظف (Employee Name)", value=target_data['employee_name']))
                job_title = to_english_str(st.text_input("المسمى الوظيفي (Job Title)", value=target_data['job_title']))
                branch = to_english_str(st.text_input("اسم الفرع (Branch)", value=target_data['branch']))
                grading = to_english_str(st.text_input("الدرجة الوظيفية (Grading System)", value=target_data['grading']))
                reason = to_english_str(st.text_input("سبب الاستقالة (Reason for Leaving)", value=target_data['reason']))
                
            with col2:
                hiring_date = st.date_input("تاريخ التعيين (Hiring Date)", value=target_data['hiring_date'])
                resignation_date = st.date_input("تاريخ تقديم الاستقالة (Resignation Date)", value=target_data['resignation_date'])
                last_working_day = st.date_input("آخر يوم عمل (Last Working Day)", value=target_data['last_working_day'])
                
                calc_exp = (last_working_day - hiring_date).days
                if calc_exp < 0:
                    calc_exp = 0
                st.info(f"🏆 إجمالي الخبرة (Total Experience): **{calc_exp} Days** (تحسب تلقائياً من تاريخ التعيين وآخر يوم عمل)")
                
                net_pay = st.number_input("إجمالي المستحقات (Total Net Pay EGP)", value=int(target_data['net_pay']), step=500)
                notice_period = to_english_str(st.text_input("فترة الإشعار (Notice Period Status)", value=target_data['notice_period']))
                handover_status = to_english_str(st.text_input("حالة التسليم (Handover Status)", value=target_data['handover_status']))

            col3, col4 = st.columns(2)
            with col3:
                absence_days = st.number_input("أيام الغياب (Absence Days)", value=int(target_data['absence_days']))
                loan_balance = st.number_input("رصيد السلفة (Loan Balance EGP)", value=int(target_data['loan_balance']))
            with col4:
                uploaded_photo = st.file_uploader("🖼️ رفع صورة شخصية للموظف (Upload Photo 4x6)", type=["png", "jpg", "jpeg"])

            save_btn = st.form_submit_button("💾 حفظ البيانات والتحديث", type="primary")

            if save_btn:
                if uploaded_photo is not None:
                    photo_b64 = base64.b64encode(uploaded_photo.getvalue()).decode()
                else:
                    photo_b64 = target_data.get('photo_b64')

                new_id = target_data['id'] if target_data['id'] else (max([r['id'] for r in st.session_state.resignations_db], default=0) + 1)
                
                updated_record = {
                    "id": new_id,
                    "recipient_name": recipient_input,
                    "employee_name": emp_name if emp_name else "Unnamed Employee",
                    "job_title": job_title,
                    "branch": branch,
                    "grading": grading,
                    "hiring_date": hiring_date,
                    "resignation_date": resignation_date,
                    "last_working_day": last_working_day,
                    "net_pay": net_pay,
                    "reason": reason,
                    "direct_manager": direct_manager,
                    "notice_period": notice_period,
                    "handover_status": handover_status,
                    "absence_days": absence_days,
                    "loan_balance": loan_balance,
                    "photo_b64": photo_b64
                }

                if action_type == "تعديل بيانات استقالة ✏️" and target_data['id']:
                    idx = next(i for i, item in enumerate(st.session_state.resignations_db) if item["id"] == target_data['id'])
                    st.session_state.resignations_db[idx] = updated_record
                    st.success("✅ تم حفظ التعديلات بنجاح!")
                else:
                    st.session_state.resignations_db.insert(0, updated_record)
                    st.success("✅ تم تسجيل الاستقالة بنجاح!")
                
                st.rerun()

# ---------------------------------------------------------
# TAB 3: DASHBOARD
# ---------------------------------------------------------
with tab_dashboard:
    st.title("📊 داشبورد تحليل استقالات الفروع")

    if not st.session_state.resignations_db:
        st.info("لا توجد استقالات مسجلة.")
    else:
        records = []
        for r in st.session_state.resignations_db:
            exp = (r['last_working_day'] - r['hiring_date']).days
            if exp < 0:
                exp = 0
            records.append({
                "المرسل إليه": r.get('recipient_name', ''),
                "اسم الموظف": r['employee_name'],
                "الفرع": r['branch'],
                "المسمى الوظيفي": r['job_title'],
                "تاريخ التعيين": r['hiring_date'].strftime("%Y-%m-%d"),
                "آخر يوم عمل": r['last_working_day'].strftime("%Y-%m-%d"),
                "إجمالي الخبرة (يوم)": exp,
                "إجمالي المستحقات (EGP)": r['net_pay'],
                "سبب الاستقالة": r['reason'],
                "المدير المباشر": r['direct_manager']
            })
        
        df = pd.DataFrame(records)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("إجمالي الاستقالات", len(df))
        m2.metric("عدد الفروع", df['الفرع'].nunique())
        m3.metric("إجمالي المستحقات (EGP)", f"{df['إجمالي المستحقات (EGP)'].sum():,}")
        m4.metric("متوسط الخبرة (يوم)", f"{int(df['إجمالي الخبرة (يوم)'].mean())} يوم")

        st.markdown("---")

        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("🏢 توزيع الاستقالات حسب الفرع")
            b_df = df['الفرع'].value_counts().reset_index()
            b_df.columns = ['اسم الفرع', 'عدد الاستقالات']
            st.dataframe(b_df, use_container_width=True)
            st.bar_chart(data=b_df.set_index('اسم الفرع'))

        with c2:
            st.subheader("💡 الأسباب الأكثر شيوعاً")
            r_df = df['سبب الاستقالة'].value_counts().reset_index()
            r_df.columns = ['السبب', 'العدد']
            st.dataframe(r_df, use_container_width=True)

        st.markdown("---")
        st.subheader("🔍 البحث والتصدير")
        q = st.text_input("ابحث باسم الموظف أو الفرع:").strip()
        filtered = df[df['اسم الموظف'].str.contains(q, case=False, na=False) | df['الفرع'].str.contains(q, case=False, na=False)] if q else df
        st.dataframe(filtered, use_container_width=True)

        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 تصدير سجل الاستقالات كملف CSV", data=csv, file_name="resignations_master_log.csv", mime="text/csv")
