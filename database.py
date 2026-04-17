"""
Smart Planner — SQLite Database Layer
"""
import sqlite3
import uuid
import os
import sys
from datetime import datetime, timedelta


def get_db_path():
    """Возвращает путь к БД. В режиме .exe — рядом с .exe, иначе со скриптом."""
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "smart_planner.db")


DB_PATH = get_db_path()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            protected INTEGER DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS priorities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            sort_order INTEGER DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            category TEXT,
            priority TEXT NOT NULL,
            start_date TEXT,
            deadline TEXT,
            progress INTEGER DEFAULT 0,
            notes TEXT DEFAULT '',
            time_start TEXT DEFAULT '',
            time_end TEXT DEFAULT '',
            completed_at TEXT,
            type TEXT DEFAULT 'task',
            meeting_result TEXT DEFAULT '',
            recurring_id TEXT,
            notified_start INTEGER DEFAULT 0,
            notified_overdue INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS recurring (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            kind TEXT NOT NULL,
            description TEXT DEFAULT '',
            category TEXT,
            priority TEXT NOT NULL,
            time_start TEXT DEFAULT '',
            time_end TEXT DEFAULT '',
            deadline_days INTEGER DEFAULT 0,
            weekdays TEXT DEFAULT '',
            start_date TEXT,
            end_date TEXT,
            active INTEGER DEFAULT 1,
            last_generated TEXT,
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # Migrations for older DBs
    cols = [r["name"] for r in c.execute("PRAGMA table_info(tasks)").fetchall()]
    migrations = [
        ("type", "ALTER TABLE tasks ADD COLUMN type TEXT DEFAULT 'task'"),
        ("meeting_result", "ALTER TABLE tasks ADD COLUMN meeting_result TEXT DEFAULT ''"),
        ("recurring_id", "ALTER TABLE tasks ADD COLUMN recurring_id TEXT"),
        ("notified_start", "ALTER TABLE tasks ADD COLUMN notified_start INTEGER DEFAULT 0"),
        ("notified_overdue", "ALTER TABLE tasks ADD COLUMN notified_overdue INTEGER DEFAULT 0"),
    ]
    for col, sql in migrations:
        if col not in cols:
            try:
                c.execute(sql)
            except sqlite3.OperationalError:
                pass

    # Fix old schema: mark old-style 'Совещание' rows as meetings
    c.execute("UPDATE tasks SET type='meeting' WHERE category='Совещание' AND (type IS NULL OR type='task')")

    first_cat = c.execute("SELECT name FROM categories WHERE name!='Совещание' ORDER BY id LIMIT 1").fetchone()
    if first_cat:
        c.execute("UPDATE tasks SET category=? WHERE type='meeting' AND category='Совещание'", (first_cat["name"],))
    legacy = c.execute("SELECT COUNT(*) FROM tasks WHERE category='Совещание' AND type='task'").fetchone()[0]
    if legacy == 0:
        c.execute("DELETE FROM categories WHERE name='Совещание'")

    if c.execute("SELECT COUNT(*) FROM categories").fetchone()[0] == 0:
        for name in ["Рабочая", "Проект", "Обучение", "Личная", "Рутина"]:
            c.execute("INSERT INTO categories (name, protected) VALUES (?, 0)", (name,))

    if c.execute("SELECT COUNT(*) FROM priorities").fetchone()[0] == 0:
        for i, p in enumerate(["Высокий", "Средний", "Низкий"]):
            c.execute("INSERT INTO priorities (name, sort_order) VALUES (?, ?)", (p, i))

    if c.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0:
        today = datetime.now().strftime("%Y-%m-%d")
        seed = [
            (uid(), "Подготовить отчёт Q1", "Рабочая", "Высокий",
             "Сводный отчёт за квартал с графиками", today, off(3), 35,
             "Нужны данные от финансов", "", "", None, "task", "", None),
            (uid(), "Совещание по проекту Alpha", "Рабочая", "Средний",
             "Еженедельный статус-митинг", today, today, 0,
             "Презентация на 5 слайдов", "10:00", "11:30", None, "meeting", "", None),
            (uid(), "Обновить тарифы на сайте", "Проект", "Высокий",
             "Актуализация цен", off(-5), off(-1), 45,
             "Согласовать с маркетингом", "", "", None, "task", "", None),
            (uid(), "Планёрка отдела логистики", "Рабочая", "Высокий",
             "Обсуждение KPI", off(1), off(1), 0, "", "09:00", "09:45", None, "meeting", "", None),
        ]
        c.executemany("""
            INSERT INTO tasks (id, name, category, priority, description,
                start_date, deadline, progress, notes, time_start, time_end, completed_at, type, meeting_result, recurring_id)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, seed)

    conn.commit()
    conn.close()


def uid():
    return uuid.uuid4().hex[:12]


def off(n):
    return (datetime.now() + timedelta(days=n)).strftime("%Y-%m-%d")


# ─── TASKS & MEETINGS ───────────────────────────────────────────

def get_all_data():
    conn = get_conn()
    cats = [r["name"] for r in conn.execute("SELECT name FROM categories ORDER BY id").fetchall()]
    pris = [r["name"] for r in conn.execute("SELECT name FROM priorities ORDER BY sort_order").fetchall()]
    tasks_raw = conn.execute("SELECT * FROM tasks ORDER BY created_at").fetchall()
    tasks = []
    for t in tasks_raw:
        keys = t.keys()
        tasks.append({
            "id": t["id"],
            "name": t["name"],
            "desc": t["description"] or "",
            "cat": t["category"] or "",
            "pri": t["priority"],
            "start": t["start_date"],
            "deadline": t["deadline"],
            "progress": t["progress"] or 0,
            "notes": t["notes"] or "",
            "timeStart": t["time_start"] or "",
            "timeEnd": t["time_end"] or "",
            "completedAt": t["completed_at"],
            "createdAt": t["created_at"],
            "type": (t["type"] if "type" in keys else "task") or "task",
            "meetingResult": (t["meeting_result"] if "meeting_result" in keys else "") or "",
            "recurringId": (t["recurring_id"] if "recurring_id" in keys else None),
        })
    rec_raw = conn.execute("SELECT * FROM recurring ORDER BY created_at DESC").fetchall()
    recurring = []
    for r in rec_raw:
        recurring.append({
            "id": r["id"],
            "name": r["name"],
            "kind": r["kind"],
            "desc": r["description"] or "",
            "cat": r["category"] or "",
            "pri": r["priority"],
            "timeStart": r["time_start"] or "",
            "timeEnd": r["time_end"] or "",
            "deadlineDays": r["deadline_days"] or 0,
            "weekdays": r["weekdays"] or "",
            "startDate": r["start_date"],
            "endDate": r["end_date"],
            "active": bool(r["active"]),
            "lastGenerated": r["last_generated"],
            "notes": r["notes"] or "",
            "createdAt": r["created_at"],
        })
    conn.close()
    return {"categories": cats, "priorities": pris, "tasks": tasks, "recurring": recurring}


def add_task(data):
    conn = get_conn()
    tid = data.get("id") or uid()
    conn.execute("""
        INSERT OR REPLACE INTO tasks (id, name, description, category, priority,
            start_date, deadline, progress, notes, time_start, time_end, completed_at,
            type, meeting_result, recurring_id)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        tid, data["name"], data.get("desc", ""), data.get("cat", ""), data["pri"],
        data.get("start", ""), data.get("deadline", ""),
        int(data.get("progress", 0)), data.get("notes", ""),
        data.get("timeStart", ""), data.get("timeEnd", ""),
        data.get("completedAt"),
        data.get("type", "task"),
        data.get("meetingResult", ""),
        data.get("recurringId"),
    ))
    conn.commit()
    conn.close()
    return tid


