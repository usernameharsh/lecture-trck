from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import tracker_core
import database

app = Flask(__name__)

def get_playlists():
    """Fetches all playlists currently saved in your database."""
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    # Grabs the ID, Title, and total duration
    cursor.execute('SELECT playlist_id, title, total_duration_seconds FROM Playlists')
    playlists = cursor.fetchall()
    conn.close()
    return playlists

@app.route('/')
def home():
    # Gets the data and sends it to the HTML file
    saved_playlists = get_playlists()
    return render_template('index.html', playlists=saved_playlists)
# Add these to your imports at the very top
import tracker_core
import database

# Add this below your existing home() route
@app.route('/playlist/<playlist_id>')
def view_playlist(playlist_id):
    watched_vids = database.get_watched_videos(playlist_id)
    vids = tracker_core.get_playlist_video_ids(playlist_id)
    stats = tracker_core.get_video_stats(vids)
    
    # Let's default to 1.5x speed for the web view
    progress = tracker_core.calculate_eta(stats, watched_vids, playback_speed=1.5)
    
    return render_template('playlist.html', 
                           stats=stats, 
                           progress=progress, 
                           playlist_id=playlist_id,
                           watched=watched_vids)

@app.route('/add', methods=['POST'])
def add_playlist():
    # 1. Grab the text the user pasted into the box
    raw_url = request.form.get('playlist_url')
    
    # 2. Smart Extraction: If they paste a full URL, we just want the ID part at the end
    playlist_id = raw_url
    if 'list=' in raw_url:
        playlist_id = raw_url.split('list=')[1].split('&')[0]
        
    try:
        # 3. Use our core engine to fetch the data from YouTube
        print(f"Fetching data for {playlist_id}...")
        vids = tracker_core.get_playlist_video_ids(playlist_id)
        stats = tracker_core.get_video_stats(vids)
        total_duration = sum(v['duration_seconds'] for v in stats.values())
        
        # 4. Save it to our database
        database.add_playlist(playlist_id, f"Course: {playlist_id[:8]}...", total_duration)
        
        # 5. Refresh the homepage so the new card appears!
        return redirect(url_for('home'))
        
    except Exception as e:
        return f"An error occurred: {e}. Make sure the playlist is public!"
    
@app.route('/toggle', methods=['POST'])
def toggle_video():
    # Grabs the data sent by the checkbox
    data = request.json
    video_id = data.get('video_id')
    playlist_id = data.get('playlist_id')
    is_checked = data.get('is_checked')
    
    # Updates the database instantly
    if is_checked:
        database.mark_watched(video_id, playlist_id)
    else:
        database.unmark_watched(video_id, playlist_id)
        
    return jsonify({"status": "success"})
@app.route('/delete/<playlist_id>', methods=['POST'])
def delete_course(playlist_id):
    # Call the new database function
    database.delete_playlist(playlist_id)
    # Send the user back to the updated dashboard
    return redirect(url_for('home'))
if __name__ == '__main__':
    # debug=True means the server auto-reloads if you change the code
    app.run(debug=True)