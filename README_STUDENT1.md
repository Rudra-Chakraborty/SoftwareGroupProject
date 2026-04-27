# SkyTrack Student 1 - Team Module with Spreadsheet Registry Data

This version includes the Student 1 Django frontend/backend and a pre-loaded `db.sqlite3` generated from the uploaded spreadsheet:

`Agile Project Module UofW - Team Registry.xlsx`

## Imported data

- 6 departments
- 46 teams
- 230 team members (team leader + 4 engineers per team)
- 52 upstream/downstream dependency links
- Team leaders and department heads added as Django users
- Existing admin/superuser accounts preserved in the database

## How to run in VS Code

1. Open this folder in VS Code.
2. Open Terminal.
3. Activate your virtual environment:

```powershell
venv\Scriptsctivate
```

4. Install dependencies if needed:

```powershell
pip install -r requirements.txt
```

5. Because the database is already included, you can usually run:

```powershell
python manage.py runserver
```

6. Open:

```text
http://127.0.0.1:8000/
```

## If tables are missing or database is reset

Run:

```powershell
python manage.py migrate
python manage.py seed_student1
```

## Important URLs

- Login: http://127.0.0.1:8000/
- Register: http://127.0.0.1:8000/register/
- Teams: http://127.0.0.1:8000/teams/
- Meetings: http://127.0.0.1:8000/teams/meetings/
- Admin: http://127.0.0.1:8000/admin/

## Database file

The updated database is:

```text
db.sqlite3
```

You can also open this file in SQLiteStudio.
