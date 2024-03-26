from database_handler import Database_Handler
from datetime import datetime


class Service:
    def preprocess_data_and_insert(self,data):

        # Extract required information
        videos = []
        for item in data['items']:
            video = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'publishing_datetime': datetime.strptime(item['snippet']['publishTime'], '%Y-%m-%dT%H:%M:%SZ'),
                'thumbnails': {
                    'default': item['snippet']['thumbnails']['default']['url'],
                    'medium': item['snippet']['thumbnails']['medium']['url'],
                    'high': item['snippet']['thumbnails']['high']['url']
                }
            }
            videos.append(video)

        # Print extracted information
        for video in videos:
            print('Title:', video['title'])
            print('Description:', video['description'])
            print('Publishing Datetime:', video['publishing_datetime'])
            print('Thumbnails:')
            for key, value in video['thumbnails'].items():
                print(f'{key}: {value}')
            print()
        
        insert_data = Database_Handler()
        insert_data.make_connection_and_insert_data(videos)



    def get_videos(self,page,per_page):

        database_handler = Database_Handler()
        # Fetch video data
        video_data = database_handler.fetch_videos(page, per_page)

        # Format response
        response = []
        for video in video_data:
            response.append({
                'title': video[2],
                'description': video[3],
                'publishing_datetime': str(video[4]),
                'thumbnails': {
                    'default': video[5],
                    'medium': video[6],
                    'high': video[7]
                }
            })

        return response
    
    def search_videos(self,title_query,description_query):

        database_handler = Database_Handler()
        # Perform search
        search_results = database_handler.search_videos(title_query, description_query)

        # Format response
        response = []
        for video in search_results:
            response.append({
                'title': video[2],
                'description': video[3],
                'publishing_datetime': str(video[4]),
                'thumbnails': {
                    'default': video[5],
                    'medium': video[6],
                    'high': video[7]
                }
            })
        return response