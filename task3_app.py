import streamlit as st
import base64

st.set_page_config(page_title="Contact Manager", page_icon="📱")

# 🎨 Background
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_path = r"C:\Users\supra\OneDrive\Pictures\print-141437814.webp"
bg_img = get_base64(img_path)

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/webp;base64,{bg_img}");
    background-size: cover;
}}

h1 {{
    text-align: center;
    color: white;
    text-shadow: 2px 2px 10px black;
}}

.card {{
    background: rgba(0,0,0,0.6);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>📱 Smart Contact Manager</h1>", unsafe_allow_html=True)

# 📂 Initialize state
if "contacts" not in st.session_state:
    st.session_state.contacts = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# 👉 Prefill values
if "name_val" not in st.session_state:
    st.session_state.name_val = ""
if "phone_val" not in st.session_state:
    st.session_state.phone_val = ""
if "email_val" not in st.session_state:
    st.session_state.email_val = ""

# ➕ FORM
st.subheader("➕ Add / Edit Contact")

with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Name", value=st.session_state.name_val)
    phone = st.text_input("Phone", value=st.session_state.phone_val)
    email = st.text_input("Email", value=st.session_state.email_val)

    submit = st.form_submit_button(
        "Update Contact" if st.session_state.edit_index is not None else "Add Contact"
    )

    if submit:
        if name and phone and email:
            if st.session_state.edit_index is None:
                st.session_state.contacts.append({
                    "name": name,
                    "phone": phone,
                    "email": email
                })
                st.success("Contact Added!")
            else:
                idx = st.session_state.edit_index
                st.session_state.contacts[idx] = {
                    "name": name,
                    "phone": phone,
                    "email": email
                }
                st.session_state.edit_index = None
                st.success("Contact Updated!")

            # 🔄 Reset prefill values
            st.session_state.name_val = ""
            st.session_state.phone_val = ""
            st.session_state.email_val = ""

            st.rerun()
        else:
            st.error("Fill all fields")

# 📋 CONTACT LIST
st.subheader("📋 Contact List")

if st.session_state.contacts:
    for i, c in enumerate(st.session_state.contacts):
        st.markdown(f"""
        <div class="card">
            <b>👤 {c['name']}</b><br>
            📞 {c['phone']}<br>
            ✉ {c['email']}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # ✏ EDIT (prefill values)
        with col1:
            if st.button(f"✏ Edit {c['name']}", key=f"edit{i}"):
                st.session_state.edit_index = i
                st.session_state.name_val = c["name"]
                st.session_state.phone_val = c["phone"]
                st.session_state.email_val = c["email"]
                st.rerun()

        # ❌ DELETE
        with col2:
            if st.button(f"❌ Delete {c['name']}", key=f"del{i}"):
                st.session_state.contacts.pop(i)
                st.success("Deleted!")
                st.rerun()
else:
    st.info("No contacts yet")