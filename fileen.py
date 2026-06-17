import streamlit as st
from cryptography.fernet import Fernet
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
        "<h1 style='text-align:center;'>File Encryption Tool</h1>",
        unsafe_allow_html=True
    )

    st.subheader("Securely encrypt Documents, Images, Audio (MP3), and Video (MP4) using AES.")

    st.write(
        """
        Upload a file and generate a secret key to encrypt the file securely.
        The same key will be required later to decrypt the file.
        """
    )

    uploaded_file = st.file_uploader(
        "Upload file to encrypt",
        type=None
    )

    if uploaded_file is not None:

        # Generate encryption key
        key = Fernet.generate_key()
        cipher = Fernet(key)

        file_data = uploaded_file.read()
        encrypted_data = cipher.encrypt(file_data)

        st.markdown("### 🔐 Encryption Key")
        st.code(key.decode())
        st.warning("⚠️ Save this key securely. You will need it to decrypt the file.")

        st.markdown("### 📁 Encrypted File")

        st.download_button(
            label="Download Encrypted File",
            data=encrypted_data,
            file_name=uploaded_file.name + ".enc",
            mime="application/octet-stream"
        )

        st.success("✅ File encrypted successfully!")

        # ✅ Save to database
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO encryption_logs (file_name)
            VALUES (?)
        """, (uploaded_file.name,))
        conn.commit()
        conn.close()

    st.markdown("---")
    st.caption(
        "⚠️ This tool uses Fernet (AES) symmetric encryption for educational purposes."
    )
