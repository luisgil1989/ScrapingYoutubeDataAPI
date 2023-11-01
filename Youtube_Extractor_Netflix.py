# Import necessary libraries
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Set your YouTube Data API key
api_key = 'AIzaSyB0zkZTRGhRt05VHYbuTarj7ctTPaJYiCY'

# If you have multiple channel IDs, add them to this list
channel_ids = [
    'UCWOA1ZGywLbqmigxE4Qlvuw',  # Netflix
    'UCQJWtTnAHhEG5w4uN0udnUQ',  # PrimeVideo
    'UCx-KWLTKlB83hDI6UKECtJQ',  # HBOMAX
    'UC6pGDc4bFGD1_36IKv3FnYg',  # CrunchyRoll
    'UCPgMAS8woHJ_o_OZdTR7kcQ'  # Peacock
]

# Build a YouTube API client using your API key
youtube = build('youtube', 'v3', developerKey=api_key)


# Define a function to get channel statistics
def get_channel_stats(youtube, channel_ids):
    all_data = []  # Initialize an empty list to store channel data

    # Create a request to get channel statistics
    request = youtube.channels().list(
        part='snippet,statistics,contentDetails',  # Request specific parts of channel data
        id=','.join(channel_ids)  # Join multiple channel IDs into a single string
    )

    response = request.execute()  # Execute the request and get the response

    # Loop through the channel data in the response
    for item in response.get('items', []):
        data = {
            'Channel_name': item['snippet']['title'],  # Get channel name from snippet
            'Subscribers': item['statistics']['subscriberCount'],  # Get subscriber count
            'Views': item['statistics']['viewCount'],  # Get view count
            'Total_Videos': item['statistics']['videoCount'],  # Get total video count
            'Playlist_id': item['contentDetails']['relatedPlaylists']['uploads']  # Get playlist ID
        }
        all_data.append(data)  # Append the data to the list

    return all_data


# Call the function to get channel statistics
channel_statistics = get_channel_stats(youtube, channel_ids)

# Create a DataFrame from the channel statistics
channel_data = pd.DataFrame(channel_statistics)

#Funstion to get video ids
playlist_id = channel_data.loc[channel_data['Channel_name'] == 'Netflix', 'Playlist_id'].iloc[0]

# Function to get video ids
def get_video_ids(youtube, playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return video_ids

# Call the function to get video IDs
video_ids_response = get_video_ids(youtube, playlist_id)



#Function to get video details

def get_video_details(youtube, video_ids):
    all_video_stats = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids[i:i+50])
        )

        response = request.execute()

        for video in response['items']:
            video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = video['statistics']['viewCount'],
                               Likes=video['statistics']['viewCount'],
                               Dislikes=video['statistics']['viewCount'],
                               Comments=video['statistics']['viewCount'],
                               )

            all_video_stats.append(video_stats)

    return all_video_stats

# Call the function to get video details
video_details = get_video_details(youtube, video_ids_response)
video_data = pd.DataFrame(video_details)



video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Dislikes'] = pd.to_numeric(video_data['Dislikes'])

top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)


ax2 = sns.barplot(x='Views', y='Title', data=top10_videos, color='red')

# Set the title of the plot
plt.title('Top 10 Videos by Views in Netflix', fontsize=20, fontweight='bold')

# Set the x and y labels with increased font size
plt.xlabel('Views', fontsize=14, fontweight='bold')
plt.ylabel('video Title', fontsize=14, fontweight='bold')
plt.show()



