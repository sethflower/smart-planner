"""
Smart Planner — SQLite Database Layer
"""
import sqlite3
import json
import uuid
import os
from datetime import datetime, timedelta


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smart_planner.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
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
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            start_date TEXT,
            deadline TEXT,
            progress INTEGER DEFAULT 0,
            notes TEXT DEFAULT '',
            time_start TEXT DEFAULT '',
            time_end TEXT DEFAULT '',
            completed_at TEXT,
            type TEXT DEFAULT 'task',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (category) REFERENCES categories(name),
            FOREIGN KEY (priority) REFERENCES priorities(name)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS recurrence_rules (
            id TEXT PRIMARY KEY,
            item_type TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            category TEXT,
            priority TEXT NOT NULL,
            notes TEXT DEFAULT '',
            time_start TEXT DEFAULT '',
            time_end TEXT DEFAULT '',
            start_date TEXT NOT NULL,
            end_date TEXT,
            weekdays TEXT DEFAULT '[]',
            every_day INTEGER DEFAULT 0,
            deadline_offset_days INTEGER DEFAULT 0,
            active INTEGER DEFAULT 1,
            last_generated_date TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # Migration: add `type` column to existing databases if missing
    cols = [r["name"] for r in c.execute("PRAGMA table_info(tasks)").fetchall()]
    if "type" not in cols:
        c.execute("ALTER TABLE tasks ADD COLUMN type TEXT DEFAULT 'task'")
        # Mark existing tasks in 'Совещание' category as meetings
        c.execute("UPDATE tasks SET type='meeting' WHERE category='Совещание'")
        conn.commit()
    if "result_text" not in cols:
        c.execute("ALTER TABLE tasks ADD COLUMN result_text TEXT DEFAULT ''")
        conn.commit()
    if "recurrence_rule_id" not in cols:
        c.execute("ALTER TABLE tasks ADD COLUMN recurrence_rule_id TEXT")
        conn.commit()
    if "reminder_sent" not in cols:
        c.execute("ALTER TABLE tasks ADD COLUMN reminder_sent INTEGER DEFAULT 0")
        conn.commit()
    if "overdue_notified" not in cols:
        c.execute("ALTER TABLE tasks ADD COLUMN overdue_notified INTEGER DEFAULT 0")
        conn.commit()
    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_tasks_rule_start ON tasks(recurrence_rule_id, start_date)")

    # Migration: meetings shouldn't belong to "Совещание" category anymore.
    # Reassign their category to first available category so they don't need that legacy category.
    meeting_count = c.execute("SELECT COUNT(*) FROM tasks WHERE type='meeting' AND category='Совещание'").fetchone()[0]
    if meeting_count > 0:
        first_cat_row = c.execute("SELECT name FROM categories WHERE name!='Совещание' ORDER BY id LIMIT 1").fetchone()
        if first_cat_row:
            c.execute("UPDATE tasks SET category=? WHERE type='meeting' AND category='Совещание'", (first_cat_row["name"],))
        conn.commit()

    # Now safe to remove legacy "Совещание" category if no regular tasks use it
    legacy_task_count = c.execute("SELECT COUNT(*) FROM tasks WHERE category='Совещание' AND type='task'").fetchone()[0]
    if legacy_task_count == 0:
        c.execute("DELETE FROM categories WHERE name='Совещание'")
        conn.commit()

    # Seed defaults if empty
    cats = c.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    if cats == 0:
        defaults = [
            ("Рабочая", 0), ("Проект", 0),
            ("Обучение", 0), ("Личная", 0), ("Рутина", 0),
        ]
        c.executemany("INSERT INTO categories (name, protected) VALUES (?, ?)", defaults)

    pris = c.execute("SELECT COUNT(*) FROM priorities").fetchone()[0]
    if pris == 0:
        for i, p in enumerate(["Высокий", "Средний", "Низкий"]):
            c.execute("INSERT INTO priorities (name, sort_order) VALUES (?, ?)", (p, i))

    tasks_count = c.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if tasks_count == 0:
        today = datetime.now().strftime("%Y-%m-%d")
        # (id, name, category, priority, description, start, deadline, progress, notes, time_start, time_end, completed_at, type)
        seed = [
            (uid(), "Подготовить отчёт Q1", "Рабочая", "Высокий",
             "Сводный отчёт за квартал с графиками", today, off(3), 35,
             "Нужны данные от финансов", "", "", None, "task"),
            (uid(), "Совещание по проекту Alpha", "Рабочая", "Средний",
             "Еженедельный статус-митинг", today, today, 0,
             "Презентация на 5 слайдов", "10:00", "11:30", None, "meeting"),
            (uid(), "Обновить тарифы на сайте", "Проект", "Высокий",
             "Актуализация цен", off(-5), off(-1), 45,
             "Согласовать с маркетингом", "", "", None, "task"),
            (uid(), "Курс по аналитике", "Обучение", "Низкий",
             "Модуль 3 из 8", off(-10), off(15), 30, "", "", "", None, "task"),
            (uid(), "Оптимизация маршрутов", "Проект", "Высокий",
             "Зоны доставки 2 и 3", off(-7), off(7), 40,
             "Приоритет — зона 3", "", "", None, "task"),
            (uid(), "Планёрка отдела логистики", "Рабочая", "Высокий",
             "Обсуждение KPI", off(1), off(1), 0, "", "09:00", "09:45", None, "meeting"),
            (uid(), "Ревью дизайна", "Проект", "Средний",
             "Обзор макетов", off(2), off(2), 0, "", "14:00", "15:00", None, "meeting"),
        ]
        c.executemany("""
            INSERT INTO tasks (id, name, category, priority, description,
                start_date, deadline, progress, notes, time_start, time_end, completed_at, type)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, seed)

    conn.commit()
    conn.close()


def uid():
    return uuid.uuid4().hex[:12]


def off(n):
    return (datetime.now() + timedelta(days=n)).strftime("%Y-%m-%d")


# ─── CRUD ────────────────────────────────────────────────

def get_all_data():
    sync_recurring_items()
    conn = get_conn()
    cats = [r["name"] for r in conn.execute("SELECT name FROM categories ORDER BY id").fetchall()]
    pris = [r["name"] for r in conn.execute("SELECT name FROM priorities ORDER BY sort_order").fetchall()]
    tasks_raw = conn.execute("SELECT * FROM tasks ORDER BY created_at").fetchall()
    tasks = []
    for t in tasks_raw:
        tasks.append({
            "id": t["id"],
            "name": t["name"],
            "desc": t["description"],
            "cat": t["category"],
            "pri": t["priority"],
            "start": t["start_date"],
            "deadline": t["deadline"],
            "progress": t["progress"],
            "notes": t["notes"],
            "timeStart": t["time_start"] or "",
            "timeEnd": t["time_end"] or "",
            "completedAt": t["completed_at"],
            "createdAt": t["created_at"],
            "type": t["type"] if "type" in t.keys() else "task",
            "result": t["result_text"] if "result_text" in t.keys() else "",
            "recurrenceRuleId": t["recurrence_rule_id"] if "recurrence_rule_id" in t.keys() else None,
            "reminderSent": t["reminder_sent"] if "reminder_sent" in t.keys() else 0,
            "overdueNotified": t["overdue_notified"] if "overdue_notified" in t.keys() else 0,
        })
    protected = [r["name"] for r in conn.execute("SELECT name FROM categories WHERE protected=1").fetchall()]
    conn.close()
    return {
        "categories": cats,
        "priorities": pris,
        "tasks": tasks,
        "protectedCats": protected,
        "recurrenceRules": get_recurrence_rules(),
    }


def add_task(data):
    conn = get_conn()
    tid = uid()
    category = data.get("cat")
    if data.get("type") == "meeting" and category == "Совещание":
        cat_row = conn.execute("SELECT name FROM categories ORDER BY id LIMIT 1").fetchone()
        category = cat_row["name"] if cat_row else "Рабочая"
    conn.execute("""
        INSERT INTO tasks (id, name, description, category, priority,
            start_date, deadline, progress, notes, time_start, time_end, completed_at, type, result_text, recurrence_rule_id)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        tid, data["name"], data.get("desc", ""), category, data["pri"],
        data.get("start", ""), data.get("deadline", ""),
        int(data.get("progress", 0)), data.get("notes", ""),
        data.get("timeStart", ""), data.get("timeEnd", ""),
        data.get("completedAt"),
        data.get("type", "task"),
        data.get("result", ""),
        data.get("recurrenceRuleId"),
    ))
    conn.commit()
    conn.close()
    return tid


