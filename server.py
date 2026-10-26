from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from database import init_db, save_log_to_db, get_all_logs_from_db

app = FastAPI(title="Smart-SIEM Backend", version="1.0")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

class LogEntry(BaseModel):
    agent_id: str
    ip_address: str
    username: str
    action: str
    timestamp: str = None

@app.get("/")
def home():
    return {"message": "Smart-SIEM Ingestion Server is running successfully! 🛡️"}

# --- LOG INGESTION ENDPOINT ---
@app.post("/api/v1/ingest")
def ingest_log(log: LogEntry):
    if not log.timestamp:
        log.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    trusted_ips = ["192.168.1.10", "192.168.1.15", "10.0.0.5"]
    is_trusted = log.ip_address in trusted_ips

    # --- TRIAGE & NOISE REDUCTION LOGIC ---
    risk_score = 0
    is_noise = False
    reason = "Normal Activity"

    if log.action == "FAILED_LOGIN" and is_trusted:
        risk_score = 10
        is_noise = True
        reason = "Failed login from trusted network (Ignored as Noise)"
    elif log.action == "FAILED_LOGIN" and not is_trusted:
        risk_score = 75
        is_noise = False
        reason = "Failed login from external IP (Potential Brute Force)"
    elif log.action == "UNAUTHORIZED_DB_ACCESS":
        risk_score = 95
        is_noise = False
        reason = "Critical: Unauthorized Database Access Attempt!"
    elif log.action == "PRIVILEGE_ESCALATION":
        risk_score = 90
        is_noise = False
        reason = "High: Privilege Escalation Detected!"
    else:
        risk_score = 0
        is_noise = True
        reason = "Routine user action"

    processed_log = {
        "agent_id": log.agent_id,
        "ip_address": log.ip_address,
        "username": log.username,
        "action": log.action,
        "timestamp": log.timestamp,
        "risk_score": risk_score,
        "is_noise": is_noise,
        "reason": reason
    }

    # Save to SQLite Database
    save_log_to_db(processed_log)

    return {
        "status": "success",
        "message": "Log processed and saved to DB",
        "analysis": processed_log
    }

# --- GET ALL LOGS FOR DASHBOARD ---
@app.get("/api/v1/logs")
def get_logs():
    all_logs = get_all_logs_from_db()
    return {
        "total_logs_received": len(all_logs),
        "logs": all_logs
    }