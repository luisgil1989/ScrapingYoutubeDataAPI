# Import necessary libraries
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


########################################################################################################################
# Important note:
#
# Create a project in the Google Developer Console:
#
# To obtain an API key for YouTube Data API, you need to create a project in the Google Developer Console.
# Follow these steps:
#
# a. Go to Google Developer Console.
#
# b. Create a new project or select an existing one.
#
# c. In the left sidebar, navigate to "APIs & Services" > "Library."
#
# d. Search for "YouTube Data API" and click on it. Then, click the "Enable" button.
#
# e. In the left sidebar, go to "APIs & Services" > "Credentials."
#
# f. Click the "Create credentials" button and select "API Key." Your API key will be generated.
#
# g. Replace api_key = ' ' in your code with your actual API key.

##############################################################################################################

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
        part='snippet,statistics',  # Request specific parts of channel data
        id=','.join(channel_ids)  # Join multiple channel IDs into a single string
    )

    response = request.execute()  # Execute the request and get the response

    # Loop through the channel data in the response
    for item in response.get('items', []):
        data = {
            'Channel_name': item['snippet']['title'],  # Get channel name from snippet
            'Subscribers': item['statistics']['subscriberCount'],  # Get subscriber count
            'Views': item['statistics']['viewCount'],  # Get view count
            'Total_Videos': item['statistics']['videoCount']  # Get total video count
        }
        all_data.append(data)  # Append the data to the list

    return all_data


# Call the function to get channel statistics
channel_statistics = get_channel_stats(youtube, channel_ids)

# Create a DataFrame from the channel statistics
channel_data = pd.DataFrame(channel_statistics)

# Convert columns to numeric (e.g., converting subscriber counts, views, and video counts to integers)
channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_Videos'] = pd.to_numeric(channel_data['Total_Videos'])

# Modify the DataFrame to change a label of Crunchyroll channel
channel_data.loc[channel_data['Channel_name'] == 'Crunchyroll Collection', 'Channel_name'] = 'Crunchyroll'

# Set Seaborn plot size and style
sns.set(rc={'figure.figsize': (10, 8)})

# # Define a custom color palette with colors for each channel
custom_palette = {
    'Netflix': 'red',
    'Crunchyroll': '#FF6600',  # Use a darker shade of orange
    'Prime Video': 'blue',
    'Max': 'purple',
    'Peacock': 'black'
}

# Create a bar plot using Seaborn with the custom color palette
ax = sns.barplot(x='Channel_name', y='Subscribers', data=channel_data, palette=custom_palette, hue='Channel_name', legend=False)


# Customize the appearance of the x-axis labels
for tick in ax.get_xticklabels():
    tick.set_rotation(45)  # Rotate the labels by 45 degrees
    tick.set_ha('right')  # Set horizontal alignment to 'right'

    # Set the x and y axis labels and plot title
    ax.set(xlabel='Channels', ylabel='Subscribers')
    plt.title('Subscriber Count for Different Channels', fontsize=20, fontweight='bold')

# Set the x and y labels' font size
plt.xlabel('Channels', fontsize=16, fontweight='bold')
plt.ylabel('Subscribers', fontsize=16, fontweight='bold')

# Add a grid to the y-axis
ax.yaxis.grid(True, linestyle='--', alpha=0.7)


# Show the plot using Matplotlib
plt.show()
