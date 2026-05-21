import streamlit as st
import random

# 1. Khởi tạo dữ liệu giả lập (Database tạm thời)
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "matched_user" not in st.session_state:
    st.session_state.matched_user = None
if "messages_nn" not in st.session_state:
    st.session_state.messages_nn = [
        {"sender": "Hệ thống (1:N)", "text": "Chào mừng bạn đến với sảnh hẹn hò! Hãy tìm một nửa của mình nhé.", "type": "system"}
    ]
if "messages_11" not in st.session_state:
    st.session_state.messages_11 = {}
if "active_call" not in st.session_state:
    st.session_state.active_call = {}
if "call_duration" not in st.session_state:
    st.session_state.call_duration = 0

# Danh sách người dùng ngẫu nhiên để quẹt match
DATING_POOL = [
    {"name": "Linh", "age": 22, "bio": "Thích du lịch, mê trà sữa 🧋", "gender": "Nữ", "logged_in": True, "profile_created": True},
    {"name": "Minh", "age": 25, "bio": "Kỹ sư phần mềm, thích nuôi mèo 🐱", "gender": "Nam", "logged_in": False, "profile_created": True},
    {"name": "Trang", "age": 24, "bio": "Yêu âm nhạc, biết đánh đàn Piano 🎹", "gender": "Nữ", "logged_in": True, "profile_created": False},
    {"name": "Tuấn", "age": 27, "bio": "Đam mê nhiếp ảnh và chạy bộ 🏃‍♂️", "gender": "Nam", "logged_in": False, "profile_created": False}
]

st.set_page_config(page_title="Dating Chat App", page_icon="❤️", layout="wide")
st.title("❤️ Ứng Dụng Hẹn Hò Siêu Tốc (Realtime Dating Chat)")

# ---- PHẦN ĐĂNG NHẬP / TẠO PROFILE ----
if not st.session_state.user_profile:
    st.subheader("Bước 1: Tạo hồ sơ hẹn hò của bạn")
    name = st.text_input("Tên của bạn:")
    age = st.number_input("Tuổi:", min_value=18, max_value=50, value=20)
    gender = st.selectbox("Giới tính:", ["Nam", "Nữ", "Khác"])
    bio = st.text_area("Giới thiệu bản thân (Bio):")
    
    if st.button("Bắt đầu hẹn hò ngay"):
        if name and bio:
            st.session_state.user_profile = {"name": name, "age": age, "gender": gender, "bio": bio}
            st.rerun()
        else:
            st.error("Vui lòng điền đầy đủ thông tin!")
