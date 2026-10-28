import streamlit as st
import pandas as pd
from datetime import date, datetime
import base64

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Resignation Approval System",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------------
# Custom CSS (Matching Image Colors & Printable A4 Template)
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
    
    /* Top Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #EADBCE;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #FAF8F5;
        border-radius: 8px;
        color: #8C5A2B;
        font-weight: 700;
        border: 1px solid #D6C2A7;
    }
    .stTabs [aria-selected="true"] {
        background-color: #8C5A2B !important;
        color: white !important;
    }

    /* Print & A4 Setup */
    @media print {
        @page {
            size: A4 portrait;
            margin: 10mm;
        }
        body * {
            visibility: hidden;
        }
        #printable-a4, #printable-a4 * {
            visibility: visible;
        }
        #printable-a4 {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            border: none !important;
            box-shadow: none !important;
        }
        .no-print {
            display: none !important;
        }
    }

    /* A4 Container Box */
    .a4-container {
        background-color: #FAF8F5;
        border: 1.5px solid #D6C2A7;
        border-radius: 14px;
        padding: 24px;
        margin: 0 auto;
        max-width: 800px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Header Typography */
    .req-subtitle {
        color: #8C5A2B;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .req-title {
        color: #8C5A2B;
        font-weight: 800;
        font-size: 24px;
        line-height: 1.1;
    }
    .emp-label {
        font-size: 10px;
        text-transform: uppercase;
        color: #8C5A2B;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    .emp-name {
        font-size: 17px;
        font-weight: 800;
        color: #111;
        margin: 2px 0;
    }
    .emp-title {
        font-size: 13px;
        color: #444;
    }
    .emp-resign-date {
        font-size: 11px;
        color: #666;
        margin-top: 2px;
    }

    /* Journey Box */
    .journey-flex {
        display: flex;
        justify-content: space-between;
        gap: 6px;
        margin-top: 10px;
    }
    .journey-item {
        background-color: #FAF8F5;
        border: 1px solid #D6C2A7;
        border-radius: 8px;
        padding: 8px 4px;
        text-align: center;
        flex: 1;
    }
    .journey-icon {
        background-color: #8C5A2B;
        color: white;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        margin: 0 auto 4px auto;
    }
    .journey-title {
        font-size: 10px;
        font-weight: 700;
        color: #111;
    }
    .journey-val {
        font-size: 11px;
        color: #333;
    }

    /* Metrics Pills */
    .metrics-flex {
        display: flex;
        gap: 8px;
        margin-top: 12px;
    }
    .metric-col {
        flex: 1;
    }
    .metric-header {
        background-color: #8C5A2B;
        color: white;
        border-radius: 14px;
        padding: 5px 8px;
        text-align: center;
        font-weight: 700;
        font-size: 11px;
        margin-bottom: 4px;
    }
    .metric-body {
        background-color: #FAF8F5;
        border: 1px solid #D6C2A7;
        border-radius: 6px;
        padding: 6px;
        text-align: center;
        font-weight: 800;
        font-size: 13px;
        color: #111;
    }

    /* Custom Table */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 12px;
        border: 1px solid #D6C2A7;
    }
    .custom-table th {
        background-color: #8C5A2B;
        color: white;
        padding: 6px 10px;
        text-align: left;
        font-size: 12px;
        font-weight: 700;
    }
    .custom-table td {
        padding: 5px 10px;
        border-bottom: 1px solid #EADBCE;
        font-size: 12px;
        color: #222;
    }
    .custom-table tr:nth-child(even) {
        background-color: #FAF8F5;
    }

    /* Action Box */
    .action-box {
        background-color: #FAF8F5;
        border: 1px solid #D6C2A7;
        border-radius: 8px;
        padding: 12px;
        margin-top: 12px;
    }
    .action-title {
        color: #8C5A2B;
        font-weight: 800;
        font-size: 14px;
    }
    .action-subtitle {
        color: #8C5A2B;
        font-weight: 700;
        font-size: 12px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def to_english_str(text):
    if not text:
        return ""
    arabic_num = "٠١٢٣٤٥٦٧٨٩"
    english_num = "0123456789"
    trans = str.maketrans(arabic_num, english_num)
    return str(text).translate(trans)

# Database Initialization
if 'resignations_db' not in st.session_state:
    st.session_state.resignations_db = [
        {
            "id": 1,
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
            "photo": None
        }
    ]

# ---------------------------------------------------------
# Top Navigation Bar
# ---------------------------------------------------------
tab_main, tab_manage, tab_dashboard = st.tabs([
    "🏠 عرض وطباعة طلب الاستقالة (A4)", 
    "📝 إضافة / تعديل / حذف استقالة", 
    "📊 داشبورد الفروع"
])

# ---------------------------------------------------------
# TAB 1: DISPLAY & PRINT A4 PAGE
# ---------------------------------------------------------
with tab_main:
    if not st.session_state.resignations_db:
        st.info("لا توجد استقالات مسجلة حالياً.")
    else:
        top_col1, top_col2 = st.columns([3, 1])
        with top_col1:
            emp_options = {r['id']: f"{r['employee_name']} — ({r['branch']})" for r in st.session_state.resignations_db}
            selected_id = st.selectbox("اختر الموظف لعرض طلب الاستقالة:", options=list(emp_options.keys()), format_func=lambda x: emp_options[x])
        with top_col2:
            st.write("")
            st.write("")
            st.markdown('<button onclick="window.print()" style="background-color:#8C5A2B; color:white; border:none; padding:10px 16px; border-radius:8px; font-weight:bold; cursor:pointer; width:100%;">🖨️ طباعة / حفظ A4 PDF</button>', unsafe_allow_html=True)

        data = next(item for item in st.session_state.resignations_db if item["id"] == selected_id)

        exp_days = (data['resignation_date'] - data['hiring_date']).days
        h_date = data['hiring_date'].strftime("%d/%m/%Y")
        r_date = data['resignation_date'].strftime("%d/%m/%Y")
        l_date = data['last_working_day'].strftime("%d/%m/%Y")
        r_date_header = data['resignation_date'].strftime("%d %b %Y")

        # HTML Structure for Page-Fit A4
        st.markdown(f"""
        <div id="printable-a4" class="a4-container">
            <!-- Header -->
            <table style="width:100%; border:none; margin-bottom:10px;">
                <tr>
                    <td style="width:60%; vertical-align:top; border:none;">
                        <div class="req-subtitle">Dear Mr. {data['direct_manager'].split()[0] if data['direct_manager'] else 'Manager'},</div>
                        <div class="req-title">RESIGNATION<br>APPROVAL REQUEST</div>
                    </td>
                    <td style="width:40%; vertical-align:top; border:none;">
                        <div style="background:#FAF8F5; border:1px solid #D6C2A7; border-radius:8px; padding:8px; display:flex; gap:10px; align-items:center;">
                            <div style="font-size:32px;">👤</div>
                            <div>
                                <div class="emp-label">EMPLOYEE PROFILE</div>
                                <div class="emp-name">{data['employee_name']}</div>
                                <div class="emp-title">{data['job_title']}</div>
                                <div class="emp-resign-date">Resigning {r_date_header}</div>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>

            <!-- Journey Header -->
            <div style="color:#000; font-weight:800; font-size:15px; margin-top:5px;">Resignation Journey</div>
            
            <div class="journey-flex">
                <div class="journey-item"><div class="journey-icon">👤</div><div class="journey-title">Joined</div><div class="journey-val">{h_date}</div></div>
                <div class="journey-item"><div class="journey-icon">🏆</div><div class="journey-title">Total Experience</div><div class="journey-val">{exp_days} Days</div></div>
                <div class="journey-item"><div class="journey-icon">📄</div><div class="journey-title">Resignation Submitted</div><div class="journey-val">{r_date}</div></div>
                <div class="journey-item"><div class="journey-icon">🕒</div><div class="journey-title">Notice Period Status</div><div class="journey-val">{data["notice_period"]}</div></div>
                <div class="journey-item"><div class="journey-icon">✅</div><div class="journey-title">Process Finalized</div><div class="journey-val">Approved {r_date}</div></div>
            </div>

            <!-- Metrics Pills -->
            <div class="metrics-flex">
                <div class="metric-col"><div class="metric-header">Total Net Pay (EGP)</div><div class="metric-body">{data["net_pay"]}</div></div>
                <div class="metric-col"><div class="metric-header">Last Working Day</div><div class="metric-body">{l_date}</div></div>
                <div class="metric-col"><div class="metric-header">Reason for Leaving</div><div class="metric-body">{data["reason"]}</div></div>
                <div class="metric-col"><div class="metric-header">Direct Manager</div><div class="metric-body">{data["direct_manager"]}</div></div>
            </div>

            <!-- Table -->
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

            <!-- Actions -->
            <div class="action-box">
                <div class="action-title">MANAGER ACTION ITEMS</div>
                <div class="action-subtitle">Resignation Next Steps</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:11px;">
                    <div>🧮 Calculate final dues payout ({data['net_pay']} EGP).</div>
                    <div>🤝 Facilitate handover process with {data['handover_status']}.</div>
                    <div>🕒 Review notice period waiver request ({data['notice_period']}).</div>
                    <div>📦 Schedule property return (laptop, badge, keys).</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: EDIT / DELETE / CREATE RESIGNATION
# ---------------------------------------------------------
with tab_manage:
    st.subheader("⚙️ إدارة الاستقالات (إضافة / تعديل / حذف)")

    action_type = st.radio("اختر نوع الإجراء المطلوب:", ["إضافة استقالة جديدة ➕", "تعديل بيانات استقالة ✏️", "حذف استقالة 🗑️"], horizontal=True)

    # 1. DELETE ACTION
    if action_type == "حذف استقالة 🗑️":
        if not st.session_state.resignations_db:
            st.warning("لا توجد استقالات لحذفها.")
        else:
            del_options = {r['id']: f"{r['employee_name']} — ({r['branch']})" for r in st.session_state.resignations_db}
            del_id = st.selectbox("اختر الاستقالة المراد حذفها نهائياً:", options=list(del_options.keys()), format_func=lambda x: del_options[x])
            
            if st.button("❌ تأكيد حذف الاستقالة", type="primary"):
                st.session_state.resignations_db = [r for r in st.session_state.resignations_db if r['id'] != del_id]
                st.success("تم حذف الاستقالة بنجاح!")
                st.rerun()

    # 2. EDIT OR CREATE FORM
    else:
        if action_type == "تعديل بيانات استقالة ✏️" and st.session_state.resignations_db:
            edit_options = {r['id']: f"{r['employee_name']} — ({r['branch']})" for r in st.session_state.resignations_db}
            edit_id = st.selectbox("اختر الموظف المراد تعديل بياناته:", options=list(edit_options.keys()), format_func=lambda x: edit_options[x])
            target_data = next(item for item in st.session_state.resignations_db if item["id"] == edit_id)
        else:
            target_data = {
                "id": None,
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
                "photo": None
            }

        with st.form("edit_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                emp_name = to_english_str(st.text_input("اسم الموظف", target_data['employee_name']))
                job_title = to_english_str(st.text_input("المسمى الوظيفي", target_data['job_title']))
                branch = to_english_str(st.text_input("الفرع", target_data['branch']))
                grading = to_english_str(st.text_input("نظام الدرجة الوظيفية", target_data['grading']))
                direct_manager = to_english_str(st.text_input("المدير المباشر", target_data['direct_manager']))
                reason = to_english_str(st.text_input("سبب الاستقالة", target_data['reason']))
                
            with col2:
                hiring_date = st.date_input("تاريخ التعيين", target_data['hiring_date'])
                resignation_date = st.date_input("تاريخ تقديم الاستقالة", target_data['resignation_date'])
                last_working_day = st.date_input("آخر يوم عمل", target_data['last_working_day'])
                net_pay = st.number_input("إجمالي المستحقات (EGP)", value=int(target_data['net_pay']), step=500)
                notice_period = to_english_str(st.text_input("فترة الإشعار", target_data['notice_period']))
                handover_status = to_english_str(st.text_input("حالة التسليم", target_data['handover_status']))

            col3, col4 = st.columns(2)
            with col3:
                absence_days = st.number_input("أيام الغياب", value=int(target_data['absence_days']))
                loan_balance = st.number_input("رصيد السلفة (EGP)", value=int(target_data['loan_balance']))
            with col4:
                photo_file = st.file_uploader("الصورة الشخصية", type=["png", "jpg", "jpeg"])

            save_btn = st.form_submit_button("💾 حفظ البيانات", type="primary")

            if save_btn:
                photo_bytes = photo_file.getvalue() if photo_file else target_data['photo']
                
                updated_record = {
                    "id": target_data['id'] if target_data['id'] else (max([r['id'] for r in st.session_state.resignations_db], default=0) + 1),
                    "employee_name": emp_name,
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
                    "photo": photo_bytes
                }

                if action_type == "تعديل بيانات استقالة ✏️" and target_data['id']:
                    idx = next(i for i, item in enumerate(st.session_state.resignations_db) if item["id"] == target_data['id'])
                    st.session_state.resignations_db[idx] = updated_record
                    st.success("✅ تم تحديث بيانات الاستقالة بنجاح!")
                else:
                    st.session_state.resignations_db.insert(0, updated_record)
                    st.success("✅ تم إضافة الاستقالة الجديدة بنجاح!")
                st.rerun()

# ---------------------------------------------------------
# TAB 3: BRANCHES DASHBOARD
# ---------------------------------------------------------
with tab_dashboard:
    st.title("📊 داشبورد تحليل استقالات الفروع")

    if not st.session_state.resignations_db:
        st.info("لا توجد استقالات مسجلة.")
    else:
        records = []
        for r in st.session_state.resignations_db:
            exp = (r['resignation_date'] - r['hiring_date']).days
            records.append({
                "Employee Name": r['employee_name'],
                "Branch": r['branch'],
                "Job Title": r['job_title'],
                "Hiring Date": r['hiring_date'].strftime("%Y-%m-%d"),
                "Resignation Date": r['resignation_date'].strftime("%Y-%m-%d"),
                "Net Pay (EGP)": r['net_pay'],
                "Reason": r['reason'],
                "Manager": r['direct_manager'],
                "Experience (Days)": exp
            })
        
        df = pd.DataFrame(records)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("إجمالي الاستقالات", len(df))
        m2.metric("عدد الفروع", df['Branch'].nunique())
        m3.metric("إجمالي المستحقات (EGP)", f"{df['Net Pay (EGP)'].sum():,}")
        m4.metric("متوسط الخبرة (يوم)", f"{int(df['Experience (Days)'].mean())} يوم")

        st.markdown("---")

        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("🏢 توزيع الاستقالات حسب الفرع")
            b_df = df['Branch'].value_counts().reset_index()
            b_df.columns = ['اسم الفرع', 'عدد الاستقالات']
            st.dataframe(b_df, use_container_width=True)
            st.bar_chart(data=b_df.set_index('اسم الفرع'))

        with c2:
            st.subheader("💡 الأسباب الأكثر شيوعاً")
            r_df = df['Reason'].value_counts().reset_index()
            r_df.columns = ['السبب', 'العدد']
            st.dataframe(r_df, use_container_width=True)

        st.markdown("---")
        st.subheader("🔍 البحث والتصدير")
        q = st.text_input("بحث باسم الموظف أو الفرع:").strip()
        filtered = df[df['Employee Name'].str.contains(q, case=False, na=False) | df['Branch'].str.contains(q, case=False, na=False)] if q else df
        st.dataframe(filtered, use_container_width=True)
