import streamlit as st
import re
import database   # ✅ import at top

# ---------------- BACKGROUND ---------------- #

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

# ---------------- UTILITY FUNCTIONS ---------------- #

def is_ip_address(url):
    ip_pattern = r"(http[s]?://)?(\d{1,3}\.){3}\d{1,3}"
    return re.search(ip_pattern, url)

def phishing_url_detector(url):
    score = 0
    reasons = []

    if len(url) > 75:
        score += 1
        reasons.append("URL length is unusually long")

    if "@" in url:
        score += 1
        reasons.append("URL contains '@' symbol")

    if is_ip_address(url):
        score += 1
        reasons.append("URL uses IP address instead of domain name")

    suspicious_words = [
        "login", "verify", "update", "free",
        "click", "secure", "account", "bank", "confirm"
    ]

    for word in suspicious_words:
        if word in url.lower():
            score += 1
            reasons.append(f"Suspicious word detected: '{word}'")
            break

    if url.count('.') > 4:
        score += 1
        reasons.append("URL contains too many dots")

    if "-" in url:
        score += 1
        reasons.append("URL contains hyphen (-)")

    return score, reasons

# ---------------- STREAMLIT PAGE ---------------- #

def app():

    add_dark_bg()

    st.markdown(
        "<h1 style='text-align:center;'>Phishing URL Detector</h1>",
        unsafe_allow_html=True
    )

    st.subheader("Detect potentially harmful URLs using heuristic analysis")

    url = st.text_input(
        "Enter URL",
        placeholder="https://example.com"
    )

    if st.button("Check URL"):

        if url.strip() == "":
            st.warning("⚠️ Please enter a URL")

        else:
            score, reasons = phishing_url_detector(url)

            # ✅ Save to database (properly inside block)
            conn = database.connect_db()
            cursor = conn.cursor()

            result = "Phishing" if score >= 3 else "Legitimate"

            cursor.execute("""
                INSERT INTO phishing_logs (url, risk_score, result)
                VALUES (?, ?, ?)
            """, (url, score, result))

            conn.commit()
            conn.close()

            # ✅ Show result
            st.markdown("### 🔍 Analysis Result")

            if score >= 3:
                st.error("⚠️ Phishing URL Detected")
            else:
                st.success("✅ Legitimate URL")

            st.write(f"**Risk Score:** {score}")

            if reasons:
                st.markdown("### 🚩 Reasons")
                for r in reasons:
                    st.write(f"- {r}")

            st.markdown("---")
