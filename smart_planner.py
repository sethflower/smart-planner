"""
Smart Planner Pro — Windows Desktop Application
Requires: pip install pywebview
"""
import os
import sys
import time
import threading
import json as _json
import webview
import database as db
from api import Api


def _resource_path(rel):
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, rel)


def _load_html():
    path = _resource_path("app.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def background_worker(window_ref):
    last_gen_date = None
    while True:
        try:
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            if last_gen_date != today:
                db.generate_recurring_tasks()
                last_gen_date = today
                w = window_ref[0]
                if w is not None:
                    try:
                        w.evaluate_js("window.__onDataChanged && window.__onDataChanged()")
                    except Exception:
                        pass
            notifications = db.get_pending_notifications()
            if notifications:
                w = window_ref[0]
                if w is not None:
                    try:
                        w.evaluate_js(
                            f"window.__onNotifications && window.__onNotifications({_json.dumps(notifications, ensure_ascii=False)})"
                        )
                    except Exception:
                        pass
        except Exception:
            pass
        time.sleep(30)


def main():
    db.init_db()
    db.generate_recurring_tasks()
    api = Api()
    window_ref = [None]
    html = _load_html()
    window = webview.create_window(
        title="Smart Planner Pro",
        html=html,
        js_api=api,
        width=1400,
        height=900,
        min_size=(900, 600),
        text_select=True,
    )
    window_ref[0] = window
    t = threading.Thread(target=background_worker, args=(window_ref,), daemon=True)
    t.start()
    webview.start(debug=False)


if __name__ == "__main__":
    main()