def update_task(task_id, data):
    conn = get_conn()
    mapping = {
        "name": "name", "desc": "description", "cat": "category",
        "pri": "priority", "start": "start_date", "deadline": "deadline",
        "progress": "progress", "notes": "notes",
        "timeStart": "time_start", "timeEnd": "time_end",
        "completedAt": "completed_at", "type": "type",
        "meetingResult": "meeting_result",
        "notifiedStart": "notified_start",
        "notifiedOverdue": "notified_overdue",
    }
    fields, values = [], []
    for k, col in mapping.items():
        if k in data:
            fields.append(f"{col}=?")
            values.append(data[k])
    if fields:
        values.append(task_id)
        conn.execute(f"UPDATE tasks SET {','.join(fields)} WHERE id=?", values)
        conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_conn()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


# ─── RECURRING RULES ────────────────────────────────────────────

def add_recurring(data):
    conn = get_conn()
    rid = uid()
    conn.execute("""
        INSERT INTO recurring (id, name, kind, description, category, priority,
            time_start, time_end, deadline_days, weekdays, start_date, end_date, active, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        rid, data["name"], data["kind"], data.get("desc", ""),
        data.get("cat", ""), data["pri"],
        data.get("timeStart", ""), data.get("timeEnd", ""),
        int(data.get("deadlineDays", 0)),
        data.get("weekdays", ""),
        data.get("startDate"), data.get("endDate"),
        1 if data.get("active", True) else 0,
        data.get("notes", ""),
    ))
    conn.commit()
    conn.close()
    return rid


def update_recurring(rec_id, data):
    conn = get_conn()
    mapping = {
        "name": "name", "kind": "kind", "desc": "description",
        "cat": "category", "pri": "priority",
        "timeStart": "time_start", "timeEnd": "time_end",
        "deadlineDays": "deadline_days", "weekdays": "weekdays",
        "startDate": "start_date", "endDate": "end_date",
        "active": "active", "notes": "notes",
    }
    fields, values = [], []
    for k, col in mapping.items():
        if k in data:
            fields.append(f"{col}=?")
            val = 1 if (k == "active" and data[k]) else (0 if k == "active" else data[k])
            values.append(val)
    if fields:
        values.append(rec_id)
        conn.execute(f"UPDATE recurring SET {','.join(fields)} WHERE id=?", values)
        conn.commit()
    conn.close()


def delete_recurring(rec_id, remove_future=False):
    conn = get_conn()
    if remove_future:
        today = datetime.now().strftime("%Y-%m-%d")
        conn.execute(
            "DELETE FROM tasks WHERE recurring_id=? AND (start_date IS NULL OR start_date >= ?) AND (progress IS NULL OR progress < 100)",
            (rec_id, today),
        )
    conn.execute("DELETE FROM recurring WHERE id=?", (rec_id,))
    conn.commit()
    conn.close()


def propagate_recurring_edit(rec_id, patch):
    """Apply changes to all future (and today) not-completed generated tasks."""
    conn = get_conn()
    today = datetime.now().strftime("%Y-%m-%d")
    sync_map = {
        "name": "name", "desc": "description", "cat": "category",
        "pri": "priority", "timeStart": "time_start", "timeEnd": "time_end",
    }
    fields, values = [], []
    for k, col in sync_map.items():
        if k in patch:
            fields.append(f"{col}=?")
            values.append(patch[k])
    if fields:
        values.extend([rec_id, today])
        sql = (f"UPDATE tasks SET {','.join(fields)} "
               f"WHERE recurring_id=? AND (start_date IS NULL OR start_date >= ?) "
               f"AND (progress IS NULL OR progress < 100)")
        conn.execute(sql, values)

    if "deadlineDays" in patch:
        dd = int(patch["deadlineDays"] or 0)
        futures = conn.execute(
            "SELECT id, start_date FROM tasks WHERE recurring_id=? AND (start_date IS NULL OR start_date >= ?) AND (progress IS NULL OR progress < 100)",
            (rec_id, today),
        ).fetchall()
        for t in futures:
            if t["start_date"]:
                new_dl = (datetime.strptime(t["start_date"], "%Y-%m-%d") + timedelta(days=dd)).strftime("%Y-%m-%d")
                conn.execute("UPDATE tasks SET deadline=? WHERE id=?", (new_dl, t["id"]))
    conn.commit()
    conn.close()


def generate_recurring_tasks():
    """Generate instances for active recurring rules.
    - Meetings: created up to today+30 days (so they appear in the calendar ahead of time)
    - Tasks: created only for today (appear on the day they are due)
    """
    conn = get_conn()
    today = datetime.now().date()
    meeting_horizon = today + timedelta(days=30)
    rules = conn.execute("SELECT * FROM recurring WHERE active=1").fetchall()
    created = []

    for rule in rules:
        weekdays_str = rule["weekdays"] or ""
        wdays = set()
        for x in weekdays_str.split(","):
            x = x.strip()
            if x.isdigit():
                wdays.add(int(x))
        if not wdays:
            continue

        try:
            rule_start = datetime.strptime(rule["start_date"], "%Y-%m-%d").date() if rule["start_date"] else today
        except Exception:
            rule_start = today
        try:
            rule_end_raw = datetime.strptime(rule["end_date"], "%Y-%m-%d").date() if rule["end_date"] else None
        except Exception:
            rule_end_raw = None

        is_meeting = (rule["kind"] == "meeting")

        if is_meeting:
            # Meetings: generate up to 30 days ahead so they show in the weekly calendar
            horizon = meeting_horizon
            last_day = min(horizon, rule_end_raw) if rule_end_raw else horizon
        else:
            # Tasks: only generate for today
            horizon = today
            last_day = min(today, rule_end_raw) if rule_end_raw else today

        day = max(rule_start, today)
        dd = rule["deadline_days"] or 0

        while day <= last_day:
            if day.weekday() in wdays:
                day_iso = day.strftime("%Y-%m-%d")
                exists = conn.execute(
                    "SELECT 1 FROM tasks WHERE recurring_id=? AND start_date=?",
                    (rule["id"], day_iso),
                ).fetchone()
                if not exists:
                    tid = uid()
                    deadline = (day + timedelta(days=dd)).strftime("%Y-%m-%d") if dd else day_iso
                    conn.execute("""
                        INSERT INTO tasks (id, name, description, category, priority,
                            start_date, deadline, progress, notes, time_start, time_end,
                            completed_at, type, meeting_result, recurring_id)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (
                        tid, rule["name"], rule["description"] or "", rule["category"] or "",
                        rule["priority"], day_iso, deadline, 0, rule["notes"] or "",
                        rule["time_start"] or "", rule["time_end"] or "",
                        None, rule["kind"], "", rule["id"],
                    ))
                    created.append(tid)
            day += timedelta(days=1)

        conn.execute("UPDATE recurring SET last_generated=? WHERE id=?",
                     (last_day.strftime("%Y-%m-%d"), rule["id"]))

    conn.commit()
    conn.close()
    return created


