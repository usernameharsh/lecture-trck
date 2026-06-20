A full-stack web application designed to help students track their progress through long-form educational YouTube courses.
Features
One-Click Import: Paste any YouTube playlist URL to instantly scrape video titles, durations, and metadata using the YouTube Data API.

Interactive Dashboard: View all active courses as clean, responsive cards displaying total watch time and current completion percentage.

Dynamic Checklists: Click into a course to view a full syllabus checklist. Mark videos as "watched" with asynchronous JavaScript updates.

Real-Time Analytics: Instantly recalculates remaining time and progress bars as you check off lectures.

Database Management: Safely delete completed courses and clear associated watch history from the database

Tech Stack
Backend: Python, Flask

Database: SQLite (Persistent relational storage)

Frontend: HTML5, Vanilla JavaScript (Fetch API), Tailwind CSS (via CDN)

External APIs: YouTube Data API v3 (google-api-python-client)

Environment: python-dotenv for secure credential management
Local Installation
1. Clone the repository
2. set up virtual envirment
3. install requrired dependencies pip install -r requirements.txt
4. Set up your environment variables
Create a .env file in the root directory and add your YouTube Data API key:
initiliase database and run !!!
Deployment
This application is configured for production deployment on PythonAnywhere using WSGI.

Ensure that your tracker.db, .env, and .venv/ directories are included in your .gitignore prior to deployment to protect your API keys and prevent database overwriting on the production server. The production database must be initialized manually via the server's bash console before first use.
