from datetime import datetime

def log_info(msg: str):
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    message = f"[INFO - {now}] {msg}"
    print(message)

def log_error(msg: str):
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    message = f"[ERROR - {now}] {msg}"
    print(message)
    