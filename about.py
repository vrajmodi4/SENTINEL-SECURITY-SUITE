import streamlit as st

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

        h1, h2, h3, p, li {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- ABOUT PAGE ---------------- #

def app():
    add_dark_bg()

    st.markdown(
        "<h1 style='text-align:center;'>About Us</h1>",
        unsafe_allow_html=True
    )

    st.write(
        """
        We are a team that developed **Sentinel Security Suite** as part of a  
        **Real-Time Project** with the goal of providing multiple cybersecurity
        services on a **single unified platform**.

        ### Abstract
        The **Sentinel Security Suite** is an integrated, beginner-friendly **web-based** 
        cybersecurity educational tool designed to provide a hands-on learning experience. 
        It implements a multi-modular system that addresses core areas of digital security, 
        including phishing detection, malware analysis, brute force simulations, and encryption. 
        By bridging the gap between theoretical knowledge and practical application, this suite 
        offers a unified, interactive **web-based** interface that empowers users to detect 
        and mitigate digital risks effectively.

        ###  Services Offered
        - Phishing Detection  
        - Malware Analysis  
        - Brute Force Attack Detection  
        - File Encryption  
        - File Decryption  
        - IP Spoofing Detection  

        ###  Technology Used
        - Python  
        - Streamlit Framework  

        This tool helps users identify threats, protect data, and understand
        cybersecurity risks in a **simple, interactive, and user-friendly way**.

        ---
        ###  Acknowledgment
        We would like to express our sincere gratitude to **Prof. Nilesh Parmar** (Project Guide) and the 
        **Department of Computer Engineering of U.V. Patel College of Engineering** for their invaluable
        support and guidance in the development of this suite.
        """
    )
