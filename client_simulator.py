import requests
import random
import time
from datetime import datetime

# Server URL (Jahan logs bhejane hain)
SERVER_URL = "http://127.0.0.1:8000/api/v1/ingest"

# 1,000 simulated agents / endpoints ke names generate karna
agents = [f"server-node-{i}" for i in range(1, 1001)]
trusted_ips = ["192.168.1.10", "192.168.1.15", "10.0.0.5"]
suspicious_ips = ["45.33.32.156", "185.220.101.5", "103.25.14.88"]
usernames = ["admin", "root", "palak", "developer", "guest"]

def simulate_single_log():
    agent = random.choice(agents)
    # 80% chances normal IP ke honge, 20% suspicious attack IP ke
    ip = random.choice(trusted_ips * 4 + suspicious_ips)
    user = random.choice(usernames)
    
    if ip in suspicious_ips:
        action = random.choice(["FAILED_LOGIN", "UNAUTHORIZED_DB_ACCESS", "PRIVILEGE_ESCALATION"])
    else:
        action = random.choice(["SUCCESSFUL_LOGIN", "FILE_DOWNLOAD", "LOGOUT"])

    payload = {
        "agent_id": agent,
        "ip_address": ip,
        "username": user,
        "action": action,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        response = requests.post(SERVER_URL, json=payload)
        print(f"[{agent}] Sent log -> Status: {response.status_code}")
    except Exception as e:
        print(f"Connection error with server: {e}")

if __name__ == "__main__":
    print("Starting Client Simulator for 1,000 Endpoints...")
    print("Press Ctrl+C to stop.\n")
    
    # Continuously simulate logs coming from different endpoints
    while True:
        simulate_single_log()
        time.sleep(0.5) # Har 0.5 second mein logs bhejega