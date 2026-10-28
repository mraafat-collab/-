import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Resignation Approval System",
    page_icon="📄",
    layout="wide"
)

# Custom Styling (Theme Matching the Image Layout)
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
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .stat-card {
        background-color: #FAF8F5;
        border: 2px solid #B87A44;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
    }
    
    .stat-title {
        color: #5C381A;
        font-size: 12px;
        font-weight: 700;
    }
    
    .stat-value {
        color: #111827;
        font-size: 16px;
        font-weight: 800;
    }
    
    .table-header {
        background-color: #A36531;
        color: white;
        font-weight: bold;
        padding: 10px 15px;
    }
    
    .action-box {
        background-color: rgba(250, 248, 245, 0.5);
        border: 1px solid #E7D5C1;
        border-radius: 16px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Data Inputs
st.sidebar.title("⚙️ إدخال البيانات الشخصية")

recipient_name = st.sidebar.text_input("اسم المدير / المرسل إليه", "Mohamed")
photo_url = st.sidebar.text_input("رابط الصورة", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300")

st.sidebar.subheader("بيانات الموظف")
emp_name = st.sidebar.text_input("اسم الموظف", "Abu Bakr Muhammad Mahmoud")
job_title = st.sidebar.text_input("المسمى الوظيفي", "Sales Casual")
branch = st.sidebar.text_input("الفرع", "Park-St Branch")
direct_manager = st.sidebar.text_input("المدير المباشر", "Sherif S. El-Sayed")
grading = st.sidebar.text_input("نظام الدرجات", "G1 - L1")

st.sidebar.subheader("التواريخ والمدة")
hiring_date = st.sidebar.text_input("تاريخ التعيين", "03/10/2026")
resignation_date = st.sidebar.text_input("تاريخ الاستقالة", "20/10/2026")
last_day = st.sidebar.text_input("آخر يوم عمل", "20/10/2026")
total_exp = st.sidebar.text_input("إجمالي الخبرة", "17 Days")

st.sidebar.subheader("الماليات والسبب")
net_pay = st.sidebar.text_input("صافي المستحقات (EGP)", "7000")
reason = st.sidebar.text_input("سبب الترك", "Education")
notice_status = st.sidebar.text_input("حالة فترة الإخطار", "One Month")
handover = st.sidebar.text_input("تسليم العمل", "Team Leader")
absence = st.sidebar.text_input("أيام الغياب", "0 Day")
loan = st.sidebar.text_input("رصيد السلفة", "0 EGP")

# Main Content Layout
col_head1, col_head2 = st.columns([2, 1])

with col_head1:
    st.write(f"### Dear Mr. {recipient_name},")
    st.markdown("<h1 style='color: #834F24; margin-top: -10px;'>RESIGNATION<br>APPROVAL REQUEST</h1>", unsafe_allow_html=True)

with col_head2:
    st.markdown(f"""
    <div class="main-card" style="display: flex; gap: 15px; align-items: center;">
        <img src="{photo_url}" style="width: 70px; height: 85px; object-fit: cover; border-radius: 8px;">
        <div>
            <div style="font-size: 10px; color: #834F24; font-weight: 800;">EMPLOYEE PROFILE</div>
            <div style="font-size: 16px; font-weight: 800;">{emp_name}</div>
            <div style="font-size: 13px; color: #4B5563;">{job_title}</div>
            <div style="font-size: 11px; background: #F4ECE1; padding: 2px 8px; border-radius: 10px; margin-top: 5px; display: inline-block;">
                Resigning {resignation_date}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Resignation Journey Pipeline
st.markdown("### Resignation Journey")
j1, j2, j3, j4, j5 = st.columns(5)
with j1:
    st.markdown(f"**👤 Joined**<br><small>{hiring_date}</small>", unsafe_allow_html=True)
with j2:
    st.markdown(f"**🏆 Total Exp**<br><small>{total_exp}</small>", unsafe_allow_html=True)
with j3:
    st.markdown(f"**📄 Submitted**<br><small>{resignation_date}</small>", unsafe_allow_html=True)
with j4:
    st.markdown(f"**⏰ Notice Status**<br><small>{notice_status}</small>", unsafe_allow_html=True)
with j5:
    st.markdown(f"**✅ Finalized**<br><small>Approved {resignation_date}</small>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Highlight Stat Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat-card"><div class="stat-title">Total Net Pay (EGP)</div><div class="stat-value">{net_pay}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><div class="stat-title">Last Working Day</div><div class="stat-value">{last_day}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><div class="stat-title">Reason for Leaving</div><div class="stat-value">{reason}</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-card"><div class="stat-title">Direct Manager</div><div class="stat-value" style="font-size:12px;">{direct_manager}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Data Table
data = {
    "Field": [
        "Employee Name", "Branch", "Job Title", "Hiring Date", "Resignation Date",
        "Last Working Day", "Grading System", "Total Net to pay EGP", "Reason for Leaving",
        "Notice Period Status", "Handover Status", "Total Experience", "Direct Manager",
        "Absence during the year", "Loan balance"
    ],
    "Value": [
        emp_name, branch, job_title, hiring_date, resignation_date,
        last_day, grading, net_pay, reason,
        notice_status, handover, total_exp, direct_manager,
        absence, loan
    ]
}
st.table(data)

# Manager Action Items Box
st.markdown(f"""
<div class="action-box">
    <div style="color: #834F24; font-size: 12px; font-weight: 800;">MANAGER ACTION ITEMS</div>
    <h4 style="margin-top: 0;">Resignation Next Steps</h4>
    <ul>
        <li>🧮 Calculate final dues and payout. Ensure <strong>'Total Net to pay {net_pay} EGP'</strong> is correct.</li>
        <li>🤝 Facilitate handover process with Team Leader and new point of contact.</li>
        <li>⏰ Review notice period waiver request <strong>({notice_status} Status)</strong>.</li>
        <li>📦 Schedule property return (laptop, badge, keys).</li>
        <li>✉️ Issue final acceptance letter and experience certificate.</li>
    </ul>
</div>
""", unsafe_allow_html=True)