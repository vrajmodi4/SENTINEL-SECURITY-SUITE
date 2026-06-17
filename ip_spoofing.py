import streamlit as st
import database
import random

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

        h1, h2, h3, p, label, li {
            color: white !important;
        }

        div.stButton > button {
            background-color: #1f6feb !important;
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 0.6em 1.2em;
            font-size: 16px;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- LOGIC ---------------- #

def detect_spoofing(packet_ip, real_ip):
    if packet_ip == real_ip:
        return "Legitimate", "✅ Source IP matches. No spoofing detected."
    else:
        return "Spoofed", "🚨 IP Spoofing Detected! The packet claims to be from a different source."

# ---------------- STREAMLIT PAGE ---------------- #

def app():
    add_dark_bg()

    st.markdown(
        "<h1 style='text-align:center;'>IP Spoofing Detector</h1>",
        unsafe_allow_html=True
    )

    st.subheader("Analyze incoming packets for IP source validation")

    st.write(
        """
        This tool simulates network packet inspection to detect if the source IP 
        address in the packet header has been tampered with.
        """
    )

    col1, col2 = st.columns(2)
    
    with col1:
        packet_ip = st.text_input("Declared Source IP (from Packet Header)", placeholder="e.g. 192.168.1.50")
    
    with col2:
        real_ip = st.text_input("Actual Source IP (System/Connection Level)", placeholder="e.g. 192.168.1.100")

    if st.button("Inspect Packet"):
        if not packet_ip or not real_ip:
            st.warning("⚠️ Please provide both IP addresses.")
        else:
            status, message = detect_spoofing(packet_ip, real_ip)
            
            if status == "Legitimate":
                st.success(message)
            else:
                st.error(message)
                st.info(f"Report: Packet claims to be {packet_ip} but is actually from {real_ip}")

            # ✅ Save to database
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ip_spoofing_logs (packet_source, real_source, status)
                VALUES (?, ?, ?)
            """, (packet_ip, real_ip, status))
            conn.commit()
            conn.close()

    st.markdown("---")
    st.markdown("### 🛠️ Common Spoofing Scenarios")
    st.write("- **Intranet Access:** Attacker uses an internal IP to bypass firewalls.")
    st.write("- **DoS Attack:** Forging source IPs to overwhelm a target and hide the attacker.")
    st.write("- **Man-in-the-Middle:** Spoofing IPs to redirect traffic through an attacker's machine.")
