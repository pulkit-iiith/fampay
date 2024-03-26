from insert_data_in_database import Insert_data_in_database
from datetime import datetime

class Data_preprocessing:

    def trigger_processing(self,data):
        # parsed_response = json.loads(json_response)

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
        
        insert_data = Insert_data_in_database()
        insert_data.make_connection_and_insert_data(videos)
        

