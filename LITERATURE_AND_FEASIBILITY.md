# Literature Review and Feasibility Study

## 1. Literature Review

### 1.1 Overview of Cybersecurity Education Tools
The increasing sophistication of cyber threats has created a significant demand for cybersecurity awareness. Traditional methods of learning often involve theoretical textbooks or complex command-line tools (like Kali Linux) which can intimidate beginners. Recent studies emphasize the effectiveness of **Interactive Visualization Tools** in cybersecurity education. Tools that allow users to simulate attacks and defenses in a controlled, safe environment (sandboxing) significantly improve learning outcomes compared to passive learning.

### 1.2 Phishing Detection Techniques
Phishing remains one of the most common attack vectors. Existing literature categorizes detection methods into:
1.  **List-Based Approaches**: Checking URLs against blacklists (e.g., Google Safe Browsing, PhishTank). While accurate, these fail to detect zero-day phishing sites.
2.  **Heuristic/Lexical Analysis**: Analyzing the URL string itself (length, suspicious characters, domain obfuscation).
3.  **Machine Learning**: Training models on dataset features.
**Relevance to Project**: The *Sentinel Security Suite* implements the **Heuristic Approach**. Research by *M. Khonji et al.* suggests that lexical analysis is computationally efficient for real-time detection on local machines, making it suitable for this lightweight application working without an external API dependency.

### 1.3 Malware Analysis and Hashing
Static malware analysis often relies on **Cryptographic Hashing**. The unique identification of files using algorithms like MD5, SHA-1, or SHA-256 is a foundational concept in digital forensics.
*   **Industry Standard**: Antivirus software maintains massive databases of known malicious hashes.
*   **Project Implementation**: This project uses **SHA-256**, which is currently the industry standard for integrity verification, surpassing MD5 which is robust to collision attacks. This provides students with a realistic view of how "File Signatures" work in enterprise AV solutions.

### 1.4 Brute Force Attack Simulation
Brute Force Attacks (BFA) exploit weak credentials. The **NIST Digital Identity Guidelines (SP 800-63B)** recommend "rate limiting" or "account lockout" after a specific number of failed attempts to mitigate BFA.
* **Project Implementation**: The simulation implements a "Lockout Policy" (5 failures = 30-second lockout). This directly mirrors recommended defense strategies, providing a practical demonstration of how throttle mechanisms prevent dictionary attacks.

### 1.5 Cryptography Standards (AES)
Symmetric encryption is the backbone of file security. **AES (Advanced Encryption Standard)** is the globally accepted standard approved by NIST.
* **Library Choice**: The project uses the `cryptography` Python library, specifically the **Fernet** module. Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key. This uses AES-128 in CBC mode with a SHA256 HMAC, ensuring both *confidentiality* and *integrity*, a concept often highlighted in academic cryptography courses.

---

## 2. Feasibility Study

### 2.1 Technical Feasibility
The project is technically feasible as it relies on stable, open-source technologies:
*   **Python 3.x**: A mature language with extensive security libraries (`hashlib`, `cryptography`).
*   **Streamlit**: A framework designed for data scripts, allowing rapid UI development without needing deep knowledge of HTML/CSS/JavaScript.
*   **SQLite**: A serverless, self-contained database engine. It requires no administration, making it perfect for a standalone educational tool.
*   **Hardware**: The application runs on standard consumer hardware (4GB RAM, generic CPU), requiring no specialized servers or GPUs.

### 2.2 Economic Feasibility
*   **Development Cost**: Zero ($0). All tools (VS Code, Python, Git) and libraries are open-source and free to use.
*   **Infrastructure Cost**: No cloud hosting is required as it runs on `localhost`.
*   **Maintenance**: Low. The codebase is modular, and Python code is easy to maintain.
*   **Conclusion**: The project is highly economically viable with a high educational Return on Investment (ROI).

### 2.3 Operational Feasibility
*   **Usability**: The Graphical User Interface (GUI) provided by Streamlit is intuitive (menu-driven). Students do not need to learn command-line arguments to use the tools.
*   **Deployment**: The "Installation" consists of a single `pip install` command, making it accessible to students with minimal technical setup.
*   **Legal/Ethical**: The tool is defensive and educational. It simulates attacks (BFA) internally and checks files passively, avoiding any legal issues associated with offensive security tools.

### 2.4 Time Schedule Feasibility
*   **Development Time**: The modular design allows for incremental development. Core features (Hashing, Phishing Logic) can be built in days.
*   **Testing**: Unit testing of individual functions (e.g., `calculate_hash`) is straightforward.
*   **Status**: The project has been successfully implemented within the allotted semester timeline, proving its schedule feasibility.
