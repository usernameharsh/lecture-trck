# ... (Keep get_playlist_video_ids and get_video_stats exactly the same) ...

# def get_playlist_video_ids(playlist_id):
#     video_ids = []
#     next_page_token = None
#     while True:
#         request = youtube.playlistItems().list(
#             part='contentDetails', playlistId=playlist_id, maxResults=50, pageToken=next_page_token
#         )
#         response = request.execute()
#         for item in response['items']:
#             video_ids.append(item['contentDetails']['videoId'])
#         next_page_token = response.get('nextPageToken')
#         if not next_page_token:
#             break
#     return video_ids

# def get_video_stats(video_ids):
#     video_stats = {}
#     for i in range(0, len(video_ids), 50):
#         chunk = video_ids[i:i+50]
#         request = youtube.videos().list(part='contentDetails,snippet', id=','.join(chunk))
#         response = request.execute()
#         for item in response['items']:
#             vid_id = item['id']
#             title = item['snippet']['title']
#             duration_iso = item['contentDetails']['duration']
#             duration_seconds = int(isodate.parse_duration(duration_iso).total_seconds())
#             video_stats[vid_id] = {'title': title, 'duration_seconds': duration_seconds}
#     return video_stats

# def calculate_eta(video_stats, watched_ids, playback_speed=1.0):
#     total_seconds = sum(stats['duration_seconds'] for stats in video_stats.values())
#     watched_seconds = sum(stats['duration_seconds'] for vid_id, stats in video_stats.items() if vid_id in watched_ids)
    
#     remaining_seconds = total_seconds - watched_seconds
#     real_eta_seconds = remaining_seconds / playback_speed

#     return {
#         'total_hours': round(total_seconds / 3600, 2),
#         'watched_hours': round(watched_seconds / 3600, 2),
#         'remaining_hours': round(remaining_seconds / 3600, 2),
#         'real_eta_hours_at_speed': round(real_eta_seconds / 3600, 2)
#     }

# # --- Execution ---
# if __name__ == '__main__':
#     database.init_db() # Ensure DB exists
    
#     TEST_PLAYLIST_ID = 'PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU' 
#     PLAYLIST_TITLE = "Python OOP Tutorials" # You can fetch this dynamically later
    
#     print("Fetching and saving playlist data...")
#     all_vids = get_playlist_video_ids(TEST_PLAYLIST_ID)
#     stats = get_video_stats(all_vids)
    
#     # Calculate total duration and save to DB
#     total_duration = sum(v['duration_seconds'] for v in stats.values())
#     database.add_playlist(TEST_PLAYLIST_ID, PLAYLIST_TITLE, total_duration)
    
#     # Simulate marking the first 3 videos as watched in the DB
#     for vid in all_vids[:3]:
#         database.mark_watched(vid, TEST_PLAYLIST_ID)
        
#     # Retrieve watched history from DB to calculate ETA
#     watched_from_db = database.get_watched_videos(TEST_PLAYLIST_ID)
#     progress = calculate_eta(stats, watched_from_db, playback_speed=1.5)
    
#     print(f"\nStats for {PLAYLIST_TITLE}:")
#     print(f"Total Videos: {len(all_vids)}")
#     print(f"Time Remaining (1x speed): {progress['remaining_hours']} hours")
#     print(f"Actual ETA (at 1.5x speed): {progress['real_eta_hours_at_speed']} hours")