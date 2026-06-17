# System Diagrams (PlantUML Syntax)

You can render these diagrams using any PlantUML viewer (like the PlantUML extension for VS Code) or online at [planttext.com](https://www.planttext.com/).

## 1. Use Case Diagram

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "User" as u
actor "Admin" as a

package "Sentinel Security Suite" {
  usecase "Phishing Detection" as UC1
  usecase "Malware Analysis" as UC2
  usecase "Brute Force Simulation" as UC3
  usecase "File Encryption" as UC4
  usecase "File Decryption" as UC5
  usecase "View Logs" as UC6
  usecase "Admin Dashboard" as UC7
  usecase "Login" as UC8
}

u --> UC1
u --> UC2
u --> UC3
u --> UC4
u --> UC5

a --> UC8
UC8 ..> UC6 : <<include>>
UC8 ..> UC7 : <<include>>
@enduml
```

## 2. Class Diagram

```plantuml
@startuml
skinparam classAttributeIconSize 0

class MultiApp {
  +apps : list
  +add_app(title, function)
  +run()
}

class Database {
  +connect_db() : Connection
  +create_tables() : void
}

class Phishing {
  +phishing_url_detector(url) : tuple
  +is_ip_address(url) : bool
  +app() : void
}

class Malware {
  +calculate_hash(file) : string
  +is_suspicious_file(filename) : bool
  +app() : void
}

class BFA {
  +app() : void
  -validate_login(user, pass) : bool
}

class FileEncryption {
  +app() : void
  -encrypt_file(file) : bytes
}

class FileDecryption {
  +app() : void
  -decrypt_file(file, key) : bytes
}

class Admin {
  +check_password() : bool
  +app() : void
  +view_metrics() : void
}

MultiApp --> Phishing
MultiApp --> Malware
MultiApp --> BFA
MultiApp --> FileEncryption
MultiApp --> FileDecryption
MultiApp --> Admin

Phishing ..> Database
Malware ..> Database
BFA ..> Database
FileEncryption ..> Database
FileDecryption ..> Database
Admin ..> Database
@enduml
```

## 3. Sequence Diagram (Phishing Detection)

```plantuml
@startuml
actor User
participant "Streamlit UI" as UI
participant "Phishing Logic" as Logic
participant "Database" as DB

User -> UI: Input URL
User -> UI: Click "Check URL"
activate UI

UI -> Logic: phishing_url_detector(url)
activate Logic
Logic -> Logic: Check Length
Logic -> Logic: Check IP Pattern
Logic -> Logic: Check Suspicious Words
Logic -> Logic: Calculate Risk Score
Logic --> UI: Return (Score, Reasons)
deactivate Logic

UI -> DB: INSERT INTO phishing_logs
activate DB
DB --> UI: Success
deactivate DB

alt Score >= 3
    UI -> User: Show "Phishing Detected" (Error)
else Score < 3
    UI -> User: Show "Legitimate URL" (Success)
end

UI -> User: Display Analysis Details
deactivate UI
@enduml
```

## 4. Activity Diagram (Malware Analysis)

```plantuml
@startuml
start
:User Uploads File;

if (File Uploaded?) then (yes)
  :Calculate SHA-256 Hash;
  :Check File Extension;
  
  if (Is Suspicious Extension?) then (yes)
    :Result = Suspicious;
    :Log to Database (Mark Suspicious);
  else (no)
    :Result = Safe;
    :Log to Database (Mark Safe);
  endif
  
  :Display File Hash;
  :Display Analysis Result;
else (no)
  :Wait for Input;
endif

stop
@enduml
```

## 5. Entity-Relationship (E-R) Diagram

```plantuml
@startuml
entity "Phishing Logs" as phish {
  *id : INTEGER <<PK>>
  --
  url : TEXT
  risk_score : INTEGER
  result : TEXT
  timestamp : TIMESTAMP
}

entity "Malware Logs" as mal {
  *id : INTEGER <<PK>>
  --
  file_name : TEXT
  file_hash : TEXT
  result : TEXT
  timestamp : TIMESTAMP
}

entity "Login Attempts" as login {
  *id : INTEGER <<PK>>
  --
  username : TEXT
  status : TEXT
  attempt_time : TIMESTAMP
}

entity "Encryption Logs" as enc {
  *id : INTEGER <<PK>>
  --
  file_name : TEXT
  timestamp : TIMESTAMP
}

entity "Decryption Logs" as dec {
  *id : INTEGER <<PK>>
  --
  file_name : TEXT
  status : TEXT
  timestamp : TIMESTAMP
}

note bottom: Tables are independent logs\n(No Foreign Keys used)
@enduml
```

## 6. Data Flow Diagrams (DFD)

### Level 0: Context Diagram

```plantuml
@startuml
rectangle "User" as U
rectangle "Admin" as A
circle "Sentinel Security Suite" as Sys
database "Database" as DB

U --> Sys : Inputs (URL, Files)
Sys --> U : Results (Risk Score, Hash)

A --> Sys : Login Credentials
Sys --> A : Dashboard / Logs

Sys <--> DB : Read/Write Logs
@enduml
```

### Level 1: System Breakdown

```plantuml
@startuml
rectangle "User" as U
rectangle "Admin" as A

package "Sentinel Security Suite" {
    usecase "1.0 Phishing Detection" as P
    usecase "2.0 Malware Analysis" as M
    usecase "3.0 Brute Force Sim" as B
    usecase "4.0 Crypto Operations" as C
    usecase "5.0 Admin Dashboard" as AD
}

database "Database" as DB

U --> P : URL
U --> M : File
U --> B : Credentials
U --> C : File & Key

P --> DB : Log Result
M --> DB : Log Result
B --> DB : Log Attempt
C --> DB : Log Operation

DB --> AD : Fetch Logs
A --> AD : View
@enduml
```

### Level 2: Phishing Module Detail

```plantuml
@startuml
rectangle "User" as U
database "Database" as DB

rectangle "1.0 Phishing Detection" {
    usecase "1.1 Receive Input" as P1
    usecase "1.2 Validate Format" as P2
    usecase "1.3 Heuristic Analysis" as P3
    usecase "1.4 Calculate Score" as P4
    usecase "1.5 Format Result" as P5
}

U --> P1 : Input URL
P1 --> P2
P2 --> P3 : Valid
P2 --> U : Error (Invalid)
P3 --> P4 : Extract Features
P4 --> P5 : Score & Details
P5 --> DB : Log Data
P5 --> U : Display Result
@enduml
```
