import streamlit as st
import json
import os
import hashlib
from datetime import datetime

# ---- HÀM LƯU/TẢI DỮ LIỆU ----
DATA_FILE = "users_data.json"

def hash_password(password):
    """Mã hóa mật khẩu"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users_data():
    """Load dữ liệu người dùng từ file JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"users": [], "friends": {}}
    return {"users": [], "friends": {}}

def save_users_data(data):
    """Lưu dữ liệu người dùng vào file JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_user(username, password):
    """Thêm người dùng mới (chỉ tên đăng nhập và mật khẩu)"""
    data = load_users_data()
    # Kiểm tra tên đăng nhập đã tồn tại chưa
    if any(u["username"] == username for u in data["users"]):
        return False, "❌ Tên đăng nhập này đã được sử dụng!"
    
    new_user = {
        "username": username,
        "password": hash_password(password),
        "name": None,
        "age": None,
        "gender": None,
        "bio": None,
        "profile_created": False,
        "logged_in": False
    }
    data["users"].append(new_user)
    data["friends"][username] = []
    save_users_data(data)
    return True, "✅ Tạo tài khoản thành công!"

def login_user(username, password):
    """Đăng nhập người dùng (kiểm tra tên và mật khẩu)"""
    data = load_users_data()
    user = next((u for u in data["users"] if u["username"] == username), None)
    if user:
        if user["password"] == hash_password(password):
            return True, user
        else:
            return False, None
    return False, None

def update_user_profile(username, name, age, gender, bio):
    """Cập nhật thông tin profile của người dùng"""
    data = load_users_data()
    user = next((u for u in data["users"] if u["username"] == username), None)
    if user:
        user["name"] = name
        user["age"] = age
        user["gender"] = gender
        user["bio"] = bio
        user["profile_created"] = True
        user["logged_in"] = True
        save_users_data(data)
        return True
    return False

def logout_user():
    """Đăng xuất người dùng"""
    st.session_state.user_profile = None
    st.session_state.matched_user = None

def load_private_messages(chat_key):
    """Load tin nhắn riêng tư (1:1) từ file JSON"""
    data = load_users_data()
    if "messages" not in data:
        data["messages"] = {}
    return data.get("messages", {}).get(chat_key, [])

def save_private_message(chat_key, sender, text, msg_type="text"):
    """Lưu tin nhắn riêng tư (1:1) vào file JSON"""
    from datetime import datetime
    data = load_users_data()
    if "messages" not in data:
        data["messages"] = {}
    
    if chat_key not in data["messages"]:
        data["messages"][chat_key] = []
    
    message = {
        "sender": sender,
        "text": text,
        "type": msg_type,
        "timestamp": datetime.now().isoformat()
    }
    data["messages"][chat_key].append(message)
    save_users_data(data)
    return True

def load_group_messages():
    """Load global group (N-N) messages from file"""
    data = load_users_data()
    if "group_messages" not in data:
        data["group_messages"] = []
    return data.get("group_messages", [])

def save_group_message(sender, text, msg_type="text"):
    """Save a message to the global group chat"""
    from datetime import datetime
    data = load_users_data()
    if "group_messages" not in data:
        data["group_messages"] = []
    msg = {
        "sender": sender,
        "text": text,
        "type": msg_type,
        "timestamp": datetime.now().isoformat()
    }
    data["group_messages"].append(msg)
    save_users_data(data)
    return True

def load_calls(chat_key):
    """Load lịch sử cuộc gọi từ file JSON"""
    data = load_users_data()
    if "calls" not in data:
        data["calls"] = {}
    return data.get("calls", {}).get(chat_key, [])

def save_call_record(chat_key, caller, call_type, duration=0):
    """Lưu ghi chép cuộc gọi vào file JSON"""
    from datetime import datetime
    data = load_users_data()
    if "calls" not in data:
        data["calls"] = {}
    
    if chat_key not in data["calls"]:
        data["calls"][chat_key] = []
    
    call_record = {
        "caller": caller,
        "type": call_type,  # "voice" hoặc "video"
        "duration": duration,
        "timestamp": datetime.now().isoformat()
    }
    data["calls"][chat_key].append(call_record)
    save_users_data(data)

# 1. Khởi tạo dữ liệu (sử dụng setdefault để tránh AttributeError)
st.session_state.setdefault("user_profile", None)
st.session_state.setdefault("matched_user", None)
st.session_state.setdefault("messages_nn", [
    {"sender": "Hệ thống", "text": "👋 Chào mừng! Bạn có thể kết bạn để chat chung hoặc chat riêng với bạn bè. Hãy chọn bạn ở phần bên trái nhé!", "type": "system"}
])
st.session_state.setdefault("messages_11", {})
st.session_state.setdefault("active_call", {})
st.session_state.setdefault("call_duration", 0)
st.session_state.setdefault("active_video_call", {})
st.session_state.setdefault("pending_upload_nn", {"image": None, "file": None, "audio": None})
st.session_state.setdefault("pending_upload_11", {})
st.session_state.setdefault("uploaded_image_nn_id", None)
st.session_state.setdefault("uploaded_image_11_id", {})
st.session_state.setdefault("user_friends", {})

# Load dữ liệu từ file
data = load_users_data()
if "all_users" not in st.session_state:
    if data["users"]:
        st.session_state.all_users = data["users"]
    else:
        # Tài khoản mẫu
        st.session_state.all_users = [
            {"username": "linh", "password": hash_password("123456"), "name": "Linh", "age": 22, "bio": "Thích du lịch, mê trà sữa 🧋", "gender": "Nữ", "logged_in": False, "profile_created": True},
            {"username": "minh", "password": hash_password("123456"), "name": "Minh", "age": 25, "bio": "Kỹ sư phần mềm, thích nuôi mèo 🐱", "gender": "Nam", "logged_in": False, "profile_created": True},
        ]

# Load danh sách bạn từ file
if "file_friends" not in st.session_state:
    st.session_state.file_friends = data.get("friends", {})

# Khởi tạo biến để lưu username của người dùng hiện tại
if "current_username" not in st.session_state:
    st.session_state.current_username = None

st.set_page_config(page_title="Dating Chat App", page_icon="❤️", layout="wide")
st.title("❤️ Ứng Dụng Hẹn Hò Siêu Tốc (Realtime Dating Chat)")

# ---- PHẦN ĐĂNG NHẬP / TẠO PROFILE ----
if not st.session_state.user_profile:
    st.subheader("🔐 Đăng nhập hoặc Tạo tài khoản mới")
    
    tab_login, tab_register = st.tabs(["🔑 Đăng nhập", "✍️ Tạo tài khoản"])
    
    with tab_login:
        st.write("**Nhập tên đăng nhập và mật khẩu**")
        login_username = st.text_input("Tên đăng nhập:", key="login_username", placeholder="Ví dụ: linh, minh...")
        login_password = st.text_input("Mật khẩu:", type="password", key="login_password", placeholder="Nhập mật khẩu của bạn")
        
        if st.button("🔑 Đăng nhập", key="login_btn", use_container_width=True):
            if login_username and login_password:
                success, user = login_user(login_username, login_password)
                if success and user:
                    st.session_state.user_profile = user
                    st.session_state.current_username = user["username"]
                    # Load danh sách bạn của user này
                    if user["username"] in st.session_state.file_friends:
                        st.session_state.user_friends[user["username"]] = st.session_state.file_friends[user["username"]]
                    else:
                        st.session_state.user_friends[user["username"]] = []
                    
                    # Nếu profile chưa tạo, chuyển hướng đến setup profile
                    if not user.get("profile_created") or not user.get("name"):
                        st.success("✅ Đăng nhập thành công! Hãy hoàn tất hồ sơ của bạn.")
                        st.rerun()
                    else:
                        st.success(f"✅ Chào {user['name']}! 👋")
                        st.rerun()
                else:
                    st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng!")
            else:
                st.error("❌ Vui lòng nhập tên đăng nhập và mật khẩu!")
    
    with tab_register:
        st.write("**Tạo tài khoản mới**")
        st.info("💡 Sau khi tạo tài khoản, bạn sẽ điền thông tin hồ sơ để bắt đầu hẹn hò")
        
        new_username = st.text_input("Tên đăng nhập:", key="register_username", placeholder="Ví dụ: linh123, minh456...")
        new_password = st.text_input("Mật khẩu:", type="password", key="register_password", placeholder="Tối thiểu 6 ký tự")
        new_password_confirm = st.text_input("Nhập lại mật khẩu:", type="password", key="register_password_confirm", placeholder="Xác nhận mật khẩu")
        
        if st.button("✍️ Tạo tài khoản", key="register_btn", use_container_width=True):
            if not new_username or not new_password:
                st.error("❌ Vui lòng nhập tên đăng nhập và mật khẩu!")
            elif len(new_password) < 6:
                st.error("❌ Mật khẩu phải có ít nhất 6 ký tự!")
            elif new_password != new_password_confirm:
                st.error("❌ Mật khẩu nhập lại không khớp!")
            else:
                success, message = add_user(new_username, new_password)
                if success:
                    st.success(message)
                    st.info("💡 Giờ hãy đăng nhập với tài khoản vừa tạo")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

# Sau khi đăng nhập, kiểm tra nếu profile chưa hoàn tất
elif st.session_state.user_profile and (not st.session_state.user_profile.get("profile_created") or not st.session_state.user_profile.get("name")):
    st.subheader(f"📝 Hoàn tất hồ sơ hẹn hò của bạn")
    st.write(f"Tên đăng nhập: **{st.session_state.user_profile['username']}**")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        profile_name = st.text_input("Tên hiển thị:", value=st.session_state.user_profile.get("name", ""), key="setup_name")
        profile_age = st.number_input("Tuổi:", min_value=18, max_value=50, value=st.session_state.user_profile.get("age", 20), key="setup_age")
    
    with col2:
        default_gender = st.session_state.user_profile.get("gender") or "Nam"
        gender_options = ["Nam", "Nữ", "Khác"]
        gender_index = gender_options.index(default_gender) if default_gender in gender_options else 0
        profile_gender = st.selectbox("Giới tính:", gender_options, key="setup_gender", index=gender_index)
    
    profile_bio = st.text_area("Giới thiệu bản thân (Bio):", value=st.session_state.user_profile.get("bio", ""), key="setup_bio", height=100)
    
    col_submit, col_logout = st.columns(2)
    with col_submit:
        if st.button("✅ Hoàn tất & Vào Hẹn Hò", use_container_width=True, key="setup_submit"):
            if profile_name and profile_bio:
                # Cập nhật profile
                success = update_user_profile(
                    st.session_state.user_profile["username"],
                    profile_name,
                    profile_age,
                    profile_gender,
                    profile_bio
                )
                if success:
                    # Cập nhật session state
                    st.session_state.user_profile["name"] = profile_name
                    st.session_state.user_profile["age"] = profile_age
                    st.session_state.user_profile["gender"] = profile_gender
                    st.session_state.user_profile["bio"] = profile_bio
                    st.session_state.user_profile["profile_created"] = True
                    st.success(f"✅ Chào {profile_name}! Vào hẹn hò thôi! 🎉")
                    st.rerun()
            else:
                st.error("❌ Vui lòng điền đầy đủ thông tin!")
    
    with col_logout:
        if st.button("🚪 Đăng xuất", use_container_width=True, key="setup_logout"):
            logout_user()
            st.success("✅ Đã đăng xuất")
            st.rerun()
else:
    # Giao diện chính sau khi đăng nhập và setup profile hoàn tất
    current_username = st.session_state.current_username or st.session_state.user_profile['username']
    
    # Luôn load lại danh sách bạn từ file để đồng bộ
    st.session_state.file_friends = load_users_data().get("friends", {})
    st.session_state.all_users = load_users_data()["users"]
    
    # Tính DATING_POOL mỗi lần page load (không phải global)
    DATING_POOL = [u for u in st.session_state.all_users if u.get("profile_created", False) and u.get("name")]
    
    st.sidebar.header(f"👤 {st.session_state.user_profile['name']} ({st.session_state.user_profile['age']})")
    st.sidebar.write(f"ℹ️ {st.session_state.user_profile['bio']}")
    st.sidebar.write(f"🔐 Đăng nhập: {current_username}")
    
    if st.sidebar.button("🚪 Đăng xuất"):
        # Lưu danh sách bạn vào file trước khi đăng xuất
        data = load_users_data()
        data.setdefault("friends", {})
        if current_username in st.session_state.user_friends:
            data["friends"][current_username] = st.session_state.user_friends[current_username]
        save_users_data(data)
        
        logout_user()
        st.session_state.current_username = None
        st.success("✅ Đã đăng xuất. Tạm biệt! 👋")
        st.rerun()

    # Auto-refresh client-side mỗi 2 giây để cập nhật tin nhắn real-time
    st.markdown("""
    <script>
        const INTERVAL = 2000;
        // Only refresh when user is logged in (the server serves this snippet only when logged-in)
        setInterval(() => { window.location.reload(); }, INTERVAL);
    </script>
    """, unsafe_allow_html=True)

    # CHIA GIAO DIỆN THÀNH 2 CỘT
    col1, col2 = st.columns([1, 2])

    # ---- PHẦN 1: KẾT BẠN ----
    with col1:
        st.header("👥 Kết Bạn")
        # Lọc những người không phải là chính mình
        other_users = [u for u in DATING_POOL if u['name'] != st.session_state.user_profile['name']]
        
        # Khởi tạo danh sách bạn từ file nếu chưa có
        if current_username not in st.session_state.user_friends:
            st.session_state.user_friends[current_username] = st.session_state.file_friends.get(current_username, [])
        
        user_friends = st.session_state.user_friends[current_username]
        st.info(f"👨‍👩‍👧‍👦 Bạn bè: {len(user_friends)} người | Có sẵn: {len(other_users)} người")
        
        # Chọn xem danh sách: Bạn bè hay Tìm kiếm
        tab_friends, tab_search = st.tabs(["👫 Bạn bè của tôi", "🔍 Tìm kiếm"])
        
        with tab_friends:
            st.subheader("Danh sách bạn bè của tôi")
            if user_friends:
                for friend_name in user_friends:
                    # Tìm thông tin bạn bè từ danh sách
                    friend_info = next((u for u in st.session_state.all_users if u['name'] == friend_name), None)
                    if friend_info:
                        with st.expander(f"👤 {friend_info['name']} ({friend_info['age']} tuổi) - {friend_info['gender']}"):
                            st.write(f"**Bio:** {friend_info['bio']}")
                            st.write(f"**Trạng thái:** {'🟢 Online' if friend_info['logged_in'] else '🔴 Offline'}")
                            
                            col_chat, col_remove = st.columns([2, 1])
                            with col_chat:
                                st.caption("💬 Chọn bạn này ở tab 'Chat Riêng' bên phải để trò chuyện")
                            
                            with col_remove:
                                if st.button(f"❌ Xóa", key=f"remove_friend_{friend_name}"):
                                    user_friends.remove(friend_name)
                                    st.session_state.matched_user = None
                                    st.session_state.user_friends[current_username] = user_friends
                                    st.session_state.file_friends[current_username] = user_friends
                                    # Lưu vào file ngay lập tức
                                    data = load_users_data()
                                    data.setdefault("friends", {})
                                    data["friends"][current_username] = user_friends
                                    save_users_data(data)
                                    st.success(f"❌ Đã xóa {friend_name} khỏi danh sách bạn")
                                    st.rerun()
            else:
                st.warning("Bạn chưa có bạn nào. Hãy kết bạn ở tab 'Tìm kiếm'!")
        
        with tab_search:
            st.subheader("🔍 Tìm kiếm và kết bạn")
            
            # Thanh tìm kiếm
            search_query = st.text_input("🔎 Nhập tên để tìm kiếm:", placeholder="Ví dụ: Linh, Minh...")
            
            # Hiển thị những người chưa là bạn
            non_friends = [u for u in other_users if u['name'] not in user_friends]
            
            # Lọc theo từ khóa tìm kiếm
            if search_query.strip():
                filtered_users = [u for u in non_friends if search_query.lower() in u['name'].lower()]
            else:
                filtered_users = non_friends
            
            if filtered_users:
                st.write(f"📌 Tìm thấy **{len(filtered_users)}** kết quả")
                for user in filtered_users:
                    with st.expander(f"👤 {user['name']} ({user['age']} tuổi) - {user['gender']}"):
                        st.write(f"**Bio:** {user['bio']}")
                        st.write(f"**Trạng thái:** {'🟢 Online' if user['logged_in'] else '🔴 Offline'}")
                        
                        col_add = st.columns([1])[0]
                        
                        with col_add:
                            if st.button(f"➕ Kết bạn", key=f"add_friend_{user['name']}"):
                                if user['name'] not in user_friends:
                                    user_friends.append(user['name'])
                                    st.session_state.user_friends[current_username] = user_friends
                                    st.session_state.file_friends[current_username] = user_friends
                                    # Lưu vào file ngay lập tức
                                    data = load_users_data()
                                    data.setdefault("friends", {})
                                    data["friends"][current_username] = user_friends
                                    save_users_data(data)
                                    st.success(f"✅ Đã kết bạn với {user['name']}")
                                    st.rerun()
                                else:
                                    st.warning(f"⚠️ Bạn đã là bạn của {user['name']} rồi!")
            else:
                if search_query.strip():
                    st.warning(f"❌ Không tìm thấy ai có tên chứa '{search_query}'")
                else:
                    if non_friends:
                        st.info(f"💡 Hiển thị tất cả {len(non_friends)} người chưa là bạn. Nhập tên để tìm kiếm!")
                    else:
                        st.info("✅ Bạn đã kết bạn với tất cả mọi người!")

    # ---- PHẦN 2: CÁC KHÔNG GIAN CHAT (1:1, 1:N, N-N) ----
    with col2:
        tab1, tab2, tab3 = st.tabs(["💬 Sảnh Chung (Chat N-N)", "🔒 Chat Riêng (Chat 1:1)", "📢 Thông Báo (Kênh 1:N)"])

        # TAB 1: CHAT N-N (Tất cả mọi người cùng chat ở sảnh chờ)
        with tab1:
            st.subheader("🌐 Sảnh chờ chung (N-N Chat)")
            
            # ---- HIỂN THỊ CHAT N-N (load từ file và lọc theo danh sách bạn) ----
            chat_container_nn = st.container(height=300)
            group_msgs = load_group_messages()
            # Danh sách tên bạn (hiển thị chỉ các tin nhắn từ bạn bè hoặc chính bạn)
            friend_names = st.session_state.user_friends.get(current_username, [])
            for msg in group_msgs:
                sender = msg.get('sender')
                if msg.get('type') == 'system' or sender == st.session_state.user_profile.get('name') or sender in friend_names:
                    if msg.get("type") == "system":
                        chat_container_nn.info(msg['text'])
                    elif msg.get("type") == "image":
                        chat_container_nn.write(f"**{msg['sender']}:**")
                        # For group images we only store filename; display filename
                        chat_container_nn.write(f"[Hình ảnh] {msg.get('text')}")
                    elif msg.get("type") == "audio":
                        chat_container_nn.write(f"**{msg['sender']}:** 🎤 Tin nhắn thoại")
                        chat_container_nn.write(msg.get('text'))
                    elif msg.get("type") == "file":
                        chat_container_nn.write(f"**{msg['sender']}:** 📎 {msg.get('text')}")
                    else:
                        chat_container_nn.write(f"**{msg['sender']}:** {msg['text']}")
            
            st.divider()
            
            # ---- Nút video call sảnh chung ----
            col_header_left, col_header_right = st.columns([4, 1])
            with col_header_right:
                video_call_nn_key = "video_call_nn"
                if video_call_nn_key not in st.session_state.active_video_call:
                    st.session_state.active_video_call[video_call_nn_key] = False
                
                if not st.session_state.active_video_call[video_call_nn_key]:
                    if st.button("📹 Gửi video", key="btn_video_nn", use_container_width=True):
                        st.session_state.active_video_call[video_call_nn_key] = True
                        st.success("📹 Quét video sảnh chung được bật động!")
                        st.rerun()
                else:
                    if st.button("❌ Kết thúc video", key="btn_end_video_nn", use_container_width=True):
                        st.session_state.active_video_call[video_call_nn_key] = False
                        st.session_state.messages_nn.append({
                            "sender": "Hệ thống",
                            "text": "[Quét video sảnh chung đã kết thúc]",
                            "type": "system"
                        })
                        st.rerun()
            
            # ---- FORM GỬI TIN NHẮN VÀ TẬP TIN N-N ----
            with st.form(key="form_msg_nn", clear_on_submit=True):
                col_input, col_img, col_file, col_audio, col_send = st.columns([4, 0.8, 0.8, 0.8, 0.8])
                
                user_msg_nn = ""
                uploaded_image_nn = None
                uploaded_file_nn = None
                audio_bytes_nn = None
                submit_clicked = False
                
                # Ô nhập tin nhắn chiếm nhiều không gian
                with col_input:
                    user_msg_nn = st.text_input(
                        "",
                        placeholder="💬 Gõ tin nhắn...",
                        label_visibility="collapsed",
                        key="msg_nn_input"
                    )
                
                # Popover ảnh
                with col_img:
                    with st.popover("📷", use_container_width=True):
                        uploaded_image_nn = st.file_uploader(
                            "Chọn ảnh:",
                            type=["png", "jpg", "jpeg", "gif"],
                            key="img_nn",
                            label_visibility="collapsed"
                        )
                        if uploaded_image_nn and uploaded_image_nn.name != st.session_state.uploaded_image_nn_id:
                            st.session_state.pending_upload_nn["image"] = uploaded_image_nn
                            st.session_state.uploaded_image_nn_id = uploaded_image_nn.name
                
                # Popover tệp
                with col_file:
                    with st.popover("📁", use_container_width=True):
                        uploaded_file_nn = st.file_uploader(
                            "Chọn tệp:",
                            key="file_nn",
                            label_visibility="collapsed"
                        )
                        if uploaded_file_nn:
                            st.session_state.pending_upload_nn["file"] = uploaded_file_nn
                
                # Popover âm thanh
                with col_audio:
                    with st.popover("🎤", use_container_width=True):
                        audio_bytes_nn = st.audio_input(
                            "Ghi âm:",
                            key="audio_nn",
                            label_visibility="collapsed"
                        )
                        if audio_bytes_nn:
                            st.session_state.pending_upload_nn["audio"] = audio_bytes_nn
                
                # Nút gửi
                with col_send:
                    submit_clicked = st.form_submit_button("↩️", use_container_width=True, help="Gửi (Enter)")
            
            # Xử lý submission bên ngoài form (lưu vào file group)
            if submit_clicked and user_msg_nn:
                save_group_message(st.session_state.user_profile['name'], user_msg_nn, "text")
                st.success("✅ Đã gửi tin nhắn vào sảnh chung")
                st.rerun()
            
            # Xử lý hình ảnh được lưu trong pending_upload
            if st.session_state.pending_upload_nn["image"] is not None:
                img = st.session_state.pending_upload_nn["image"]
                # Lưu tên file vào group messages
                save_group_message(st.session_state.user_profile['name'], f"📷 {img.name}", "image")
                st.session_state.pending_upload_nn["image"] = None
                st.session_state.uploaded_image_nn_id = None
                st.success("✅ Đã gửi hình ảnh vào sảnh chung")
                st.rerun()
            
            # Xử lý tệp được lưu trong pending_upload
            if st.session_state.pending_upload_nn["file"] is not None:
                f = st.session_state.pending_upload_nn["file"]
                save_group_message(st.session_state.user_profile['name'], f"📎 {f.name}", "file")
                st.session_state.pending_upload_nn["file"] = None
                st.success("✅ Đã gửi tệp vào sảnh chung")
                st.rerun()
            
            # Xử lý âm thanh được lưu trong pending_upload
            if st.session_state.pending_upload_nn["audio"] is not None:
                audio = st.session_state.pending_upload_nn["audio"]
                save_group_message(st.session_state.user_profile['name'], "🎤 Tin nhắn thoại", "audio")
                st.session_state.pending_upload_nn["audio"] = None
                st.success("✅ Đã gửi tin nhắn thoại vào sảnh chung")
                st.rerun()

        # TAB 2: CHAT 1:1 (Chỉ chat được khi đã MATCH thành công)
        with tab2:
            st.subheader("🔒 Trò chuyện riêng tư (1:1 Chat)")
            
            # Nút làm mới để cập nhật tin nhắn mới
            col_refresh, col_spacer = st.columns([0.15, 0.85])
            with col_refresh:
                if st.button("🔄 Làm mới", help="Nhấn để tải tin nhắn mới"):
                    st.rerun()
            
            # Hiển thị danh sách bạn bè để chọn chat
            if user_friends:
                st.write("**Chọn một bạn để chat riêng:**")
                selected_friend = st.selectbox("👥 Bạn bè của tôi:", user_friends, key="friend_selector_11")
                
                if selected_friend:
                    # Tạo khoá chat unified (sorted để cả 2 bên đều dùng khoá giống nhau)
                    chat_key = "_".join(sorted([st.session_state.user_profile['name'], selected_friend]))
                    
                    # Load tin nhắn từ file JSON
                    if chat_key not in st.session_state.messages_11:
                        st.session_state.messages_11[chat_key] = load_private_messages(chat_key)
                    
                    # Khởi tạo pending_upload nếu chưa có
                    if chat_key not in st.session_state.pending_upload_11:
                        st.session_state.pending_upload_11[chat_key] = {"image": None, "file": None, "audio": None}
                    
                    # ---- PHẦN CUỘC GỌI (Voice/Video Call) ----
                    call_key = f"call_{chat_key}"
                    video_call_key = f"video_call_{chat_key}"
                    col_call1, col_call2, col_call3, col_call4 = st.columns(4)
                    
                    if call_key not in st.session_state.active_call:
                        st.session_state.active_call[call_key] = False
                    
                    with col_call1:
                        if not st.session_state.active_call[call_key]:
                            if st.button("📞 Gọi thoại", key=f"voice_call_{chat_key}"):
                                st.session_state.active_call[call_key] = True
                                # Lưu ghi chép cuộc gọi vào file
                                save_call_record(chat_key, st.session_state.user_profile['name'], "voice")
                                st.success(f"📞 Đang gọi {selected_friend}... Chờ phía bên kia trả lời.")
                                st.rerun()
                        else:
                            if st.button("❌ Kết thúc cuộc gọi", key=f"end_call_{chat_key}"):
                                st.session_state.active_call[call_key] = False
                                st.session_state.messages_11[chat_key].append(
                                    {"sender": "Hệ thống", "text": f"[Cuộc gọi thoại kết thúc]", "type": "system"}
                                )
                                # Lưu tin nhắn hệ thống vào file
                                save_private_message(chat_key, "Hệ thống", "[Cuộc gọi thoại kết thúc]", "system")
                                st.rerun()
                    
                    with col_call2:
                        if video_call_key not in st.session_state.active_video_call:
                            st.session_state.active_video_call[video_call_key] = False
                        
                        if not st.session_state.active_video_call[video_call_key]:
                            if st.button("📹 Video", key=f"video_call_start_{chat_key}"):
                                st.session_state.active_video_call[video_call_key] = True
                                # Lưu ghi chép cuộc gọi video vào file
                                save_call_record(chat_key, st.session_state.user_profile['name'], "video")
                                st.success(f"📹 Đang gửi video cho {selected_friend}... Chờ trả lời.")
                                st.rerun()
                        else:
                            if st.button("❌ Kết thúc", key=f"video_call_end_{chat_key}"):
                                st.session_state.active_video_call[video_call_key] = False
                                st.session_state.messages_11[chat_key].append(
                                    {"sender": "Hệ thống", "text": f"[Cuộc gọi video kết thúc]", "type": "system"}
                                )
                                # Lưu tin nhắn hệ thống vào file
                                save_private_message(chat_key, "Hệ thống", "[Cuộc gọi video kết thúc]", "system")
                                st.rerun()
                    
                    with col_call3:
                        if st.session_state.active_call[call_key]:
                            st.warning("🔴 Thoại...")
                        elif st.session_state.active_video_call.get(video_call_key, False):
                            st.warning("🔴 Video...")
                        else:
                            st.caption("Bấm để gửi")
                    
                    with col_call4:
                        pass
                    
                    st.divider()
                    
                    # ---- HIỂN THỊ CHAT ----
                    chat_container_11 = st.container(height=250)
                    
                    # Load lại tin nhắn từ file JSON mỗi lần (để đồng bộ real-time)
                    current_messages = load_private_messages(chat_key)
                    
                    # Hiển thị lịch sử chat 1:1
                    for msg in current_messages:
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
                    with st.form(key=f"form_msg_{chat_key}", clear_on_submit=True):
                        col_input, col_img, col_file, col_audio, col_send = st.columns([4, 0.8, 0.8, 0.8, 0.8])
                        
                        user_msg_11 = ""
                        uploaded_image = None
                        uploaded_file = None
                        audio_bytes = None
                        submit_clicked_11 = False
                        
                        # Ô nhập tin nhắn chiếm nhiều không gian
                        with col_input:
                            user_msg_11 = st.text_input(
                                "",
                                placeholder="💬 Gõ tin nhắn...",
                                label_visibility="collapsed",
                                key=f"msg_{chat_key}_input"
                            )
                        
                        # Popover ảnh
                        with col_img:
                            with st.popover("📷", use_container_width=True):
                                uploaded_image = st.file_uploader(
                                    "Chọn ảnh:",
                                    type=["png", "jpg", "jpeg", "gif"],
                                    key=f"img_{chat_key}",
                                    label_visibility="collapsed"
                                )
                                if uploaded_image and uploaded_image.name != st.session_state.uploaded_image_11_id.get(chat_key):
                                    st.session_state.pending_upload_11[chat_key]["image"] = uploaded_image
                                    st.session_state.uploaded_image_11_id[chat_key] = uploaded_image.name
                        
                        # Popover tệp
                        with col_file:
                            with st.popover("📁", use_container_width=True):
                                uploaded_file = st.file_uploader(
                                    "Chọn tệp:",
                                    key=f"file_{chat_key}",
                                    label_visibility="collapsed"
                                )
                                if uploaded_file:
                                    st.session_state.pending_upload_11[chat_key]["file"] = uploaded_file
                        
                        # Popover âm thanh
                        with col_audio:
                            with st.popover("🎤", use_container_width=True):
                                audio_bytes = st.audio_input(
                                    "Ghi âm:",
                                    key=f"audio_{chat_key}",
                                    label_visibility="collapsed"
                                )
                                if audio_bytes:
                                    st.session_state.pending_upload_11[chat_key]["audio"] = audio_bytes
                        
                        # Nút gửi
                        with col_send:
                            submit_clicked_11 = st.form_submit_button("↩️", use_container_width=True, help="Gửi (Enter)")
                    
                    # Xử lý submission bên ngoài form
                    if submit_clicked_11 and user_msg_11:
                        st.session_state.messages_11[chat_key].append({"sender": st.session_state.user_profile['name'], "text": user_msg_11})
                        # Lưu vào file JSON
                        save_private_message(chat_key, st.session_state.user_profile['name'], user_msg_11, "text")
                        st.rerun()
                    
                    # Xử lý hình ảnh được lưu
                    if st.session_state.pending_upload_11[chat_key]["image"] is not None:
                        img = st.session_state.pending_upload_11[chat_key]["image"]
                        st.session_state.messages_11[chat_key].append({
                            "sender": st.session_state.user_profile['name'],
                            "type": "image",
                            "image_data": img,
                            "file_name": img.name
                        })
                        # Lưu vào file JSON (lưu tên file thôi, không lưu dữ liệu ảnh)
                        save_private_message(chat_key, st.session_state.user_profile['name'], f"📷 {img.name}", "image")
                        st.session_state.pending_upload_11[chat_key]["image"] = None
                        st.session_state.uploaded_image_11_id[chat_key] = None
                        st.success(f"✅ Đã gửi hình ảnh cho {selected_friend}")
                        st.rerun()
                    
                    # Xử lý tệp được lưu
                    if st.session_state.pending_upload_11[chat_key]["file"] is not None:
                        f = st.session_state.pending_upload_11[chat_key]["file"]
                        st.session_state.messages_11[chat_key].append({
                            "sender": st.session_state.user_profile['name'],
                            "type": "file",
                            "file_name": f.name,
                            "file_data": f.read()
                        })
                        # Lưu vào file JSON (lưu tên file thôi)
                        save_private_message(chat_key, st.session_state.user_profile['name'], f"📎 {f.name}", "file")
                        st.session_state.pending_upload_11[chat_key]["file"] = None
                        st.success(f"✅ Đã gửi tệp cho {selected_friend}")
                        st.rerun()
                    
                    # Xử lý âm thanh được lưu
                    if st.session_state.pending_upload_11[chat_key]["audio"] is not None:
                        audio = st.session_state.pending_upload_11[chat_key]["audio"]
                        st.session_state.messages_11[chat_key].append({
                            "sender": st.session_state.user_profile['name'],
                            "type": "audio",
                            "audio_data": audio
                        })
                        # Lưu vào file JSON (lưu thông báo lời nhắn thoại)
                        save_private_message(chat_key, st.session_state.user_profile['name'], "🎤 Tin nhắn thoại", "audio")
                        st.session_state.pending_upload_11[chat_key]["audio"] = None
                        st.success(f"✅ Đã gửi tin nhắn thoại cho {selected_friend}")
                        st.rerun()
            else:
                st.warning("⚠️ Bạn cần kết bạn với ai đó ở tab 'Tìm kiếm' trước!")

        # TAB 3: KÊNH 1:N (Chỉ Admin/Hệ thống gửi, Member chỉ đọc)
        with tab3:
            st.subheader("📢 Kênh thông báo từ Quản trị viên (1:N Channel)")
            st.warning("🔒 Chế độ: Chỉ có Admin hệ thống mới được quyền gửi tin nhắn tại đây.")
            
            # Hiển thị các thông báo hệ thống mang tính chất 1:N

            st.info("📣 **[Sự kiện]:** Tuần lễ Valentine - Tăng tỷ lệ Quẹt Match thành công lên 90%!")
