# Smart Planner Pro — Windows Desktop Application

## Установка и запуск (из исходников)

```bash
pip install -r requirements.txt
python smart_planner.py
```

## Структура файлов

```
smart_planner_app/
├── smart_planner.py   — Главный файл (pywebview + фоновый поток)
├── database.py        — SQLite (задачи, совещания, циклы, уведомления)
├── api.py             — Python↔JavaScript API мост
├── app.html           — Весь UI (React + CSS)
├── requirements.txt   — Зависимости
└── smart_planner.db   — БД (создаётся автоматически)
```

## Сборка в .exe через GitHub Actions

В файле `.github/workflows/build.yml` строка сборки должна быть:

```
pyinstaller --onefile --windowed --name "SmartPlanner" --add-data "app.html;." --hidden-import "webview.platforms.edgechromium" --hidden-import "webview.platforms.winforms" --hidden-import "clr_loader" --collect-all "webview" smart_planner.py
```

**Важно:** ключ `--add-data "app.html;."` обязателен.