def update_task(task_id, data):
    conn = get_conn()
    fields = []
    values = []
    mapping = {
        "name": "name", "desc": "description", "cat": "category",
        "pri": "priority", "start": "start_date", "deadline": "deadline",
        "progress": "progress", "notes": "notes",
        "timeStart": "time_start", "timeEnd": "time_end",
        "completedAt": "completed_at", "type": "type",
        "result": "result_text", "recurrenceRuleId": "recurrence_rule_id",
        "reminderSent": "reminder_sent", "overdueNotified": "overdue_notified",
    }
    for js_key, db_col in mapping.items():
        if js_key in data:
            fields.append(f"{db_col}=?")
            values.append(data[js_key])
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


def add_category(name):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        result = True
    except sqlite3.IntegrityError:
        result = False
    conn.close()
    return result


def delete_category(name):
    conn = get_conn()
    row = conn.execute("SELECT protected FROM categories WHERE name=?", (name,)).fetchone()
    if row and row["protected"]:
        conn.close()
        return False
    conn.execute("DELETE FROM categories WHERE name=?", (name,))
    conn.commit()
    conn.close()
    return True


def is_category_protected(name):
    conn = get_conn()
    row = conn.execute("SELECT protected FROM categories WHERE name=?", (name,)).fetchone()
    conn.close()
    return bool(row and row["protected"])


