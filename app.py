from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import tracker_core
import database

app = Flask(__name__)

def get_playlists():
    """Fetches all playlists, including the new category tag."""
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    # Fallback applied just in case the database update takes a second
    try:
        cursor.execute('SELECT playlist_id, title, total_duration_seconds, category FROM Playlists')
    except sqlite3.OperationalError:
        cursor.execute('SELECT playlist_id, title, total_duration_seconds, "General" as category FROM Playlists')
    playlists = cursor.fetchall()
    conn.close()
    return playlists

@app.route('/')
def home():
    saved_playlists = get_playlists()
    return render_template('index.html', playlists=saved_playlists)

@app.route('/playlist/<playlist_id>')
def view_playlist(playlist_id):
    watched_vids = database.get_watched_videos(playlist_id)
    vids = tracker_core.get_playlist_video_ids(playlist_id)
    stats = tracker_core.get_video_stats(vids)
    
    progress = tracker_core.calculate_eta(stats, watched_vids, playback_speed=1.5)
    
    # Fetch user notes for this specific playlist
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT video_id, note_text FROM Notes WHERE playlist_id = ?', (playlist_id,))
    notes_dict = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    
    return render_template('playlist.html', 
                           stats=stats, 
                           progress=progress, 
                           playlist_id=playlist_id,
                           watched=watched_vids,
                           notes=notes_dict)

@app.route('/add', methods=['POST'])
def add_playlist():
    raw_url = request.form.get('playlist_url')
    category = request.form.get('category', 'General')
    
    playlist_id = raw_url
    if 'list=' in raw_url:
        playlist_id = raw_url.split('list=')[1].split('&')[0]
        
    try:
        print(f"Fetching data for {playlist_id}...")
        vids = tracker_core.get_playlist_video_ids(playlist_id)
        stats = tracker_core.get_video_stats(vids)
        total_duration = sum(v['duration_seconds'] for v in stats.values())
        
        database.add_playlist(playlist_id, f"Course: {playlist_id[:8]}...", total_duration)
        
        # Instantly tag it with the user's subject
        conn = sqlite3.connect('tracker.db')
        conn.execute("UPDATE Playlists SET category = ? WHERE playlist_id = ?", (category, playlist_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))
        
    except Exception as e:
        return f"An error occurred: {e}. Make sure the playlist is public!"
    
@app.route('/toggle', methods=['POST'])
def toggle_video():
    data = request.json
    video_id = data.get('video_id')
    playlist_id = data.get('playlist_id')
    is_checked = data.get('is_checked')
    
    if is_checked:
        database.mark_watched(video_id, playlist_id)
    else:
        database.unmark_watched(video_id, playlist_id)
        
    return jsonify({"status": "success"})

@app.route('/save_note', methods=['POST'])
def save_note():
    data = request.json
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    # Saves or updates the text instantly based on video ID
    cursor.execute('''
        INSERT INTO Notes (video_id, playlist_id, note_text)
        VALUES (?, ?, ?)
        ON CONFLICT(video_id, playlist_id)
        DO UPDATE SET note_text=excluded.note_text
    ''', (data.get('video_id'), data.get('playlist_id'), data.get('note_text')))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/delete/<playlist_id>', methods=['POST'])
def delete_course(playlist_id):
    database.delete_playlist(playlist_id)
    return redirect(url_for('home'))

@app.route('/update_category', methods=['POST'])
def update_category():
    data = request.json
    playlist_id = data.get('playlist_id')
    new_category = data.get('category')
    
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Playlists SET category = ? WHERE playlist_id = ?", (new_category, playlist_id))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})
if __name__ == '__main__':
    app.run(debug=True)