else:
    # Giao diện chính sau khi đăng nhập
    st.sidebar.header(f"👤 {st.session_state.user_profile['name']} ({st.session_state.user_profile['age']})")
    st.sidebar.write(f"ℹ️ {st.session_state.user_profile['bio']}")
    if st.sidebar.button("Đăng xuất / Tạo lại Profile"):
        st.session_state.user_profile = None
        st.session_state.matched_user = None
        st.rerun()

    # CHIA GIAO DIỆN THÀNH 2 CỘT
    col1, col2 = st.columns([1, 2])

    # ---- PHẦN 1: QUẸT MATCH (TÌM KIẾM 1:1) ----
    with col1:
        st.header("🔍 Tìm kiếm đối tượng")
        with st.expander("⚙️ Bộ lọc tìm kiếm", expanded=True):
            search_mode = st.radio(
                "Chọn bộ lọc tìm kiếm:",
                ["Chỉ người đã đăng nhập", "Chỉ người đã tạo hồ sơ", "Người đã đăng nhập hoặc đã tạo hồ sơ"],
                index=2
            )

            if search_mode == "Chỉ người đã đăng nhập":
                available_candidates = [user for user in DATING_POOL if user["logged_in"]]
                st.caption("Hiển thị chỉ những người đang hoạt động ngay bây giờ.")
            elif search_mode == "Chỉ người đã tạo hồ sơ":
                available_candidates = [user for user in DATING_POOL if user["profile_created"]]
                st.caption("Hiển thị những người đã hoàn thành hồ sơ của họ.")
            else:
                available_candidates = [user for user in DATING_POOL if user["logged_in"] or user["profile_created"]]
                st.caption("Hiển thị những người đã đăng nhập hoặc đã tạo hồ sơ.")

        if not available_candidates:
            st.warning("Không có đối tượng phù hợp với bộ lọc hiện tại. Vui lòng thử lại sau.")
        elif not st.session_state.matched_user:
            # Gợi ý ngẫu nhiên một người phù hợp với bộ lọc
            if "current_candidate" not in st.session_state or st.session_state.current_candidate not in available_candidates:
                st.session_state.current_candidate = random.choice(available_candidates)
            
            cand = st.session_state.current_candidate
            st.info(f"**Tên:** {cand['name']} | **Tuổi:** {cand['age']} | **Giới tính:** {cand['gender']}")
            st.write(f"💬 *{cand['bio']}*")
            status_text = []
            if cand["logged_in"]:
                status_text.append("Đã đăng nhập")
            if cand["profile_created"]:
                status_text.append("Có hồ sơ")
            st.write(f"📌 {' • '.join(status_text)}")
            
            c_btn1, c_btn2 = st.columns(2)
            if c_btn1.button("❌ Bỏ qua (Quẹt trái)"):
                st.session_state.current_candidate = random.choice(available_candidates)
                st.rerun()
            if c_btn2.button("❤️ Thích (Quẹt phải)"):
                # Giả lập tỷ lệ Match thành công là 70%
                if random.random() < 0.7:
                    st.session_state.matched_user = cand
                    st.success(f"🎉 Bạn đã MATCH với {cand['name']}!")
                    if cand['name'] not in st.session_state.messages_11:
                        st.session_state.messages_11[cand['name']] = []
                else:
                    st.warning("Người ấy chưa quẹt lại bạn rồi. Thử người khác nhé!")
                    st.session_state.current_candidate = random.choice(available_candidates)
                st.rerun()
        else:
            st.success(f"💑 Đang kết đôi với: **{st.session_state.matched_user['name']}**")
            if st.button("💔 Huỷ kết đôi (Unmatch)"):
                st.session_state.matched_user = None
                st.rerun()

    # ---- PHẦN 2: CÁC KHÔNG GIAN CHAT (1:1, 1:N, N-N) ----
    with col2:
        tab1, tab2, tab3 = st.tabs(["💬 Sảnh Chung (Chat N-N)", "🔒 Chat Riêng (Chat 1:1)", "📢 Thông Báo (Kênh 1:N)"])

        # TAB 1: CHAT N-N (Tất cả mọi người cùng chat ở sảnh chờ)
        with tab1:
            st.subheader("🌐 Sảnh chờ chung (N-N Chat)")
            
            # ---- HIỂN THỊ CHAT N-N ----
            chat_container_nn = st.container(height=300)
            for msg in st.session_state.messages_nn:
                if msg.get("type") == "system":
                    chat_container_nn.info(msg['text'])
                elif msg.get("type") == "image":
                    chat_container_nn.write(f"**{msg['sender']}:**")
                    chat_container_nn.image(msg['image_data'], caption=msg.get('file_name', 'Hình ảnh'))
                elif msg.get("type") == "audio":
                    chat_container_nn.write(f"**{msg['sender']}:** 🎤 Tin nhắn thoại")
                    chat_container_nn.audio(msg['audio_data'])
                elif msg.get("type") == "file":
                    chat_container_nn.write(f"**{msg['sender']}:** 📎 {msg.get('file_name', 'Tệp đính kèm')}")
                else:
                    chat_container_nn.write(f"**{msg['sender']}:** {msg['text']}")
            
            st.divider()
            
            # ---- FORM GỬI TIN NHẮN VÀ TẬP TIN N-N ----
            user_msg_nn = st.text_input("Nhập tin nhắn vào sảnh chung:", key="msg_nn")
            
            col_nn1, col_nn2, col_nn3, col_nn4, col_nn5 = st.columns(5)
            
            with col_nn1:
                if st.button("📤 Gửi tin nhắn", key="send_nn"):
                    if user_msg_nn:
                        st.session_state.messages_nn.append({"sender": st.session_state.user_profile['name'], "text": user_msg_nn})
                        st.rerun()
            
            with col_nn2:
                uploaded_image_nn = st.file_uploader("🖼️ Hình ảnh", type=["png", "jpg", "jpeg", "gif"], key="img_nn")
                if uploaded_image_nn:
                    st.session_state.messages_nn.append({
                        "sender": st.session_state.user_profile['name'],
                        "type": "image",
                        "image_data": uploaded_image_nn,
                        "file_name": uploaded_image_nn.name
                    })
                    st.success("✅ Đã gửi hình ảnh vào sảnh chung")
                    st.rerun()
            
            with col_nn3:
                uploaded_file_nn = st.file_uploader("📎 Tệp đính kèm", key="file_nn")
                if uploaded_file_nn:
                    st.session_state.messages_nn.append({
                        "sender": st.session_state.user_profile['name'],
                        "type": "file",
                        "file_name": uploaded_file_nn.name,
                        "file_data": uploaded_file_nn.read()
                    })
                    st.success("✅ Đã gửi tệp vào sảnh chung")
                    st.rerun()
            
            with col_nn4:
                audio_bytes_nn = st.audio_input("🎤 Ghi âm", key="audio_nn")
                if audio_bytes_nn:
                    st.session_state.messages_nn.append({
                        "sender": st.session_state.user_profile['name'],
                        "type": "audio",
                        "audio_data": audio_bytes_nn
                    })
                    st.success("✅ Đã gửi tin nhắn thoại vào sảnh chung")
                    st.rerun()
            
            with col_nn5:
                if st.button("❓ Trợ giúp", key="help_nn"):
                    st.info("💡 Sảnh chung là nơi tất cả mọi người có thể chat, chia sẻ hình ảnh, tệp và tin nhắn thoại.")

        # TAB 2: CHAT 1:1 (Chỉ chat được khi đã MATCH thành công)
        with tab2:
            st.subheader("🔒 Trò chuyện riêng tư (1:1 Chat)")
            if st.session_state.matched_user:
                partner_name = st.session_state.matched_user['name']
                
                # ---- PHẦN CUỘC GỌI (Voice/Video Call) ----
                call_key = f"call_{partner_name}"
                col_call1, col_call2, col_call3 = st.columns(3)
                
                if call_key not in st.session_state.active_call:
                    st.session_state.active_call[call_key] = False
                
                with col_call1:
                    if not st.session_state.active_call[call_key]:
                        if st.button("📞 Gọi thoại", key=f"voice_call_{partner_name}"):
                            st.session_state.active_call[call_key] = True
                            st.success(f"📞 Đang gọi {partner_name}... Chờ phía bên kia trả lời.")
                            st.rerun()
                    else:
                        if st.button("❌ Kết thúc cuộc gọi", key=f"end_call_{partner_name}"):
                            st.session_state.active_call[call_key] = False
                            st.session_state.messages_11[partner_name].append(
                                {"sender": "Hệ thống", "text": f"[Cuộc gọi thoại kết thúc]", "type": "system"}
                            )
                            st.rerun()
                
                with col_call2:
                    if st.button("🎥 Gọi video", key=f"video_call_{partner_name}"):
                        st.info(f"🎥 Tính năng Video Call (Phần 2) sẽ được nâng cấp trong thời gian tới!")
                
                with col_call3:
                    if st.session_state.active_call[call_key]:
                        st.warning("🔴 Đang trong cuộc gọi...")
                    else:
                        st.caption("Nhấn để bắt đầu cuộc gọi")
                
                st.divider()
                
                # ---- HIỂN THỊ CHAT ----
                chat_container_11 = st.container(height=250)
                
                # Hiển thị lịch sử chat 1:1
                for msg in st.session_state.messages_11.get(partner_name, []):
                    if msg.get("type") == "system":
                        chat_container_11.info(msg['text'])
                    elif msg.get("type") == "image":
                        chat_container_11.write(f"**{msg['sender']}:**")
                        chat_container_11.image(msg['image_data'], caption=msg.get('file_name', 'Hình ảnh'))
                    elif msg.get("type") == "audio":
                        chat_container_11.write(f"**{msg['sender']}:** 🎤 Tin nhắn thoại")
                        chat_container_11.audio(msg['audio_data'])
                    elif msg.get("type") == "file":
                        chat_container_11.write(f"**{msg['sender']}:** 📎 {msg.get('file_name', 'Tệp đính kèm')}")
                    else:
                        chat_container_11.write(f"**{msg['sender']}:** {msg['text']}")
                
                st.divider()
                
                # ---- FORM GỬI TIN NHẮN VÀ TẬP TIN ----
                user_msg_11 = st.text_input(f"Nhắn tin cho {partner_name}:", key=f"msg_{partner_name}")
                
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                
                with col_btn1:
                    if st.button("📤 Gửi tin nhắn", key=f"send_msg_{partner_name}"):
                        if user_msg_11:
                            st.session_state.messages_11[partner_name].append({"sender": st.session_state.user_profile['name'], "text": user_msg_11})
                            bot_replies = ["Chào bạn nha!", "Hì, bio của bạn dễ thương quá.", "Bạn đang làm gì đó?", "Rất vui được kết nối với bạn!"]
                            st.session_state.messages_11[partner_name].append({"sender": partner_name, "text": random.choice(bot_replies)})
                            st.rerun()
                
                with col_btn2:
                    uploaded_image = st.file_uploader("🖼️ Hình ảnh", type=["png", "jpg", "jpeg", "gif"], key=f"img_{partner_name}")
                    if uploaded_image:
                        st.session_state.messages_11[partner_name].append({
                            "sender": st.session_state.user_profile['name'],
                            "type": "image",
                            "image_data": uploaded_image,
                            "file_name": uploaded_image.name
                        })
                        st.success(f"✅ Đã gửi hình ảnh cho {partner_name}")
                        st.rerun()
                
                with col_btn3:
                    uploaded_file = st.file_uploader("📎 Tệp đính kèm", key=f"file_{partner_name}")
                    if uploaded_file:
                        st.session_state.messages_11[partner_name].append({
                            "sender": st.session_state.user_profile['name'],
                            "type": "file",
                            "file_name": uploaded_file.name,
                            "file_data": uploaded_file.read()
                        })
                        st.success(f"✅ Đã gửi tệp cho {partner_name}")
                        st.rerun()
                
                with col_btn4:
                    audio_bytes = st.audio_input("🎤 Ghi âm", key=f"audio_{partner_name}")
                    if audio_bytes:
                        st.session_state.messages_11[partner_name].append({
                            "sender": st.session_state.user_profile['name'],
                            "type": "audio",
                            "audio_data": audio_bytes
                        })
                        st.success(f"✅ Đã gửi tin nhắn thoại cho {partner_name}")
                        st.rerun()
            else:
                st.warning("⚠️ Bạn cần Quẹt phải và MATCH thành công với ai đó ở cột bên trái để mở khoá Chat 1:1!")

        # TAB 3: KÊNH 1:N (Chỉ Admin/Hệ thống gửi, Member chỉ đọc)
        with tab3:
            st.subheader("📢 Kênh thông báo từ Quản trị viên (1:N Channel)")
            st.warning("🔒 Chế độ: Chỉ có Admin hệ thống mới được quyền gửi tin nhắn tại đây.")
            
            # Hiển thị các thông báo hệ thống mang tính chất 1:N
            st.info("📣 **[Admin System]:** Hệ thống sẽ bảo trì nâng cấp tính năng Voice/Video Call (Phần 2) vào lúc 24h đêm nay!")
            st.info("📣 **[Sự kiện]:** Tuần lễ Valentine - Tăng tỷ lệ Quẹt Match thành công lên 90%!")