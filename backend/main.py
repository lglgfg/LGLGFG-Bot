from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3, pyautogui

app = FastAPI()

def init_db():
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, data TEXT)")
    conn.commit()
    conn.close()

def save_memory(text: str):
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("INSERT INTO memory (data) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def get_memory():
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("SELECT data FROM memory ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

class Task(BaseModel):
    command: str
    context: str = ""

@app.post("/task")
def handle_task(task: Task):
    save_memory(task.context)
    if "autofill" in task.command.lower():
        pyautogui.typewrite(task.context)
        return {"status": "Autofilled form with data"}
    elif "marketing" in task.command.lower():
        idea = f"Marketing idea for LGLGFG: TikTok fashion trend + Instagram collab."
        save_memory(idea)
        return {"status": "Marketing idea", "plan": idea}
    elif "code" in task.command.lower():
        code = "def hello():\n    print('Hello from LGLGFG Bot!')"
        save_memory(code)
        return {"status": "Code generated", "code": code}
    return {"status": "Unknown", "memory": get_memory()}

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
