import streamlit as st
import database
import pandas as pd

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

        h1, h2, h3, p, label {
            color: white !important;
        }
        
        div.stDataFrame {
            background-color: rgba(255, 255, 255, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def app():
    add_dark_bg()

    st.markdown("<h1 style='text-align:center;'>Activity Logs</h1>", unsafe_allow_html=True)
    st.subheader("View history of all security activities")

    if st.button("🗑️ Clear All Logs"):
        if database.clear_logs():
            st.success("All logs have been cleared!")
            st.rerun()
        else:
            st.error("Failed to clear logs.")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Phishing Logs", 
        "Malware Logs", 
        "Login Attempts", 
        "Encryption Logs",
        "Decryption Logs",
        "IP Spoofing Logs"
    ])

    with tab1:
        st.header("🎣 Phishing Detection Logs")
        logs = database.get_logs("phishing_logs")
        st.dataframe(pd.DataFrame(logs), use_container_width=True)

    with tab2:
        st.header("🦠 Malware Analysis Logs")
        logs = database.get_logs("malware_logs")
        st.dataframe(pd.DataFrame(logs), use_container_width=True)

    with tab3:
        st.header("🔐 Login Attempts (Brute Force)")
        logs = database.get_logs("login_attempts")
        st.dataframe(pd.DataFrame(logs), use_container_width=True)

    with tab4:
        st.header("🔒 File Encryption Logs")
        logs = database.get_logs("encryption_logs")
        if logs:
            st.dataframe(pd.DataFrame(logs), use_container_width=True)
        else:
            st.write("No logs found yet.")

    with tab5:
        st.header("🔓 File Decryption Logs")
        logs = database.get_logs("decryption_logs")
        if logs:
            st.dataframe(pd.DataFrame(logs), use_container_width=True)
        else:
            st.write("No logs found yet.")

    with tab6:
        st.header("🛰️ IP Spoofing Detection Logs")
        logs = database.get_logs("ip_spoofing_logs")
        if logs:
            st.dataframe(pd.DataFrame(logs), use_container_width=True)
        else:
            st.write("No logs found yet.")


if __name__ == "__main__":
    app()
