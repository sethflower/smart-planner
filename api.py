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
        return json.dumps(db.get_all_data(), ensure_ascii=False)

    def add_task(self, data_json):
        data = json.loads(data_json)
        return db.add_task(data)

    def update_task(self, task_id, data_json):
        data = json.loads(data_json)
        db.update_task(task_id, data)
        return "ok"

    def delete_task(self, task_id):
        db.delete_task(task_id)
        return "ok"

    def add_category(self, name):
        return "ok" if db.add_category(name) else "exists"

    def delete_category(self, name):
        db.delete_category(name)
        return "ok"

    def add_priority(self, name):
        return "ok" if db.add_priority(name) else "exists"

    def delete_priority(self, name):
        db.delete_priority(name)
        return "ok"

    # ─── Recurring ────────────────────────────
    def add_recurring(self, data_json):
        data = json.loads(data_json)
        rid = db.add_recurring(data)
        db.generate_recurring_tasks()
        return rid

    def update_recurring(self, rec_id, data_json):
        data = json.loads(data_json)
        db.update_recurring(rec_id, data)
        db.propagate_recurring_edit(rec_id, data)
        db.generate_recurring_tasks()
        return "ok"

    def delete_recurring(self, rec_id, remove_future):
        rf = remove_future if isinstance(remove_future, bool) else str(remove_future).lower() == "true"
        db.delete_recurring(rec_id, rf)
        return "ok"

    def generate_recurring(self):
        """Trigger recurring task generation. Returns list of new ids."""
        return db.generate_recurring_tasks()

    # ─── Notifications ────────────────────────
    def get_notifications(self):
        """Returns pending notifications as JSON string."""
        return json.dumps(db.get_pending_notifications(), ensure_ascii=False)

    # ─── Report ───────────────────────────────
    def save_pdf_report(self, html_content):
        tmp = os.path.join(
            tempfile.gettempdir(),
            f"smart_planner_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
        )
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(html_content)
        webbrowser.open(f"file:///{tmp}")
        return tmp
