import sys
import database
import tracker_core

def main():
    database.init_db()
    
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python cli.py add <playlist_id>")
        print("  python cli.py status <playlist_id>")
        return

    command = sys.argv[1].lower()
    playlist_id = sys.argv[2]

    if command == 'add':
        print("Fetching playlist data from YouTube...")
        vids = tracker_core.get_playlist_video_ids(playlist_id)
        stats = tracker_core.get_video_stats(vids)
        total_duration = sum(v['duration_seconds'] for v in stats.values())
        
        # We can dynamically fetch the title later, using a placeholder for now
        database.add_playlist(playlist_id, "Imported Playlist", total_duration)
        print(f"Success! Added {len(vids)} videos to your local database.")

    elif command == 'status':
        print("Calculating ETA...")
        vids = tracker_core.get_playlist_video_ids(playlist_id)
        stats = tracker_core.get_video_stats(vids)
        watched_vids = database.get_watched_videos(playlist_id)
        
        progress = tracker_core.calculate_eta(stats, watched_vids, playback_speed=1.5)
        
        print("\n--- Playlist Status ---")
        print(f"Progress: {len(watched_vids)} / {len(vids)} videos watched")
        print(f"Time Completed: {progress['watched_hours']} hours")
        print(f"Remaining (1x): {progress['remaining_hours']} hours")
        print(f"ETA at 1.5x speed: {progress['real_eta_hours_at_speed']} hours")

if __name__ == '__main__':
    main()