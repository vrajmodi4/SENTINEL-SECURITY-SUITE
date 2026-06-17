import streamlit as st
import pandas as pd
import database
import plotly.express as px

# ---------------- CONFIG ---------------- #
ADMIN_USER = "admin"
ADMIN_PASS = "Admin@123"

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] == ADMIN_USER and st.session_state["password"] == ADMIN_PASS:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for username/password.
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

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
        div.stMetric {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 5px;
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
    
    st.markdown("<h1 style='text-align:center;'>🔐 Admin Dashboard</h1>", unsafe_allow_html=True)

    if not check_password():
        st.stop()  # Do not continue if check_password is not True.

    # --- ADMIN CONTENT STARTS HERE ---
    
    st.success("✅ Logged in as Admin")
    
    if st.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    # --- METRICS ---
    st.subheader("📊 Security Overview")
    
    # Fetch Data from MongoDB
    df_phishing = pd.DataFrame(database.get_logs("phishing_logs"))
    df_malware = pd.DataFrame(database.get_logs("malware_logs"))
    df_login = pd.DataFrame(database.get_logs("login_attempts"))
    df_spoofing = pd.DataFrame(database.get_logs("ip_spoofing_logs"))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        phishing_count = len(df_phishing[df_phishing['result'] == 'Phishing']) if not df_phishing.empty else 0
        st.metric("Detected Phishing URLs", phishing_count, delta_color="inverse")
        
    with col2:
        malware_count = len(df_malware[df_malware['result'] == 'Suspicious']) if not df_malware.empty else 0
        st.metric("Suspicious Files", malware_count, delta_color="inverse")
        
    with col3:
        failed_logins = len(df_login[df_login['status'] == 'Failed']) if not df_login.empty else 0
        st.metric("Failed Login Attempts", failed_logins, delta_color="inverse")
 
    with col4:
        spoofing_count = len(df_spoofing[df_spoofing['status'] == 'Spoofed']) if not df_spoofing.empty else 0
        st.metric("IP Spoofing Alerts", spoofing_count, delta_color="inverse")
 
    st.markdown("---")
 
    # --- CHARTS ---
    st.subheader("📈 Threat Analysis")
    
    tab_charts, tab_logs = st.tabs(["Visualizations", "Raw Logs"])
    
    with tab_charts:
        c1, c2, c3 = st.columns(3)
        
        with c1:
            if not df_phishing.empty:
                fig_phishing = px.pie(df_phishing, names='result', title='Phishing Scan Results', 
                                      color_discrete_map={'Phishing':'red', 'Legitimate':'green'})
                st.plotly_chart(fig_phishing, use_container_width=True)
            else:
                st.info("No phishing data available.")
                
        with c2:
            if not df_malware.empty:
                fig_malware = px.pie(df_malware, names='result', title='Malware Scan Results',
                                     color_discrete_map={'Suspicious':'red', 'Safe':'green'})
                st.plotly_chart(fig_malware, use_container_width=True)
            else:
                st.info("No malware data available.")
 
        with c3:
            if not df_spoofing.empty:
                fig_spoofing = px.pie(df_spoofing, names='status', title='IP Spoofing Results',
                                      color_discrete_map={'Spoofed':'red', 'Legitimate':'green'})
                st.plotly_chart(fig_spoofing, use_container_width=True)
            else:
                st.info("No spoofing data available.")
 
    # --- LOGS ---
    with tab_logs:
        log_type = st.selectbox("Select Log Type", 
                                ["Phishing Logs", "Malware Logs", "Login Attempts", "Encryption Logs", "Decryption Logs", "IP Spoofing Logs"])
        
        if log_type == "Phishing Logs":
            st.dataframe(df_phishing, use_container_width=True)
            
        elif log_type == "Malware Logs":
            st.dataframe(df_malware, use_container_width=True)
            
        elif log_type == "Login Attempts":
            st.dataframe(df_login, use_container_width=True)
            
        elif log_type == "Encryption Logs":
            df_enc = pd.DataFrame(database.get_logs("encryption_logs"))
            st.dataframe(df_enc, use_container_width=True)
            
        elif log_type == "Decryption Logs":
            df_dec = pd.DataFrame(database.get_logs("decryption_logs"))
            st.dataframe(df_dec, use_container_width=True)
 
        elif log_type == "IP Spoofing Logs":
            st.dataframe(df_spoofing, use_container_width=True)


if __name__ == "__main__":
    app()
