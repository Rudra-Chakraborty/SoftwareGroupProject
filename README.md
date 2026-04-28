//SkyTrack
SkyTrack is a team management and coordination web app built with Django as a group university project. It lets staff log in, view their organisation's teams and departments, send internal messages, schedule meetings, and pull reports — all in one place.
The project was split across five students, each owning a module, then integrated into a single codebase at the end.

What we built
Authentication & core (Student 2)
Login and session management using a custom User model rather than Django's built-in one. Staff profiles are stored separately in a Staff table linked to the user. A custom middleware (GroupSessionToDjangoAuthMiddleware) bridges the group session with Django's auth system so that the different modules can all check login state consistently without rewriting each other's code.
Teams & departments (Student 1)
The main organisational layer. Teams belong to departments, have managers, skills, contact info, and can depend on other teams (upstream/downstream dependencies). The dependency view lets you see the full chain of which teams rely on which. There's also a seed command (python manage.py seed_student1) that loads real team data from the organisation registry into the database.
Messaging (Student 3)
Internal messaging between staff members. Users have an inbox, outbox, and compose page. Messages are stored with sender/receiver references to the custom User model and ordered by timestamp.
Schedule (Student 4)
A personal meeting scheduler built as its own Django app. The schedule page has three views — upcoming list, week grid, and month calendar — all on one page without any page reloads. You can create, edit, and delete meetings through a modal form. Created meetings show up immediately in the upcoming list and on the calendar. The mini calendar on the right shows dots on days that have meetings.
Reports (Student 5)
A dashboard pulling stats across the whole organisation — total departments, teams, members, and inactive teams. Charts are rendered in the browser using Chart.js. The page also supports exporting the full data as a PDF or as a multi-sheet Excel file with a bar chart included in the Excel output.

Project structure
skytrack/        Django project settings, URLs, middleware
main/            Auth, dashboard, profile, messaging views
teams/           Teams, departments, dependencies
meetings/        Personal schedule and calendar app
reports/         Analytics dashboard and PDF/Excel export
web_pages/       Shared HTML templates (base, login, dashboard etc.)
assets/          Static files (CSS, images)

Requirements

Python 3.10+
Django 5.x
reportlab (PDF export)
openpyxl (Excel export)


How to run it
1. Clone the repo
bashgit clone https://github.com/your-org/skytrack.git
cd skytrack
2. Create and activate a virtual environment
bashpython -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
3. Install dependencies
bashpip install -r requirements.txt
4. Run migrations
bashpython manage.py migrate
5. Load team data
This seeds the database with team and department records:
bashpython manage.py seed_student1
6. Install export libraries
Needed for the PDF and Excel buttons on the reports page:
bashpython manage.py install_packages
7. Create an admin account
bashpython manage.py createsuperuser
8. Start the server
bashpython manage.py runserver
Then open http://127.0.0.1:8000 in your browser.

Pages
URLWhat it does/Login/dashboard/Home/profile/Staff profile/messages/Inbox/messages/outbox/Outbox/messages/compose/Compose/teams/All teams/teams/dependencies/Dependency map/teams/departments/Departments/meetings/Schedule/reports/Analytics dashboard/reports/pdf/Download PDF/reports/excel/Download Excel/admin/Django admin

A few things worth knowing
The database is SQLite and a db.sqlite3 file is included with seed data already loaded. If you want a clean slate delete it and run migrate and seed_student1 again.
DEBUG = True in settings which is fine for running it locally. The secret key in settings is just a placeholder — change it before putting this anywhere public.
The export buttons on the reports page need reportlab and openpyxl installed. Running python manage.py install_packages handles that automatically.
