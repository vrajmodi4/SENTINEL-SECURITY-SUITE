import streamlit as st
import time
import database

# ---------------- DARK BACKGROUND ---------------- #

def add_dark_bg():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(
                135deg,
                rgba(0, 0, 0, 0.95),
                rgba(10, 20, 40, 0.95)
            );
        }

        h1, h2, h3, p, li, label {
            color: white !important;
        }

        input {
            color: white !important;
            background-color: rgba(0,0,0,0.6) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
def add_dark_bg():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(
                135deg,
                rgba(0, 0, 0, 0.95),
                rgba(10, 20, 40, 0.95)
            );
        }

        /* -------- TEXT COLOR -------- */
        h1, h2, h3, p, label {
            color: white !important;
        }

        /* -------- BUTTON STYLE -------- */
        div.stButton > button {
            background-color: #1f6feb !important;   /* BLUE */
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 0.6em 1.2em;
            font-size: 16px;
            font-weight: 600;
        }

        div.stButton > button:hover {
            background-color: #1158c7 !important;   /* DARKER BLUE */
            color: white !important;
        }

        div.stButton > button:active {
            background-color: #0b3d91 !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------------- CONFIGURATION ---------------- #

# VALID_USERNAME = "admin"
# VALID_PASSWORD = "Admin@123"


MAX_ATTEMPTS = 3
TIME_WINDOW = 30  # seconds

# ---------------- STREAMLIT PAGE ---------------- #

def app():
    add_dark_bg()

    st.markdown(
        "<h1 style='text-align:center;'>Brute Force Attack Detection</h1>",
        unsafe_allow_html=True
    )

    st.subheader("Simulated login system with brute force detection")

    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
        st.session_state.start_time = time.time()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login Attempt"):
        current_time = time.time()

        # Reset attempts if time window exceeded
        if current_time - st.session_state.start_time > TIME_WINDOW:
            st.session_state.attempts = 0
            st.session_state.start_time = current_time

        # ✅ Correct login
        # Simulated login - all attempts now fail by default to focus on detection logic
        if False: # Was: username == VALID_USERNAME and password == VALID_PASSWORD:
            status = "Success"
            st.success("✅ Login Successful!")
            st.session_state.attempts = 0
            st.session_state.start_time = time.time()

        else:
            status = "Failed"
            st.session_state.attempts += 1

            if st.session_state.attempts >= MAX_ATTEMPTS:
                st.error("🚨 Brute Force Attack Detected!")
                st.write("Too many failed login attempts.")
            else:
                st.warning("❌ Login Failed")
                st.write(
                    f"Failed Attempts: {st.session_state.attempts}/{MAX_ATTEMPTS}"
                )

        # ✅ Save to database
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO login_attempts (username, status)
            VALUES (?, ?)
        """, (username, status))
        conn.commit()
        conn.close()

    st.markdown("---")
    st.caption(
        "⚠️ Educational simulation: demonstrates brute force detection logic."
    )