def add_priority(name):
    conn = get_conn()
    mx = conn.execute("SELECT COALESCE(MAX(sort_order),0)+1 FROM priorities").fetchone()[0]
    try:
        conn.execute("INSERT INTO priorities (name, sort_order) VALUES (?,?)", (name, mx))
        conn.commit()
        result = True
    except sqlite3.IntegrityError:
        result = False
    conn.close()
    return result


def delete_priority(name):
    conn = get_conn()
    conn.execute("DELETE FROM priorities WHERE name=?", (name,))
    conn.commit()
    conn.close()
    return True


def export_data():
    """Return full JSON for backup/export."""
    return json.dumps(get_all_data(), ensure_ascii=False, indent=2)


def import_data(json_str):
    """Import tasks from JSON backup."""
    data = json.loads(json_str)
    conn = get_conn()
    # Re-add categories
    for cat in data.get("categories", []):
        try:
            conn.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))
        except Exception:
            pass
    for pri in data.get("priorities", []):
        try:
            mx = conn.execute("SELECT COALESCE(MAX(sort_order),0)+1 FROM priorities").fetchone()[0]
            conn.execute("INSERT OR IGNORE INTO priorities (name, sort_order) VALUES (?,?)", (pri, mx))
        except Exception:
            pass
    for t in data.get("tasks", []):
        try:
            conn.execute("""
                INSERT OR REPLACE INTO tasks (id,name,description,category,priority,
                    start_date,deadline,progress,notes,time_start,time_end,completed_at,type,result_text,recurrence_rule_id)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                t.get("id", uid()), t["name"], t.get("desc", ""),
                t["cat"], t["pri"], t.get("start", ""), t.get("deadline", ""),
                int(t.get("progress", 0)), t.get("notes", ""),
                t.get("timeStart", ""), t.get("timeEnd", ""),
                t.get("completedAt"),
                t.get("type", "task"),
                t.get("result", ""),
                t.get("recurrenceRuleId"),
            ))
        except Exception:
            pass
    conn.commit()
    conn.close()


def get_recurrence_rules():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM recurrence_rules WHERE active=1 ORDER BY created_at DESC").fetchall()
    conn.close()
    return [{
        "id": r["id"],
        "itemType": r["item_type"],
        "name": r["name"],
        "desc": r["description"],
        "cat": r["category"],
        "pri": r["priority"],
        "notes": r["notes"],
        "timeStart": r["time_start"] or "",
        "timeEnd": r["time_end"] or "",
        "startDate": r["start_date"],
        "endDate": r["end_date"],
        "weekdays": json.loads(r["weekdays"] or "[]"),
        "everyDay": bool(r["every_day"]),
        "deadlineOffsetDays": r["deadline_offset_days"] or 0,
    } for r in rows]


def add_recurrence_rule(rule):
    conn = get_conn()
    rid = uid()
    conn.execute("""
        INSERT INTO recurrence_rules
        (id,item_type,name,description,category,priority,notes,time_start,time_end,start_date,end_date,weekdays,every_day,deadline_offset_days,last_generated_date)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        rid, rule["itemType"], rule["name"], rule.get("desc", ""), rule.get("cat"), rule["pri"],
        rule.get("notes", ""), rule.get("timeStart", ""), rule.get("timeEnd", ""),
        rule["startDate"], rule.get("endDate"), json.dumps(rule.get("weekdays", []), ensure_ascii=False),
        1 if rule.get("everyDay") else 0, int(rule.get("deadlineOffsetDays", 0)), None,
    ))
    conn.commit()
    conn.close()
    sync_recurring_items()
    return rid


