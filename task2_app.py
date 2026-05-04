import streamlit as st
import random
import base64

st.set_page_config(page_title="Guessing Game", page_icon="🎯")

# 🔥 Function to convert image to base64
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ⚠️ Use RAW string for Windows path
img_path = r"C:\Users\supra\OneDrive\Pictures\1000_F_224032170_7PfrDJYWjCw4Rs1WFvhPkiSPuD02sw1q.jpg"

bg_img = get_base64(img_path)

# 🎨 Apply background
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{bg_img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

h1, h2, h3 {{
    text-align: center;
    color: white;
    text-shadow: 2px 2px 10px black;
}}

.stButton>button {{
    background-color: #ff006e;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}}

</style>
""", unsafe_allow_html=True)

# 🎮 Title
st.markdown("<h1>🎮 Guess The Secret Number</h1>", unsafe_allow_html=True)
st.markdown("<h3>🚀 Beat the game in minimum attempts!</h3>", unsafe_allow_html=True)

# 🎯 Game logic
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False

st.markdown(f"### 🔢 Attempts: {st.session_state.attempts}")

guess = st.number_input("🎯 Enter your guess (1-100)", min_value=1, max_value=100, step=1)

if st.button("🚀 Submit Guess") and not st.session_state.game_over:
    st.session_state.attempts += 1

    if guess < st.session_state.number:
        st.error("📉 Too Low! Go Higher 🔼")
    elif guess > st.session_state.number:
        st.error("📈 Too High! Go Lower 🔽")
    else:
        st.balloons()
        st.success(f"🏆 You Won! Number was {st.session_state.number}")
        st.success(f"🎯 Total Attempts: {st.session_state.attempts}")
        st.session_state.game_over = True

# 🔄 Restart
if st.session_state.game_over:
    if st.button("🔄 Play Again"):
        st.session_state.number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False