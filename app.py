import streamlit as st
import pandas as pd
from datetime import date

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Resignation Approval System",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------------
# Custom CSS (Glowing Tab Rectangles & Clean A4 Styling)
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

    /* Glowing Rectangular Top Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        padding-bottom: 15px;
        border-bottom: 2px solid #EADBCE;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: #FFFFFF;
        border-radius: 8px;
        color: #8C5A2B;
        font-weight: 700;
        font-size: 15px;
        border: 1.5px solid #D6C2A7;
        padding: 0px 20px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.03);
        transition: all 0.25s ease-in-out;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #8C5A2B;
        color: #8C5A2B;
        transform: translateY(-2px);
    }
    
    /* Active Highlight Button */
    .stTabs [aria-selected="true"] {
        background-color: #8C5A2B !important;
        color: #FFFFFF !important;
        border-color: #8C5A2B !important;
        box-shadow: 0px 4px 14px rgba(140, 90, 43, 0.45) !important;
        transform: translateY(-2px);
    }

    /* Print Setup for A4 */
    @media print {
        @page {
            size: A4 portrait;
            margin: 6mm;
        }
        body * {
            visibility: hidden;
        }
        #printable-area, #printable-area * {
            visibility: visible;
        }
        #printable-area {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
        }
        .no-print {
            display: none !important;
        }
    }

    /* Approval Card Container */
    .a4-card {
        background-color: #FAF8F5;
        border: 1.5px solid #D6C2A7;
        border-radius: 12px;
        padding: 20px;
        margin: 0 auto;
        max-width: 820px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
    }

    /* Badges & Metrics */
    .metric-badge {
        background-color: #8C5A2B;
        color: white;
        border-radius: 14px;
        padding: 4px 8px;
        text-align: center;
        font-weight: 700;
        font-size: 11px;
        margin-bottom: 4px;
    }
    .metric-box {
        background-color: #FAF8F5;
        border: 1px solid #D6C2A7;
        border-radius: 6px;
        padding: 6px;
        text-align: center;
        font-weight: 800;
        font-size: 13px;
        color: #111;
    }

    /* Styled Table */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
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
            "loan_balance": 0
        }
    ]

# ---------------------------------------------------------
# Top Navigation Bar (Rectangular Tabs)
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
        top_col1, top_col2 = st.columns([3, 1])
        with top_col1:
            emp_options = {r['id']: f"{r['employee_name']} — ({r['branch']})" for r in st.session_state.resignations_db}
            selected_id = st.selectbox("اختر الموظف لعرض طلب الاستقالة الخاصة به:", options=list(emp_options.keys()), format_func=lambda x: emp_options[x])
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

        st.markdown('<div id="printable-area">', unsafe_allow_html=True)
        
        with st.container():
            st.markdown(f'''
            <div class="a4-card">
                <table style="width:100%; border:none; margin-bottom:10px;">
                    <tr>
                        <td style="width:60%; vertical-align:top; border:none;">
                            <div style="color:#8C5A2B; font-size:15px; font-weight:700;">Dear Mr. {data['direct_manager'].split()[0] if data['direct_manager'] else 'Manager'},</div>
                            <div style="color:#8C5A2B; font-weight:800; font-size:24px; line-height:1.1;">RESIGNATION<br>APPROVAL REQUEST</div>
                        </td>
                        <td style="width:40%; vertical-align:top; border:none;">
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
                    <div style="flex:1; border:1px solid #D
