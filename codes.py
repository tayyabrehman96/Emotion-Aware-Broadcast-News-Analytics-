from moviepy.editor import VideoFileClip
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yt_dlp
from pytubefix import YouTube
import assemblyai as aai

#####################################################################################################

# YouTube API Key
api_key = 'AIzaSyB6El_mGw8lpuZ6MWqgvA_vVsqIdxl5hDE'

# Build the YouTube service object
youtube = build('youtube', 'v3', developerKey=api_key)

aai.settings.api_key = "faf583b5e8354055a1e310f4ec0632c0"

#####################################################################################################

def search_videos(query, max_results=5):
    try:
        request = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=max_results
        )
        response = request.execute()

        for i, item in enumerate(response['items']):
            print(f"{i+1}. Title: {item['snippet']['title']}")
            print(f"   Description: {item['snippet']['description']}")
            print(f"   Published At: {item['snippet']['publishedAt']}")
            print(f"   Channel Title: {item['snippet']['channelTitle']}")
            print(f"   Video ID: {item['id'].get('videoId', 'N/A')}\n")

        selection = int(input("Enter the index of the video you want to select: "))
        selected_video = response['items'][selection - 1]
        
        print("\nSelected Video:")
        print(f"Title: {selected_video['snippet']['title']}")
        print(f"Description: {selected_video['snippet']['description']}")
        print(f"Published At: {selected_video['snippet']['publishedAt']}")
        print(f"Channel Title: {selected_video['snippet']['channelTitle']}")
        print(f"Video ID: {selected_video['id'].get('videoId', 'N/A')}")

        return selected_video

    except (HttpError, IndexError, ValueError) as e:
        print(f"An error occurred: {e}")

#####################################################################################################

def download_video(video_id, output_path):
    try:
        
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(video_url)
        video_stream = yt.streams.get_highest_resolution()

        # Download and save to the output path
        video_file = video_stream.download(output_path=output_path)

        # Get the full path of the downloaded video
        downloaded_video_path = os.path.join(output_path, os.path.basename(video_file))

        return downloaded_video_path

    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
    
#####################################################################################################
    
def VideoTranscribe(path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(path)
    full_text = transcript.text

    return full_text

#####################################################################################################

def extract_audio(video_file):
    video = VideoFileClip(video_file)
    audio_file = video_file.split('.')[0] + '.wav'
    video.audio.write_audiofile(audio_file)
    return audio_file