def update_recurrence_rule(rule_id, rule):
    conn = get_conn()
    conn.execute("""
        UPDATE recurrence_rules SET item_type=?,name=?,description=?,category=?,priority=?,notes=?,time_start=?,time_end=?,
        start_date=?,end_date=?,weekdays=?,every_day=?,deadline_offset_days=?,last_generated_date=NULL
        WHERE id=?
    """, (
        rule["itemType"], rule["name"], rule.get("desc", ""), rule.get("cat"), rule["pri"], rule.get("notes", ""),
        rule.get("timeStart", ""), rule.get("timeEnd", ""), rule["startDate"], rule.get("endDate"),
        json.dumps(rule.get("weekdays", []), ensure_ascii=False), 1 if rule.get("everyDay") else 0,
        int(rule.get("deadlineOffsetDays", 0)), rule_id,
    ))
    conn.execute("""
        DELETE FROM tasks
        WHERE recurrence_rule_id=? AND start_date>=date('now','localtime') AND (completed_at IS NULL OR completed_at='')
    """, (rule_id,))
    conn.commit()
    conn.close()
    sync_recurring_items()


def delete_recurrence_rule(rule_id):
    conn = get_conn()
    conn.execute("UPDATE recurrence_rules SET active=0 WHERE id=?", (rule_id,))
    conn.commit()
    conn.close()


def _rule_matches(rule, day):
    if rule["every_day"]:
        return True
    weekdays = json.loads(rule["weekdays"] or "[]")
    if not weekdays:
        return False
    # Monday=0 ... Sunday=6
    return datetime.strptime(day, "%Y-%m-%d").weekday() in weekdays


def sync_recurring_items():
    conn = get_conn()
    rules = conn.execute("SELECT * FROM recurrence_rules WHERE active=1").fetchall()
    today = datetime.now().date()
    horizon = today + timedelta(days=30)
    for rule in rules:
        start = datetime.strptime(rule["start_date"], "%Y-%m-%d").date()
        end = datetime.strptime(rule["end_date"], "%Y-%m-%d").date() if rule["end_date"] else horizon
        end = min(end, horizon)
        if start > end:
            continue
        day = start
        while day <= end:
            d = day.strftime("%Y-%m-%d")
            if _rule_matches(rule, d):
                deadline = day + timedelta(days=int(rule["deadline_offset_days"] or 0))
                conn.execute("""
                    INSERT OR IGNORE INTO tasks (id,name,description,category,priority,start_date,deadline,progress,notes,time_start,time_end,type,result_text,recurrence_rule_id)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    uid(), rule["name"], rule["description"] or "", rule["category"] or "Рабочая",
                    rule["priority"], d, deadline.strftime("%Y-%m-%d"), 0, rule["notes"] or "",
                    rule["time_start"] or "", rule["time_end"] or "", rule["item_type"], "", rule["id"],
                ))
            day += timedelta(days=1)
        conn.execute("UPDATE recurrence_rules SET last_generated_date=? WHERE id=?", (end.strftime("%Y-%m-%d"), rule["id"]))
    conn.commit()
    conn.close()


def get_due_notifications(now_iso=None):
    conn = get_conn()
    now_dt = datetime.strptime(now_iso, "%Y-%m-%dT%H:%M") if now_iso else datetime.now()
    today = now_dt.strftime("%Y-%m-%d")
    notifications = []

    meetings = conn.execute("""
        SELECT * FROM tasks WHERE type='meeting' AND progress<100 AND reminder_sent=0
        AND start_date IS NOT NULL AND start_date!='' AND time_start IS NOT NULL AND time_start!=''
    """).fetchall()
    for m in meetings:
        start_dt = datetime.strptime(f"{m['start_date']} {m['time_start']}", "%Y-%m-%d %H:%M")
        delta = (start_dt - now_dt).total_seconds() / 60
        if 0 <= delta <= 5:
            notifications.append({"id": m["id"], "kind": "meeting_reminder", "title": "Скоро совещание", "text": f"«{m['name']}» начнётся в {max(1, int(delta))} мин."})
            conn.execute("UPDATE tasks SET reminder_sent=1 WHERE id=?", (m["id"],))

    overdue = conn.execute("""
        SELECT * FROM tasks WHERE type='task' AND progress<100 AND overdue_notified=0
        AND deadline IS NOT NULL AND deadline!='' AND deadline < ?
    """, (today,)).fetchall()
    for t in overdue:
        notifications.append({"id": t["id"], "kind": "task_overdue", "title": "Задача просрочена", "text": f"«{t['name']}» просрочена с {t['deadline']}."})
        conn.execute("UPDATE tasks SET overdue_notified=1 WHERE id=?", (t["id"],))

    conn.commit()
    conn.close()
    return notifications