# ─── NOTIFICATIONS ──────────────────────────────────────────────

def get_pending_notifications():
    """Returns list of new notifications to show and marks them as notified."""
    conn = get_conn()
    now = datetime.now()
    today_iso = now.strftime("%Y-%m-%d")
    notifications = []

    # Meetings starting within 5 minutes
    meetings = conn.execute("""
        SELECT * FROM tasks
        WHERE type='meeting' AND notified_start=0 AND (progress IS NULL OR progress < 100)
          AND start_date=? AND time_start != '' AND time_start IS NOT NULL
    """, (today_iso,)).fetchall()
    for m in meetings:
        try:
            sh, sm = map(int, m["time_start"].split(":"))
            start_dt = now.replace(hour=sh, minute=sm, second=0, microsecond=0)
            delta = (start_dt - now).total_seconds()
            if -60 <= delta <= 300:
                notifications.append({
                    "type": "meeting_start",
                    "id": m["id"],
                    "name": m["name"],
                    "time": m["time_start"],
                    "timeEnd": m["time_end"] or "",
                    "desc": m["description"] or "",
                })
                conn.execute("UPDATE tasks SET notified_start=1 WHERE id=?", (m["id"],))
        except (ValueError, AttributeError):
            pass

    # Tasks: just became overdue
    overdue = conn.execute("""
        SELECT * FROM tasks
        WHERE type='task' AND notified_overdue=0 AND (progress IS NULL OR progress < 100)
          AND deadline IS NOT NULL AND deadline != '' AND deadline < ?
    """, (today_iso,)).fetchall()
    for t in overdue:
        notifications.append({
            "type": "overdue",
            "id": t["id"],
            "name": t["name"],
            "deadline": t["deadline"],
        })
        conn.execute("UPDATE tasks SET notified_overdue=1 WHERE id=?", (t["id"],))

    conn.commit()
    conn.close()
    return notifications


# ─── CATEGORIES & PRIORITIES ────────────────────────────────────

def add_category(name):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO categories (name, protected) VALUES (?, 0)", (name,))
        conn.commit()
        ok = True
    except sqlite3.IntegrityError:
        ok = False
    conn.close()
    return ok


def delete_category(name):
    conn = get_conn()
    conn.execute("DELETE FROM categories WHERE name=?", (name,))
    conn.commit()
    conn.close()
    return True


def add_priority(name):
    conn = get_conn()
    mx = conn.execute("SELECT COALESCE(MAX(sort_order),0)+1 FROM priorities").fetchone()[0]
    try:
        conn.execute("INSERT INTO priorities (name, sort_order) VALUES (?,?)", (name, mx))
        conn.commit()
        ok = True
    except sqlite3.IntegrityError:
        ok = False
    conn.close()
    return ok


def delete_priority(name):
    conn = get_conn()
    conn.execute("DELETE FROM priorities WHERE name=?", (name,))
    conn.commit()
    conn.close()
    return True
