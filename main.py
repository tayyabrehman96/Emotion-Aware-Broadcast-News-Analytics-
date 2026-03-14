import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from codes import search_videos, download_video, VideoTranscribe
from googleapiclient.discovery import build
from modeling import label_topics
from semantic_segmentation import get_segments
from save_data import save_file
from plot_data import plot_file
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt


#############################################################################################################

api_key = 'AIzaSyB6El_mGw8lpuZ6MWqgvA_vVsqIdxl5hDE'
youtube = build('youtube', 'v3', developerKey=api_key)

##############################################################################################################

# try:
#     search = input("Search: ", )
#     selected_video =  search_videos(search)
#     pdate = selected_video['snippet']['publishedAt']
#     print("#########################################")
#     print(pdate)
# except Exception as e:
#     print(f"Error occurred: {e}")

##############################################################################################################

# try:
#     video_id = selected_video['id']['videoId']
#     output_path = "downloads"
#     os.makedirs(output_path, exist_ok=True)
#     video_file_path = download_video(video_id, output_path)

#     print("File Path: ", video_file_path)

# except Exception as e:
#     print(f"Error occurred: {e}")


##############################################################################################################

# try:
#     text = VideoTranscribe(video_file_path)
#     print(text)

# except Exception as e:
#     print(f"Error occurred: {e}")

##############################################################################################################

# try:
#     segments = get_segments(text)    

#     print("################# Segments #################")
#     print(segments)
# except Exception as e:
#     print(f"Error occurred: {e}")

##############################################################################################################

video_file_path = 'C:\\Users\\pc\\Desktop\\Project\\downloads\\China Pushes for Peace in Russia-Ukraine ｜ Dawn News English.mp4'
try:
    segments = get_segments(video_file_path)    

    print("################# Segments #################")
    print(segments)
except Exception as e:
    print(f"Error occurred: {e}")


##############################################################################################################

from sentiment_analysis import get_sentiment

topics = []
sentiments = []
chunks = []
h_scores = []
l_scores = []

try:
    for i in segments:
        # print(f"Paragraph {i+1}:\n{paragraph}\n{'-'*80}\n")

        print("Labeling........")
        topic = label_topics(i)
        topics.append(topic)

        print("Sentiment Analysis........")
        rephrased, sentiment, h_before, l_after = get_sentiment(i)
        sentiments.append(sentiment)

        chunks.append(rephrased)
        h_scores.append(h_before)
        l_scores.append(l_after)

except Exception as e:
    print(f"Error occurred: {e}")

# current_date = str(datetime.date.today())

##############################################################################################################

# Create or update the Excel file
excel_file_path = 'C:\\Users\\pc\\Desktop\\Project\\sheet\\NewsData.xlsx'
current_date = str(datetime.date.today())
save_file(excel_file_path, topics, sentiments, chunks, current_date, h_scores, l_scores)

##############################################################################################################

plot_file(excel_file_path)