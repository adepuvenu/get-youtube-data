from googleapiclient.discovery import build
import streamlit as stm


def main():
    stm.sidebar.title("Navigation's")
    page_options = [' ', "Get Data", "Insert Data", "Retrieve Data"]
    selected_page = stm.sidebar.selectbox("Select Option", page_options)

    if selected_page == 'Get Data':
        ch_id = stm.sidebar.text_input('Enter channel id', )
        if stm.sidebar.button('Get Data'):
            stm.write(get_page(ch_id))
    elif selected_page == "Insert Data":
        insert_page()
    elif selected_page == "Retrieve Data":
        retrieve_page()


def get_page(ch_id):
    stm.title("Youtube Data Harvesting")
    stm.write("Welcome to the get page!")
    api_key = ''    # need to give api key to execute
    youtube = build('youtube', 'v3', developerKey=api_key)
    req = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=ch_id
    )
    response = req.execute()
    ch_data = {
        'Channel_Details': {
            'id': ch_id,
            'Name': response['items'][0]['snippet']['title'],
            'Description': response['items'][0]['snippet']['description'],
            'Published_At': response['items'][0]['snippet']['publishedAt'],
            'Uploads': response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
            'View_Count': response['items'][0]['statistics']['viewCount'],
            'Sub_Count': response['items'][0]['statistics']['subscriberCount'],
            'Video_Count': response['items'][0]['statistics']['videoCount']
        },
        'Videos_Details': playlist_data(ch_id),
        'Comments_details': comment_data(ch_id)
    }
    return ch_data


def playlist_data(ch_id):
    api_key = ''    # need to give api key to execute
    youtube = build('youtube', 'v3', developerKey=api_key)

    plist_req = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=ch_id,
        maxResults=25
    )
    plist_res = plist_req.execute()
    play_list = []
    for i in range(len(plist_res['items'])):
        play_list.append(plist_res['items'][i]['id'])

    video_list = []
    for i in play_list:
        vlist_req = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=25,
            playlistId=i
        )
        vlist_res = vlist_req.execute()
        for x in range(len(vlist_res['items'])):
            video_list.append(vlist_res['items'][x]['contentDetails']['videoId'])

    vi_data = []
    for i in video_list:
        video_req = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=i
        )
        video_res = video_req.execute()

        vi_data.append({
            'Video_id': i,
            'Video_Name': video_res['items'][0]['snippet']['title'],
            'Video_Description': video_res['items'][0]['snippet']['description'],
            'Published_At': video_res['items'][0]['snippet']['publishedAt'],
            'View_count': video_res['items'][0]['statistics']['viewCount'],
            'Like_count': video_res['items'][0]['statistics']['likeCount'],
            'Favorite_count': video_res['items'][0]['statistics']['favoriteCount'],
            'Duration': video_res['items'][0]['contentDetails']['duration'],
            'Comment_count': video_res['items'][0]['statistics']['commentCount']
        })
    return vi_data


def comment_data(ch_id):
    api_key = ''  # need to give api key to execute
    youtube = build('youtube', 'v3', developerKey=api_key)

    plist_req = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=ch_id,
        maxResults=25
    )
    plist_res = plist_req.execute()
    play_list = []
    for i in range(len(plist_res['items'])):
        play_list.append(plist_res['items'][i]['id'])

    video_list = []
    for i in play_list:
        vlist_req = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=25,
            playlistId=i
        )
        vlist_res = vlist_req.execute()
        for x in range(len(vlist_res['items'])):
            video_list.append(vlist_res['items'][x]['contentDetails']['videoId'])

    comment_list = []
    for i in video_list:
        comment_req = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=i
        )
        comment_res = comment_req.execute()
        for x in range(len(comment_res['items'])):
            comment_list.append({
                'Video_id:' + i:
                    {'Comment_id': comment_res['items'][x]['id'],
                     'Comment_text': comment_res['items'][x]['snippet']['topLevelComment']['snippet']['textDisplay'],
                     'Comment_author': comment_res['items'][x]['snippet']['topLevelComment']['snippet'][
                         'authorDisplayName'],
                     'Comment_publishedat': comment_res['items'][x]['snippet']['topLevelComment']['snippet'][
                         'publishedAt']
                     }
            })
    return comment_list


def insert_page():
    stm.title("Insert Page")
    stm.write("This is Insert data into Mongodb page.")


def retrieve_page():
    stm.title("Retrieve Page")
    stm.write("This is Retrieve data from SQL db page")


if __name__ == "__main__":
    main()
