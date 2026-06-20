import sqlite3

conn = sqlite3.connect('tracker.db')
cursor = conn.cursor()

# 1. Add the category column
try:
    cursor.execute("ALTER TABLE Playlists ADD COLUMN category TEXT DEFAULT 'General'")
except sqlite3.OperationalError:
    pass # Column already exists

# 2. Build the Notes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Notes (
    video_id TEXT, 
    playlist_id TEXT, 
    note_text TEXT,
    PRIMARY KEY(video_id, playlist_id)
)
''')

conn.commit()
conn.close()
print("Local database upgraded successfully!")