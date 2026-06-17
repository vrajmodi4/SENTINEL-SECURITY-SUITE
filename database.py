import pymongo
from datetime import datetime

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "sentinel_security_suite"

def get_db():
    client = pymongo.MongoClient(MONGO_URI)
    return client[DB_NAME]

def create_tables():
    """ In MongoDB, collections are created automatically. 
    We just ensure we can connect. """
    try:
        db = get_db()
        # Optionally create indexes
        db.phishing_logs.create_index("timestamp")
        db.malware_logs.create_index("timestamp")
        db.login_attempts.create_index("attempt_time")
        db.encryption_logs.create_index("timestamp")
        db.decryption_logs.create_index("timestamp")
        db.ip_spoofing_logs.create_index("timestamp")
        print("Connected to MongoDB successfully.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

def insert_log(collection_name, data):
    """ Generic function to insert a log into a specific collection """
    try:
        db = get_db()
        if "timestamp" not in data and "attempt_time" not in data:
            data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db[collection_name].insert_one(data)
    except Exception as e:
        print(f"Error inserting into {collection_name}: {e}")

def get_logs(collection_name, limit=None, sort_desc=True):
    """ Generic function to retrieve logs from a specific collection """
    try:
        db = get_db()
        cursor = db[collection_name].find()
        
        # Determine sort key
        sort_key = "timestamp" if "timestamp" in (db[collection_name].find_one() or {}) else "id"
        if collection_name == "login_attempts":
            sort_key = "attempt_time"

        if sort_desc:
            cursor = cursor.sort(sort_key, pymongo.DESCENDING)
        
        if limit:
            cursor = cursor.limit(limit)
            
        logs = list(cursor)
        # Convert ObjectId to string for JSON compatibility
        for log in logs:
            log["_id"] = str(log["_id"])
            # Ensure 'id' exists for backward compatibility if code expects it
            if "id" not in log:
                log["id"] = log["_id"]
        return logs
    except Exception as e:
        print(f"Error retrieving from {collection_name}: {e}")
        return []

def count_logs(collection_name, query=None):
    """ Generic function to count documents in a collection """
    try:
        db = get_db()
        return db[collection_name].count_documents(query or {})
    except Exception as e:
        print(f"Error counting in {collection_name}: {e}")
        return 0


def clear_logs():
    """ Function to clear all logs from all collections """
    try:
        db = get_db()
        collections = [
            "phishing_logs", 
            "malware_logs", 
            "login_attempts", 
            "encryption_logs",
            "decryption_logs", 
            "ip_spoofing_logs"
        ]
        for collection in collections:
            db[collection].delete_many({})
        print("All logs cleared successfully.")
        return True
    except Exception as e:
        print(f"Error clearing logs: {e}")
        return False

def connect_db():
    """ Legacy support for connect_db - returns None as MongoDB doesn't use the same connection pattern as SQLite """
    return None

