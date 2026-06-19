import sqlite3

def init_db(db_name='tracker.db'):
    """Creates the database and necessary tables."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Store overarching playlist data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Playlists (
            playlist_id TEXT PRIMARY KEY,
            title TEXT,
            total_duration_seconds INTEGER
        )
    ''')

    # Track individual video completion states
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Watched (
            video_id TEXT PRIMARY KEY,
            playlist_id TEXT,
            FOREIGN KEY(playlist_id) REFERENCES Playlists(playlist_id)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' initialized successfully.")

if __name__ == '__main__':
    init_db()

def add_playlist(playlist_id, title, total_duration_seconds):
    """Saves or updates a playlist in the database."""
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO Playlists (playlist_id, title, total_duration_seconds)
        VALUES (?, ?, ?)
    ''', (playlist_id, title, total_duration_seconds))
    conn.commit()
    conn.close()

def mark_watched(video_id, playlist_id):
    """Logs a specific video as watched."""
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO Watched (video_id, playlist_id)
        VALUES (?, ?)
    ''', (video_id, playlist_id))
    conn.commit()
    conn.close()

def get_watched_videos(playlist_id):
    """Retrieves a list of all watched video IDs for a playlist."""
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT video_id FROM Watched WHERE playlist_id = ?', (playlist_id,))
    watched_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return watched_ids
def unmark_watched(video_id, playlist_id):
    """Removes a video from the watched list."""
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Watched WHERE video_id = ? AND playlist_id = ?', 
                  (video_id, playlist_id))
    conn.commit()
    conn.close()
def delete_playlist(playlist_id):
    """Permanently deletes a playlist and its watched history from the database."""
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    # Delete the playlist entry
    cursor.execute('DELETE FROM Playlists WHERE playlist_id = ?', (playlist_id,))
    # Delete the associated watched history
    cursor.execute('DELETE FROM Watched WHERE playlist_id = ?', (playlist_id,))
    conn.commit()
    conn.close()