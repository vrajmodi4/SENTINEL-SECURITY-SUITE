import database
database.create_tables()

import streamlit as st
from  streamlit_option_menu import option_menu
import Phishing,fileen,filede,malware,BFA,admin,logs_viewer,ip_spoofing

st.set_page_config(
    page_title = "Sentinel Security Suite",
)

class MultiApp:
    def __init__(self) :
        self.apps = []
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
    def run(self):

        with st.sidebar:
            app = option_menu(
                menu_title = "Sentinel Security Suite",
                options = ["Phishing Detection", "Malware Analysis", "Brute Force Attack", "File Encryption","File Decryption", "IP Spoofing Detection", "View Logs (History)", "Admin Dashboard"],
                icons = ["shield-lock","bug","key","file-earmark-lock2","file-earmark-lock2", "hdd-network", "clock-history", "speedometer"],
                menu_icon = 'chat-text-fill',
                default_index = 1,
                styles = {
                    "container": {"padding": "5!important", "background-color": "#000000"},
                    "icon":{"color":"white", "font-size":"23px"},
                    "nav-link": {"color":"white","font-size":"20px","text-align":"left","margin":"0px","--hover-color": "#000000"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        if app == "Phishing Detection":
                Phishing.app()
        if app == "Malware Analysis":
                malware.app()
        if app == "Brute Force Attack":
                BFA.app()
        if app == "File Encryption":
                fileen.app()
        if app == "File Decryption":
                filede.app()
        if app == "IP Spoofing Detection":
                ip_spoofing.app()
        if app == "View Logs (History)":
                logs_viewer.app()
        if app == "Admin Dashboard":
                admin.app()


if __name__ == "__main__":
    run = MultiApp()
    run.add_app("Phishing Detection", Phishing.app)
    run.add_app("Malware Analysis", malware.app)
    run.add_app("Brute Force Attack", BFA.app)
    run.add_app("File Encryption", fileen.app)
    run.add_app("File Decryption", filede.app)  
    run.add_app("IP Spoofing Detection", ip_spoofing.app)
    run.add_app("View Logs (History)", logs_viewer.app)
    run.add_app("Admin Dashboard", admin.app)
    run.run()

    