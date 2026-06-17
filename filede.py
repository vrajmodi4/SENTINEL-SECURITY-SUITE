import streamlit as st
from cryptography.fernet import Fernet, InvalidToken
import base64
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

        /* -------- TEXT COLOR -------- */
        h1, h2, h3, p, label {
            color: white !important;
            font-family: 'Inter', sans-serif;
        }

        /* -------- FILE UPLOADER STYLE -------- */
        [data-testid="stFileUploader"] {
            background-color: rgba(255, 255, 255, 0.05);
            border: 2px dashed #1f6feb;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #4da3ff;
            background-color: rgba(255, 255, 255, 0.08);
        }

        /* -------- BUTTON STYLE -------- */
        div.stButton > button {
            background: linear-gradient(135deg, #1f6feb, #1158c7) !important;
            color: white !important;
            border-radius: 10px;
            border: none;
            padding: 0.5rem 2rem !important; /* Smaller padding */
            font-size: 15px !important;
            font-weight: 600;
            width: auto !important; /* Ensure it's not too big */
            box-shadow: 0 4px 15px rgba(31, 111, 235, 0.3);
            transition: all 0.3s ease;
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(31, 111, 235, 0.4);
            background: linear-gradient(135deg, #4da3ff, #1f6feb) !important;
        }

        div.stButton > button:active {
            transform: translateY(0);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------------- STREAMLIT PAGE ---------------- #

def app():
    add_dark_bg()

    st.markdown(
        "<h1 style='text-align:center;'> File Decryption Tool</h1>",
        unsafe_allow_html=True
    )

    st.subheader("Decrypt encrypted files (Documents, Audio, Video) using your Secret Key.")

    encrypted_file = st.file_uploader(
        "Upload encrypted file (.enc)",
        type=["enc"]
    )

    secret_key = st.text_input(
        "Enter Secret Key (paste exactly as generated)",
        type="password"
    )

    if st.button("Decrypt File"):

        if encrypted_file is None or secret_key.strip() == "":
            st.warning("⚠️ Please upload a file and enter the secret key")
            return

        # ✅ CLEAN & VALIDATE KEY
        clean_key = secret_key.strip()

        try:
            # Validate base64 format
            base64.urlsafe_b64decode(clean_key)

            cipher = Fernet(clean_key.encode())
            decrypted_data = cipher.decrypt(encrypted_file.read())

            original_filename = encrypted_file.name.replace(".enc", "")

            st.success("✅ File decrypted successfully!")

            st.download_button(
                label="Download Decrypted File",
                data=decrypted_data,
                file_name=original_filename,
                mime="application/octet-stream"
            )

            # ✅ Save to database (Success)
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO decryption_logs (file_name, status)
                VALUES (?, ?)
            """, (original_filename, "Success"))
            conn.commit()
            conn.close()

        except (InvalidToken, ValueError):
            st.error(
                "❌ Decryption failed. Invalid key or corrupted encrypted file."
            )
            # ✅ Save to database (Failure)
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO decryption_logs (file_name, status)
                VALUES (?, ?)
            """, (encrypted_file.name, "Failed"))
            conn.commit()
            conn.close()

    st.caption(
        "⚠️ The secret key must be exactly the same key generated during encryption."
    )
