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
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (category) REFERENCES categories(name),
            FOREIGN KEY (priority) REFERENCES priorities(name)
        )
    """)

    # Seed defaults if empty
    cats = c.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    if cats == 0:
        defaults = [
            ("Рабочая", 0), ("Совещание", 1), ("Проект", 0),
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
        seed = [
            (uid(), "Подготовить отчёт Q1", "Рабочая", "Высокий",
             "Сводный отчёт за квартал с графиками", today, off(3), 35,
             "Нужны данные от финансов", "", "", None),
            (uid(), "Совещание по проекту Alpha", "Совещание", "Средний",
             "Еженедельный статус-митинг", today, today, 0,
             "Презентация на 5 слайдов", "10:00", "11:30", None),
            (uid(), "Обновить тарифы на сайте", "Проект", "Высокий",
             "Актуализация цен", off(-5), off(-1), 45,
             "Согласовать с маркетингом", "", "", None),
            (uid(), "Курс по аналитике", "Обучение", "Низкий",
             "Модуль 3 из 8", off(-10), off(15), 30, "", "", "", None),
            (uid(), "Оптимизация маршрутов", "Проект", "Высокий",
             "Зоны доставки 2 и 3", off(-7), off(7), 40,
             "Приоритет — зона 3", "", "", None),
            (uid(), "Планёрка отдела логистики", "Совещание", "Высокий",
             "Обсуждение KPI", off(1), off(1), 0, "", "09:00", "09:45", None),
            (uid(), "Ревью дизайна", "Совещание", "Средний",
             "Обзор макетов", off(2), off(2), 0, "", "14:00", "15:00", None),
        ]
        c.executemany("""
            INSERT INTO tasks (id, name, category, priority, description,
                start_date, deadline, progress, notes, time_start, time_end, completed_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, seed)

    conn.commit()
    conn.close()


def uid():
    return uuid.uuid4().hex[:12]


def off(n):
    return (datetime.now() + timedelta(days=n)).strftime("%Y-%m-%d")


# ─── CRUD ────────────────────────────────────────────────

def get_all_data():
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
        })
    protected = [r["name"] for r in conn.execute("SELECT name FROM categories WHERE protected=1").fetchall()]
    conn.close()
    return {
        "categories": cats,
        "priorities": pris,
        "tasks": tasks,
        "protectedCats": protected,
    }


def add_task(data):
    conn = get_conn()
    tid = uid()
    conn.execute("""
        INSERT INTO tasks (id, name, description, category, priority,
            start_date, deadline, progress, notes, time_start, time_end, completed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        tid, data["name"], data.get("desc", ""), data["cat"], data["pri"],
        data.get("start", ""), data.get("deadline", ""),
        int(data.get("progress", 0)), data.get("notes", ""),
        data.get("timeStart", ""), data.get("timeEnd", ""),
        data.get("completedAt"),
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
        "completedAt": "completed_at",
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
                    start_date,deadline,progress,notes,time_start,time_end,completed_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                t.get("id", uid()), t["name"], t.get("desc", ""),
                t["cat"], t["pri"], t.get("start", ""), t.get("deadline", ""),
                int(t.get("progress", 0)), t.get("notes", ""),
                t.get("timeStart", ""), t.get("timeEnd", ""),
                t.get("completedAt"),
            ))
        except Exception:
            pass
    conn.commit()
    conn.close()
