import streamlit as st

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Dating Hub Premium", page_icon="💖", layout="centered")

# --- 2. CSS "TỬ TẾ" (Biến các mục thành Card giao diện) ---
st.markdown("""
<style>
    /* Tổng thể App */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Container chính */
    .hero-section {
        text-align: center;
        padding: 40px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px;
        border: 1px solid rgba(255, 20, 147, 0.3);
        margin-bottom: 40px;
    }

    .title-text {
        color: #FF1493;
        font-size: 4.5rem;
        font-weight: 900;
        margin-bottom: 10px;
        text-shadow: 2px 2px 20px rgba(255, 20, 147, 0.4);
    }

    /* Thiết kế Card tính năng */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 20px;
        border-left: 5px solid #FF1493;
        transition: 0.3s;
        height: 180px;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-5px);
    }

    .feature-title {
        color: #FF69B4;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .feature-desc {
        color: #dddddd;
        font-size: 0.95rem;
    }

    /* Nút bấm nhảy trang */
    div.stButton > button {
        background: linear-gradient(90deg, #FF1493, #FF69B4) !important;
        color: white !important;
        border: none !important;
        padding: 15px 40px !important;
        border-radius: 50px !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        width: 100% !important;
        transition: 0.3s !important;
        box-shadow: 0 10px 20px rgba(255, 20, 147, 0.3) !important;
    }

    div.stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 15px 30px rgba(255, 20, 147, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown('<div class="hero-section">', unsafe_allow_html=True)
st.markdown('<h1 class="title-text">DATING PRO</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #bbb; font-size: 1.3rem;">KẾT NỐI NGƯỜI DÙNG THỰC - KHÔNG AI - KHÔNG GIẢ TẠO</p>', unsafe_allow_html=True)

st.write("") # Khoảng cách

# Cột chứa nút bấm truy cập
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("🚀 BẮT ĐẦU NGAY"):
        st.switch_page("pages/dating_app.py")
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. MỤC TÍNH NĂNG (FEATURE CARDS) ---
# Đây là phần thay thế cho các "Note" văn bản bình thường
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🔍 Tìm kiếm</div>
        <div class="feature-desc">Hệ thống lọc người dùng thông minh theo tên và sở thích cá nhân.</div>
    </div>
    """, unsafe_allow_html=True)

with col_f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">💬 Nhắn tin</div>
        <div class="feature-desc">Trò chuyện trực tiếp 2 chiều với tốc độ cao và bảo mật tuyệt đối.</div>
    </div>
    """, unsafe_allow_html=True)

with col_f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📹 Video Call</div>
        <div class="feature-desc">Gặp mặt trực tiếp qua cuộc gọi video chất lượng cao tích hợp sẵn.</div>
    </div>
    """, unsafe_allow_html=True)