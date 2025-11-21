
# services/youtube_tracker.py
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time
import csv
import os
from datetime import datetime
import pytz
import random
import traceback
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# ---------- CONFIG / DEFAULTS ----------
TIMEZONE = "Asia/Kolkata"
PLOT_DIR = os.path.join("static", "images", "tracker")
DATA_DIR = os.path.join("instance", "tracker_data")
API_KEY = os.getenv("YOUTUBE_API_KEY")
# ---------------------------------------

def get_youtube_service():
    """Builds and returns the YouTube API service object."""
    if not API_KEY:
        print("YOUTUBE_API_KEY not found in .env file.")
        return None
    try:
        return build('youtube', 'v3', developerKey=API_KEY)
    except Exception as e:
        print("Error creating YouTube service:", e)
        return None

def fetch_video_and_channel_stats(youtube, video_id):
    """
    Fetches video and channel statistics from the YouTube API.
    Returns (views, likes, subs, channel_id).
    """
    try:
        resp = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
        items = resp.get('items', [])
        if not items:
            return None, None, None, None
        
        stats = items[0].get('statistics', {})
        snippet = items[0].get('snippet', {})
        views = int(stats.get('viewCount', 0))
        likes = int(stats.get('likeCount', 0))
        channel_id = snippet.get('channelId')
        
        subs = None
        if channel_id:
            ch_resp = youtube.channels().list(part='statistics', id=channel_id).execute()
            ch_items = ch_resp.get('items', [])
            if ch_items:
                ch_stats = ch_items[0].get('statistics', {})
                subs = int(ch_stats.get('subscriberCount', 0))
        
        return views, likes, subs, channel_id
    except Exception as e:
        print("Exception while fetching from YouTube API:", e)
        traceback.print_exc()
        return None, None, None, None

def fetch_simulated_stats(video_id):
    """
    Generates simulated statistics for testing without an API key.
    """
    seed = int(time.time() // 60) + sum(ord(c) for c in video_id)
    random.seed(seed)
    views = (seed % 1000) + 100 + random.randint(0, 300)
    likes = max(0, int(views * random.uniform(0.01, 0.07)))
    subs = 500 + random.randint(0, 50)
    return views, likes, subs, "SIMULATED_CHANNEL"

def append_row(path, ts_unix, iso, views, likes, subs):
    """Appends a row of data to the specified CSV file."""
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([ts_unix, iso,
                         views if views is not None else "",
                         likes if likes is not None else "",
                         subs if subs is not None else ""])

def plot_data(csv_path, video_id, interval_min):
    """Generates and saves plots for views, likes, and subscribers."""
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return []

    df = pd.read_csv(csv_path)
    if 'iso' not in df.columns or len(df) < 2:
        print("Not enough data to plot.")
        return []

    df['iso_dt'] = pd.to_datetime(df['iso'])
    df = df.sort_values('iso_dt')
    df['views'] = pd.to_numeric(df['views'], errors='coerce').fillna(method='ffill')
    df['likes'] = pd.to_numeric(df['likes'], errors='coerce').fillna(method='ffill')
    df['subscribers'] = pd.to_numeric(df['subscribers'], errors='coerce').fillna(method='ffill')

    tz = pytz.timezone(TIMEZONE)
    locator = mdates.MinuteLocator(interval=max(1, int(interval_min / 5)))
    formatter = mdates.DateFormatter('%H:%M', tz=tz)
    
    plot_files = []
    plot_configs = [
        ('views', 'Views', 'blue'),
        ('likes', 'Likes', 'orange'),
        ('subscribers', 'Subscribers', 'green')
    ]

    for column, title, color in plot_configs:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df['iso_dt'], df[column], marker='o', linestyle='-', label=title, color=color)
        ax.set_xlabel(f'Time ({TIMEZONE})')
        ax.set_ylabel('Count')
        ax.set_title(f'{title} over Time for video {video_id}')
        ax.legend()
        ax.grid(True)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        plt.tight_layout()

        plot_filename = f"{video_id}_{column}_{int(time.time())}.png"
        plot_filepath = os.path.join(PLOT_DIR, plot_filename)
        
        try:
            plt.savefig(plot_filepath)
            plot_files.append(os.path.join('images', 'tracker', plot_filename))
        except Exception as e:
            print(f"Could not save {column} plot: {e}")
        
        plt.close(fig)

    return plot_files

def track_video_stats(video_id, interval_min=1, samples=5):
    """
    Main function to track video stats and generate plots.
    """
    youtube = get_youtube_service()
    simulate = not youtube

    if simulate:
        print("Running in SIMULATED mode.")

    # Create a unique CSV file for this tracking session
    csv_filename = f"{video_id}_{int(time.time())}.csv"
    csv_filepath = os.path.join(DATA_DIR, csv_filename)

    # Ensure CSV has headers
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp_unix", "iso", "views", "likes", "subscribers"])

    tz = pytz.timezone(TIMEZONE)

    for i in range(samples):
        ts_unix = int(time.time())
        iso = datetime.fromtimestamp(ts_unix, tz).isoformat()

        if simulate:
            views, likes, subs, _ = fetch_simulated_stats(video_id)
        else:
            views, likes, subs, _ = fetch_video_and_channel_stats(youtube, video_id)
        
        append_row(csv_filepath, ts_unix, iso, views, likes, subs)
        print(f"Sample #{i+1}/{samples} -> views: {views}, likes: {likes}, subs: {subs}")

        if i < samples - 1:
            time.sleep(interval_min * 60)

    plot_files = plot_data(csv_filepath, video_id, interval_min)
    
    # Clean up the CSV file after generating plots
    try:
        os.remove(csv_filepath)
    except OSError as e:
        print(f"Error removing CSV file {csv_filepath}: {e}")

    return plot_files
