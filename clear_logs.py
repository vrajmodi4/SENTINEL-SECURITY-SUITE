import database

if __name__ == "__main__":
    print("Clearing all logs from Sentinel Security Suite...")
    success = database.clear_logs()
    if success:
        print("Done!")
    else:
        print("Failed to clear logs. Make sure MongoDB is running.")
