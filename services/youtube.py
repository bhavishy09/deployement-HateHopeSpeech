# -*- coding: utf-8 -*-
"""
This script uses the YouTube Data API to fetch comments and analyze them.
"""
import os
import re
import googleapiclient.discovery
import googleapiclient.errors
from langdetect import detect
from services.hate_classifier import predict_hope_hate

# --- IMPORTANT ---
# The YouTube Data API v3 Key is loaded from environment variables
DEVELOPER_KEY = os.environ.get("YOUTUBE_API_KEY")
# -----------------

# 1. YouTube API Setup
api_service_name = "youtube"
api_version = "v3"

youtube = None
if DEVELOPER_KEY:
    try:
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY
        )
    except Exception as e:
        print(f"❌ Error creating YouTube API service: {e}")
        print("Please ensure your YOUTUBE_API_KEY is correct and the API is enabled.")
else:
    print("❌ YOUTUBE_API_KEY not found in environment variables.")
    print("Please set it in your .env file to use YouTube features.")

# 2. Helper Functions
def is_english(text):
    """Checks if text is English."""
    try:
        return detect(text) == "en"
    except:
        return False

def contains_text(text):
    """Checks if the string contains at least one alphanumeric character."""
    return any(c.isalnum() for c in text)

def extract_video_id(video_input):
    """Extracts YouTube video ID from a URL or ID string."""
    match = re.search(r"(?:v=|youtu\.be/|embed/|watch\?v=)([A-Za-z0-9_-]+)", video_input)
    if match:
        return match.group(1)
    # Assume it's already an ID if no match
    return video_input.strip()

# 3. Main Analysis Function
def analyze_youtube_comments(video_id):
    """
    Fetches comments for a given video ID and performs hope/hate analysis.
    """
    if not youtube:
        raise ConnectionError("YouTube API service is not available.")

    hope_count = 0
    hate_count = 0
    comments_processed = 0
    results = []
    nextPageToken = None

    print(f"\n--- Starting Comment Analysis for Video ID: {video_id} ---")
    try:
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,  # Max allowed by API
                order="time", # Change order to time
                pageToken=nextPageToken,
                textFormat="plainText"
            )
            response = request.execute()

            for item in response["items"]:
                comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                
                if not is_english(comment_text) or not contains_text(comment_text):
                    continue

                out = predict_hope_hate(comment_text)
                comments_processed += 1

                print(f"Comment: {comment_text[:70]}...") # Print first 70 chars of comment
                print(f"Prediction: {out}") # Print the prediction result

                if comments_processed % 20 == 0:
                    print(f"...processed {comments_processed} comments")

                results.append(out)
                if out["hope_hate"].lower() == "hope":
                    hope_count += 1
                else:
                    hate_count += 1

            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:
                print("--- Reached end of comments ---")
                break

    except googleapiclient.errors.HttpError as e:
        error_message = f"An API error occurred: {e}. This could be due to an invalid API key, disabled API, or an invalid Video ID."
        print(f"\n❌ {error_message}")
        # Return what we have so far, along with the error
        return {
            "error": error_message,
            "hope_count": hope_count,
            "hate_count": hate_count,
            "comments_processed": comments_processed,
            "results": results
        }
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(f"\n❌ {error_message}")
        return {
            "error": error_message,
            "hope_count": hope_count,
            "hate_count": hate_count,
            "comments_processed": comments_processed,
            "results": results
        }

    print("\n--- Analysis Complete ---")
    print(f"Total Comments Processed: {comments_processed}")
    print(f"Hope Count: {hope_count}")
    print(f"Hate Count: {hate_count}\n")
    
    return {
        "hope_count": hope_count,
        "hate_count": hate_count,
        "comments_processed": comments_processed,
        "results": results
    }
