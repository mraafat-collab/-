import streamlit as st
import pandas as pd
from datetime import date
import streamlit.components.v1 as components

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Resignation Approval System",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------------
# Custom CSS for App & Top Tabs Styling
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

    /* Rectangular Glowing Top Navigation Tabs */
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

# Initializing Session Database
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
            "loan_balance": 0
        }
    ]

# ---------------------------------------------------------
# Top Navigation Bar (Glowing Tabs)
# ---------------------------------------------------------
tab_main, tab_manage, tab_dashboard = st.tabs([
    "🏠 عرض وطباعة الاستقالة (A4)", 
    "📝 إضافة / تعديل / حذف استقالة", 
    "📊 داشبورد الفروع"
])

# ---------------------------------------------------------
# TAB 1: DISPLAY & PRINT A4 TEMPLATE
# ---------------------------------------------------------
with tab_main:
    if not st.session_state.resignations_db:
        st.warning("⚠️ لا توجد بيانات استقالات مسجلة حالياً.")
    else:
        emp_options = {r['id']: f"{r['employee_name']} — ({r['branch']})" for r in st.session_state.resignations_db}
        selected_id = st.selectbox("اختر الموظف لعرض طلب الاستقالة الخاصة به:", options=list(emp_options.keys()), format_func=lambda x: emp_options[x])

        data = next(item for item in st.session_state.resignations_db if item["id"] == selected_id)

        exp_days = (data['resignation_date'] - data['hiring_date']).days
        h_date = data['hiring_date'].strftime("%d/%m/%Y")
        r_date = data['resignation_date'].strftime("%d/%m/%Y")
        l_date = data['last_working_day'].strftime("%d/%m/%Y")
        r_date_header = data['resignation_date'].strftime("%d %b %Y")
        mgr_first = data['direct_manager'].split()[0] if data['direct_manager'] else 'Manager'

        # Full Render Engine inside Iframe (Guarantees Working Print & HTML Rendering)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
                body {{
                    font-family: 'Inter', sans-serif;
                    background-color: #F8F6F0;
                    margin: 0;
                    padding: 10px;
                }}
                .print-btn {{
                    background-color: #8C5A2B;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 14px;
                    cursor: pointer;
                    margin-bottom: 15px;
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
                }}
                .print-btn:hover {{
                    background-color: #704721;
                }}
                .a4-card {{
                    background-color: #FAF8F5;
                    border: 1.5px solid #D6C2A7;
                    border-radius: 12px;
                    padding: 20px;
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
                .custom-table tr:nth-child(even) {{
                    background-color: #FAF8F5;
                }}
                .metric-badge {{
                    background-color: #8C5A2B;
                    color: white;
                    border-radius: 14px;
                    padding: 4px 8px;
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
                    .a4-card {{ border: none; box-shadow: none; width: 100%; max-width: 100%; }}
                }}
            </style>
        </head>
        <body>
            <div style="text-align: right;" class="no-print">
                <button onclick="window.print()" class="print-btn">🖨️ طباعة / حفظ A4 PDF</button>
            </div>

            <div class="a4-card">
                <table style="width:100%; border:none; margin-bottom:10px;">
                    <tr>
                        <td style="width:58%; vertical-align:top; border:none;">
                            <div style="color:#8C5A2B; font-size:15px; font-weight:700;">Dear Mr. {mgr_first},</div>
                            <div style="color:#8C5A2B; font-weight:800; font-size:24px; line-height:1.1;">RESIGNATION<br>APPROVAL REQUEST</div>
                        </td>
                        <td style="width:42%; vertical-align:top; border:none;">
                            <div style="background:#FAF8F5; border:1px solid #D6C2A7; border-radius:8px; padding:8px; display:flex; gap:10px; align-items:center;">
                                <div style="width:50px; height:50px; background:#EADBCE; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:24px;">👤</div>
                                <div>
                                    <div style="font-size:10px; text-transform:uppercase; color:#8C5A2B; font-weight:800;">EMPLOYEE PROFILE</div>
                                    <div style="font-size:16px; font-weight:800; color:#111;">{data['employee_name']}</div>
                                    <div style="font-size:12px; color:#444;">{data['job_title']}</div>
                                    <div style="font-size:11px; color:#666;">Resigning {r_date_header}</div>
                                </div>
                            </div>
                        </td>
                    </tr>
                </table>

                <div style="color:#000; font-weight:800; font-size:14px; margin-top:6px; margin-bottom:6px;">Resignation Journey</div>
                
                <div style="display:flex; gap:6px; text-align:center;">
                    <div style="flex:1; border:1px solid #D6C2A7; border-radius:8px; padding:6px;"><div style="background:#8C5A2B; color:white; border-radius:50%; width:22px; height:22px; margin:auto; font-size:10px; display:flex; align-items:center; justify-content:center;">👤</div><div style="font-size:10px; font-weight:700; margin-top:2px;">Joined</div><div style="font-size:11px;">{h_date}</div></div>
                    <div style="flex:1; border:1px solid #D6C2A7; border-radius:8px; padding:6px;"><div style="background:#8C5A2B; color:white; border-radius:50%; width:22px; height:22px; margin:auto; font-size:10px; display:flex; align-items:center; justify-content:center;">🏆</div><div style="font-size:10px; font-weight:700; margin-top:2px;">Experience</div><div style="font-size:11px;">{exp_days} Days</div></div>
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
                        <div>🧮 Calculate final dues payout ({data['net_pay']} EGP). Ensure 'Total Net to pay {data['net_pay']} EGP' is correct.</div>
                        <div>🤝 Facilitate handover process with {data['handover_status']} and new point of contact.</div>
                        <div>🕒 Review notice period waiver request ({data['notice_period']}).</div>
                        <div>📦 Schedule property return (laptop, badge, keys).</div>
                        <div>📑 Issue final acceptance letter and experience certificate.</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Render Component
        components.html(html_content, height=880, scrolling=True)

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
            
            if st.button("❌ تأكيد الحذف النهائيات", type="primary"):
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
                "loan_balance": 0
            }

        with st.form("resignation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                emp_name = to_english_str(st.text_input("اسم الموظف (Employee Name)", target_data['employee_name']))
                job_title = to_english_str(st.text_input("المسمى الوظيفي (Job Title)", target_data['job_title']))
                branch = to_english_str(st.text_input("اسم الفرع (Branch)", target_data['branch']))
                grading = to_english_str(st.text_input("الدرجة الوظيفية (Grading System)", target_data['grading']))
                direct_manager = to_english_str(st.text_input("المدير المباشر (Direct Manager)", target_data['direct_manager']))
                reason = to_english_str(st.text_input("سبب الاستقالة (Reason for Leaving)", target_data['reason']))
                
            with col2:
                hiring_date = st.date_input("تاريخ التعيين (Hiring Date)", target_data['hiring_date'])
                resignation_date = st.date_input("تاريخ تقديم الاستقالة (Resignation Date)", target_data['resignation_date'])
                last_working_day = st.date_input("آخر يوم عمل (Last Working Day)", target_data['last_working_day'])
                net_pay = st.number_input("إجمالي المستحقات (Total Net Pay EGP)", value=int(target_data['net_pay']), step=500)
                notice_period = to_english_str(st.text_input("فترة الإشعار (Notice Period Status)", target_data['notice_period']))
                handover_status = to_english_str(st.text_input("حالة التسليم (Handover Status)", target_data['handover_status']))

            col3, col4 = st.columns(2)
            with col3:
                absence_days = st.number_input("أيام الغياب (Absence Days)", value=int(target_data['absence_days']))
            with col4:
                loan_balance = st.number_input("رصيد السلفة (Loan Balance EGP)", value=int(target_data['loan_balance']))

            save_btn = st.form_submit_button("💾 حفظ البيانات والتحديث", type="primary")

            if save_btn:
                new_id = target_data['id'] if target_data['id'] else (max([r['id'] for r in st.session_state.resignations_db], default=0) + 1)
                
                updated_record = {
                    "id": new_id,
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
                    "loan_balance": loan_balance
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
            exp = (r['resignation_date'] - r['hiring_date']).days
            records.append({
                "اسم الموظف": r['employee_name'],
                "الفرع": r['branch'],
                "المسمى الوظيفي": r['job_title'],
                "تاريخ الاستقالة": r['resignation_date'].strftime("%Y-%m-%d"),
                "إجمالي المستحقات (EGP)": r['net_pay'],
                "سبب الاستقالة": r['reason'],
                "المدير المباشر": r['direct_manager'],
                "الخبرة (يوم)": exp
            })
        
        df = pd.DataFrame(records)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("إجمالي الاستقالات", len(df))
        m2.metric("عدد الفروع", df['الفرع'].nunique())
        m3.metric("إجمالي المستحقات (EGP)", f"{df['إجمالي المستحقات (EGP)'].sum():,}")
        m4.metric("متوسط الخبرة (يوم)", f"{int(df['الخبرة (يوم)'].mean())} يوم")

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
