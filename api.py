"""
Smart Planner — Python↔JS API Bridge for pywebview
"""
import json
import os
import tempfile
import webbrowser
from datetime import datetime

import database as db


class Api:
    """Exposed to JavaScript via pywebview.api"""

    def get_data(self):
        """Load all data from SQLite."""
        return json.dumps(db.get_all_data(), ensure_ascii=False)

    def add_task(self, data_json):
        """Add a new task. Returns new task id."""
        data = json.loads(data_json)
        tid = db.add_task(data)
        return tid

    def update_task(self, task_id, data_json):
        """Update existing task fields."""
        data = json.loads(data_json)
        db.update_task(task_id, data)
        return "ok"

    def delete_task(self, task_id):
        """Delete a task by id."""
        db.delete_task(task_id)
        return "ok"

    def add_category(self, name):
        ok = db.add_category(name)
        return "ok" if ok else "exists"

    def delete_category(self, name):
        if db.is_category_protected(name):
            return "protected"
        ok = db.delete_category(name)
        return "ok" if ok else "protected"

    def is_category_protected(self, name):
        return db.is_category_protected(name)

    def add_priority(self, name):
        ok = db.add_priority(name)
        return "ok" if ok else "exists"

    def delete_priority(self, name):
        ok = db.delete_priority(name)
        return "ok" if ok else "error"

    def get_current_time(self):
        """Return current date and time for notification checks."""
        now = datetime.now()
        return json.dumps({
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "datetime": now.isoformat()
        })

    def export_json(self):
        """Return JSON string for backup."""
        return db.export_data()

    def import_json(self, json_str):
        """Import from JSON backup."""
        try:
            db.import_data(json_str)
            return "ok"
        except Exception as e:
            return f"error: {e}"

    def save_pdf_report(self, html_content):
        """Save HTML report to temp file and open in browser for printing to PDF."""
        tmp = os.path.join(tempfile.gettempdir(), f"smart_planner_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(html_content)
        webbrowser.open(f"file:///{tmp}")
        return tmp
